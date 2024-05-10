# MIT License

# Copyright (c) 2024 asss-whom

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ast

from functools import singledispatch
from logging import basicConfig, getLogger
from rich.logging import RichHandler
from string import Template

basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
log = getLogger("rich")


def indenter(source: str) -> str:
    indent = " " * 4
    depth = 0
    lines = []

    for line in (
        source.replace("{", "{\n")
        .replace("}", "\n}")
        .replace(";", ";\n")
        .replace("\n\n", "\n")
        .splitlines()
    ):
        if "{" in line and "}" in line:
            lines.append(indent * (depth - 1) + line)
        elif "{" in line:
            lines.append(indent * depth + line)
            depth += 1
        elif "}" in line:
            depth -= 1
            lines.append(indent * depth + line)
        else:
            lines.append(indent * depth + line)
    return "\n".join(lines)


def to_sqf(source: str) -> str:
    module = ast.parse(source)
    result = translate(module)
    return indenter(result)


@singledispatch
def translate(node: ast.AST) -> str:
    log.warning(f"Unsupported node: {node:r}!")
    return ""


@translate.register(ast.Module)
@translate.register(ast.Interactive)
@translate.register(ast.Expression)
def _(node: ast.Module | ast.Interactive | ast.Expression) -> str:
    return "".join(translate(child) for child in ast.iter_child_nodes(node))


@translate.register(ast.FunctionDef)
def _(node: ast.FunctionDef) -> str:
    # TODO: Add default arguments support.
    if len(node.args.kwonlyargs) != 0 or len(node.args.defaults) != 0:
        log.warning(
            "Unsupport function arguments: keyword only and default arguments are not supported!"
        )
        return ""

    if len(node.decorator_list) != 0:
        log.warning("Unsupport function: function with decorator is not supported!")
        return ""

    func = Template("$funcname = {params [$args];$body};")
    args = ",".join(f'"_{arg.arg}"' for arg in node.args.args)
    body = "".join(translate(child) for child in node.body)
    return func.substitute(funcname=node.name, args=args, body=body)


@translate.register(ast.Return)
def _(node: ast.Return) -> str:
    return f"{translate(node.value)}" if node.value is not None else ""


@translate.register(ast.Delete)
def _(node: ast.Delete) -> str:
    syntax = []
    for target in node.targets:
        if not isinstance(target, ast.Name):
            log.warning(
                f"Unsupported delete: Deleting a non-name target is not supported!"
            )
            return ""

        syntax.append(f"_{target.id} = nil;")
    return "".join(syntax)


@translate.register(ast.Assign)
@translate.register(ast.AnnAssign)
def _(node: ast.Assign | ast.AnnAssign) -> str:
    rhs = node.value
    if rhs is None:
        log.warning(
            "Unsupport assign: assign without right hand side is not supported!"
        )
        return ""

    syntax = []
    # The type of `node.targets` is `list`.
    for lhs in node.targets:  # type: ignore
        if not isinstance(lhs, ast.Name):
            log.warning(
                f"Unsupported assign: assign with a non-name target is not supported!"
            )
            return ""

        # `lhs.ctx` must be `Store()` because it has `rhs`.
        syntax.append(f"_{lhs.id} = {translate(rhs)};")
    return "".join(syntax)


@translate.register(ast.AugAssign)
def _(node: ast.AugAssign) -> str:
    # `lhs.ctx` must be `Store()` because it must have `rhs`.
    lhs = node.target
    if not isinstance(lhs, ast.Name):
        raise RuntimeError(f"Unknown error happened in parsing {node}!")
    return f"_{lhs.id} = _{lhs.id} {translate(node.op)} {translate(node.value)};"


@translate.register(ast.For)
def _(node: ast.For) -> str:
    if len(node.orelse) != 0:
        log.warning("Unsupported or-else: else after for is not supported!")
        return ""

    # Special function: `range`.
    # TODO: find a better way to finish this.
    if (
        isinstance(node.iter, ast.Call)
        and isinstance(node.iter.func, ast.Name)
        and node.iter.func.id == "range"
    ):
        forrange = Template('for "$val" from $start to $stop step $step do{$body};')
        if not all(isinstance(arg, ast.Constant) for arg in node.iter.args):
            raise RuntimeError(f"Unknown error happened in parsing {node}!")

        if not isinstance(node.target, ast.Name):
            log.warning(
                "Unsupported variable: for-range loop can only have one variable!"
            )
            return ""

        val = f"_{node.target.id}"
        start = stop = 0
        step = 1
        # The type of `node.iter.args` is `list[ast.Constant]`.
        args: list[ast.Constant] = node.iter.args  # type: ignore
        match len(args):
            case 1:
                stop = args[0].value
            case 2:
                start, stop = (arg.value for arg in args)
            case 3:
                start, stop, step = (arg.value for arg in args)
        body = "".join(translate(child) for child in node.body)
        return forrange.substitute(
            val=val, start=start, stop=stop, step=step, body=body
        )

    foreach = Template("{$target;$body} forEach $iter;")
    if not isinstance(node.target, ast.Name):
        log.warning("Unsuppoted target: no-name target is not supported!")
        return ""

    var = node.target.id
    target = f"private _{var} = _x" if var != "x" else ""
    body = "".join(translate(child) for child in node.body)
    iter = translate(node.iter)
    return foreach.substitute(target=target, body=body, iter=iter)


@translate.register(ast.While)
def _(node: ast.While) -> str:
    if len(node.orelse) != 0:
        log.warning("Unsupported or-else: else after while is not supported!")
        return ""
    whileloop = Template("while {$condition} do {$body};")
    condition = translate(node.test)
    body = "".join(translate(child) for child in node.body)
    return whileloop.substitute(condition=condition, body=body)


@translate.register(ast.If)
def _(node: ast.If) -> str:
    if len(node.orelse) != 0:
        ifelse = Template("if ($condition) then {$ifbody} else {$elsebody};")
        condition = translate(node.test)
        ifbody = "".join(translate(child) for child in node.body)
        elsebody = "".join(translate(child) for child in node.orelse)
        return ifelse.substitute(condition=condition, ifbody=ifbody, elsebody=elsebody)
    pureif = Template("if ($condition) then {$body};")
    condition = translate(node.test)
    body = "".join(translate(child) for child in node.body)
    return pureif.substitute(condition=condition, body=body)


@translate.register(ast.Expr)
def _(node: ast.Expr) -> str:
    return f"{translate(node.value)};"


@translate.register(ast.Pass)
def _(node: ast.Pass) -> str:
    return ""


@translate.register(ast.BoolOp)
def _(node: ast.BoolOp) -> str:
    return translate(node.op).join(translate(child) for child in node.values)


@translate.register(ast.And)
def _(node: ast.And) -> str:
    return " && "


@translate.register(ast.Or)
def _(node: ast.Or) -> str:
    return " || "


@translate.register(ast.BinOp)
def _(node: ast.BinOp) -> str:
    return f"{translate(node.left)} {translate(node.op)} {translate(node.right)}"


@translate.register(ast.Add)
def _(node: ast.Add) -> str:
    return "+"


@translate.register(ast.Sub)
def _(node: ast.Sub) -> str:
    return "-"


@translate.register(ast.Mult)
def _(node: ast.Mult) -> str:
    return "*"


@translate.register(ast.Div)
def _(node: ast.Div) -> str:
    return "/"


@translate.register(ast.FloorDiv)
def _(node: ast.FloorDiv) -> str:
    return "/"


@translate.register(ast.Mod)
def _(node: ast.Mod) -> str:
    return "mod"


@translate.register(ast.Pow)
def _(node: ast.Pow) -> str:
    return "^"


@translate.register(ast.UnaryOp)
def _(node: ast.UnaryOp) -> str:
    return f"{translate(node.op)}{translate(node.operand)}"


@translate.register(ast.Not)
def _(node: ast.Not) -> str:
    return "!"


@translate.register(ast.IfExp)
def _(node: ast.IfExp) -> str:
    ifelse = Template("if ($condition) then {$ifbody} else {$elsebody};")
    condition = translate(node.test)
    ifbody = translate(node.body)
    elsebody = translate(node.orelse)
    return ifelse.substitute(condition=condition, ifbody=ifbody, elsebody=elsebody)


@translate.register(ast.Dict)
def _(node: ast.Dict) -> str:
    # TODO: Support dict.
    log.warning("Unsupported dict: dict is not supported!")
    return ""


@translate.register(ast.Compare)
def _(node: ast.Compare) -> str:
    if len(node.comparators) != 1:
        log.warning("Unsupported compare: multiple compare is not supported!")
        return ""
    return f"{translate(node.left)} {translate(node.ops[0])} {translate(node.comparators[0])}"


@translate.register(ast.Eq)
def _(node: ast.Eq) -> str:
    return "=="


@translate.register(ast.NotEq)
def _(node: ast.NotEq) -> str:
    return "!="


@translate.register(ast.Lt)
def _(node: ast.Lt) -> str:
    return "<"


@translate.register(ast.LtE)
def _(node: ast.LtE) -> str:
    return "<="


@translate.register(ast.Gt)
def _(node: ast.Gt) -> str:
    return ">"


@translate.register(ast.GtE)
def _(node: ast.GtE) -> str:
    return ">="


@translate.register(ast.Call)
def _(node: ast.Call) -> str:
    if len(node.keywords) != 0:
        log.warning("Unsupported function call: keyword argument is not supported!")
        return ""

    if any(isinstance(arg, ast.Starred) for arg in node.args):
        log.warning(
            "Unsupported function call: unpacking positional argument is not supported!"
        )
        return ""

    if isinstance(node.func, ast.Name):
        if len(node.args) == 1:
            return f"{translate(node.args[0])} call {node.func.id}"
        args = ", ".join(translate(arg) for arg in node.args)
        return f"[{args}] call {node.func.id}"

    if isinstance(node.func, ast.Attribute):
        if len(node.args) == 1:
            return f"{translate(node.func)} {translate(node.args[0])}"
        args = ", ".join(translate(arg) for arg in node.args)
        return f"{translate(node.func)} [{args}]"

    log.warning(f"Unsupported function call: {node.func} is not supported!")
    return ""


@translate.register(ast.Constant)
def _(node: ast.Constant) -> str:
    # None, str, bytes, bool, int, float, complex, Ellipsis
    if node.value is None:
        return "nil"
    if node.value is Ellipsis:
        return ""
    if isinstance(node.value, str):
        return f'"{node.value}"'
    if isinstance(node.value, bool):
        return "true" if node.value else "false"
    if isinstance(node.value, (int, float)):
        return str(node.value)
    log.warning(f"Unsupported constant: {node.value} is not supported")
    return ""


@translate.register(ast.Attribute)
def _(node: ast.Attribute) -> str:
    # Special mark: GLOBAL
    if isinstance(node.value, ast.Name) and node.value.id == "GLOBAL":
        return node.attr
    return f"{translate(node.value)} {node.attr}"


@translate.register(ast.Name)
def _(node: ast.Name) -> str:
    return f"_{node.id}"


@translate.register(ast.List)
@translate.register(ast.Tuple)
def _(node: ast.List | ast.Tuple) -> str:
    elems = ", ".join(translate(elem) for elem in node.elts)
    return f"[{elems}]"

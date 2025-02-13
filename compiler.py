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
from logging import getLogger
from string import Template

logger = getLogger(__name__)


def indenter(source: str) -> str:
    indent = " " * 4
    depth = 0
    lines: list[str] = []

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
    logger.warning(f"Unsupported node: {node:r}!")
    return ""


@translate.register
def _(node: ast.Module | ast.Interactive | ast.Expression) -> str:
    return "".join(translate(child) for child in ast.iter_child_nodes(node))


@translate.register
def _(node: ast.FunctionType) -> str:
    return ""


@translate.register
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
    logger.warning(f"Unsupported constant: {node.value} is not supported!")
    return ""


@translate.register
def _(node: ast.FormattedValue) -> str:
    if node.conversion != -1 or node.format_spec is not None:
        logger.warning(f"Unsupported format string: value format is not supported!")
        return ""
    return translate(node.value)


@translate.register
def _(node: ast.JoinedStr) -> str:
    # No need to format but is a f-string :(
    if all(isinstance(value, ast.Constant) for value in node.values):
        return "".join(value.value for value in node.values)  # type: ignore

    index = 1
    formatted_value: list[str] = []
    syntax: list[str] = []
    for value in node.values:
        if isinstance(value, ast.Constant):
            # The type of `value.value` is `str`
            syntax.append(value.value)
        else:
            # The type of `value` is `ast.FormattedValue`
            formatted_value.append(translate(value))
            syntax.append(f"%{index}")
            index += 1
    return f"format [\"{''.join(syntax)}\", {', '.join(formatted_value)}]"


@translate.register
def _(node: ast.List | ast.Tuple) -> str:
    elems = ", ".join(translate(elem) for elem in node.elts)
    return f"[{elems}]"


@translate.register
def _(node: ast.Name) -> str:
    return f"_{node.id}"


@translate.register
def _(node: ast.Expr) -> str:
    return f"{translate(node.value)};"


@translate.register
def _(node: ast.UnaryOp) -> str:
    return f"{translate(node.op)}{translate(node.operand)}"


@translate.register
def _(node: ast.Not) -> str:
    return "!"


@translate.register
def _(node: ast.BinOp) -> str:
    # Ugly but correct.
    left = (
        f"({translate(node.left)})"
        if isinstance(node.left, ast.BinOp)
        else translate(node.left)
    )
    right = (
        f"({translate(node.right)})"
        if isinstance(node.right, ast.BinOp)
        else translate(node.right)
    )
    return f"{left} {translate(node.op)} {right}"


@translate.register
def _(node: ast.Add) -> str:
    return "+"


@translate.register
def _(node: ast.Sub) -> str:
    return "-"


@translate.register
def _(node: ast.Mult) -> str:
    return "*"


@translate.register
def _(node: ast.Div) -> str:
    return "/"


@translate.register
def _(node: ast.FloorDiv) -> str:
    return "/"


@translate.register
def _(node: ast.Mod) -> str:
    return "mod"


@translate.register
def _(node: ast.Pow) -> str:
    return "^"


@translate.register
def _(node: ast.BoolOp) -> str:
    return translate(node.op).join(translate(child) for child in node.values)


@translate.register
def _(node: ast.And) -> str:
    return " && "


@translate.register
def _(node: ast.Or) -> str:
    return " || "


@translate.register
def _(node: ast.Compare) -> str:
    if len(node.comparators) != 1:
        logger.warning("Unsupported compare: multiple compare is not supported!")
        return ""
    return f"{translate(node.left)} {translate(node.ops[0])} {translate(node.comparators[0])}"


@translate.register
def _(node: ast.Eq) -> str:
    return "=="


@translate.register
def _(node: ast.NotEq) -> str:
    return "!="


@translate.register
def _(node: ast.Lt) -> str:
    return "<"


@translate.register
def _(node: ast.LtE) -> str:
    return "<="


@translate.register
def _(node: ast.Gt) -> str:
    return ">"


@translate.register
def _(node: ast.GtE) -> str:
    return ">="


@translate.register
def _(node: ast.Call) -> str:
    if len(node.keywords) != 0:
        logger.warning("Unsupported function call: keyword argument is not supported!")
        return ""

    if any(isinstance(arg, ast.Starred) for arg in node.args):
        logger.warning(
            "Unsupported function call: unpacking operator is not supported!"
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

    logger.warning(f"Unsupported function call: {node.func} is not supported!")
    return ""


@translate.register
def _(node: ast.IfExp) -> str:
    ifelse = Template("if ($condition) then {$ifbody} else {$elsebody};")
    condition = translate(node.test)
    ifbody = translate(node.body)
    elsebody = translate(node.orelse)
    return ifelse.substitute(condition=condition, ifbody=ifbody, elsebody=elsebody)


@translate.register
def _(node: ast.Attribute) -> str:
    # Special mark: GLOBAL
    if isinstance(node.value, ast.Name) and node.value.id == "GLOBAL":
        return node.attr
    return f"{translate(node.value)} {node.attr}"


@translate.register
def _(node: ast.Subscript) -> str:
    if isinstance(node.slice, ast.Constant):
        return f"{translate(node.value)} select {node.slice.value}"

    if isinstance(node.slice, ast.Slice):
        if node.slice.step is not None:
            logger.warning("Unsupported subscript: slice with step is not supported!")
            return ""

        if node.slice.lower is None or node.slice.upper is None:
            logger.warning(
                "Unsupported subscript: slice without lower or upper is not supported!"
            )
            return ""

        assert isinstance(node.slice.lower, ast.Constant) and isinstance(
            node.slice.upper, ast.Constant
        )
        return f"{translate(node.value)} select [{node.slice.lower.value}, {node.slice.upper.value - node.slice.lower.value}]"

    logger.warning("Unsupported subscript: multiple slice is not supported!")
    return ""


@translate.register
def _(node: ast.Assign | ast.AnnAssign) -> str:
    rhs = node.value
    if rhs is None:
        logger.warning(
            "Unsupport assign: assign without right hand side is not supported!"
        )
        return ""

    syntax: list[str] = []
    # The type of `node.targets` is `list`.
    for lhs in node.targets:  # type: ignore
        if isinstance(lhs, ast.Name):
            # `lhs.ctx` must be `Store()` because it has `rhs`.
            syntax.append(f"_{lhs.id} = {translate(rhs)};")
        elif isinstance(lhs, ast.Subscript):
            if not isinstance(lhs.slice, ast.Constant):
                logger.warning(f"Unsupported assign: {lhs} is not supported!")
                return ""
            index = lhs.slice.value
            syntax.append(f"{translate(node.value)} set [{index}, {translate(rhs)}]")
        else:
            logger.warning(f"Unsupported assign: {lhs} is not supported!")
            return ""
    return "".join(syntax)


@translate.register
def _(node: ast.AugAssign) -> str:
    # `lhs.ctx` must be `Store()` because it must have `rhs`.
    lhs = node.target
    assert isinstance(lhs, ast.Name)
    return f"_{lhs.id} = _{lhs.id} {translate(node.op)} {translate(node.value)};"


@translate.register
def _(node: ast.Delete) -> str:
    syntax: list[str] = []
    for target in node.targets:
        if not isinstance(target, ast.Name):
            logger.warning(
                f"Unsupported delete: Deleting a non-name target is not supported!"
            )
            return ""

        syntax.append(f"_{target.id} = nil;")
    return "".join(syntax)


@translate.register
def _(node: ast.Pass) -> str:
    return ""


@translate.register
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


@translate.register
def _(node: ast.For) -> str:
    if len(node.orelse) != 0:
        logger.warning("Unsupported or-else: else after for is not supported!")
        return ""

    # Special function: `range`.
    if (
        isinstance(node.iter, ast.Call)
        and isinstance(node.iter.func, ast.Name)
        and node.iter.func.id == "range"
    ):
        forrange = Template('for "$val" from $start to $stop step $step do{$body};')
        assert all(isinstance(arg, ast.Constant) for arg in node.iter.args)
        if not isinstance(node.target, ast.Name):
            logger.warning(
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
            case _:
                logger.error("Unknown arguments!")
        body = "".join(translate(child) for child in node.body)
        return forrange.substitute(
            val=val, start=start, stop=stop, step=step, body=body
        )

    foreach = Template("{$target;$body} forEach $iter;")
    if not isinstance(node.target, ast.Name):
        logger.warning("Unsuppoted target: no-name target is not supported!")
        return ""

    var = node.target.id
    target = f"private _{var} = _x" if var != "x" else ""
    body = "".join(translate(child) for child in node.body)
    iter = translate(node.iter)
    return foreach.substitute(target=target, body=body, iter=iter)


@translate.register
def _(node: ast.While) -> str:
    if len(node.orelse) != 0:
        logger.warning("Unsupported or-else: else after while is not supported!")
        return ""
    whileloop = Template("while {$condition} do {$body};")
    condition = translate(node.test)
    body = "".join(translate(child) for child in node.body)
    return whileloop.substitute(condition=condition, body=body)


@translate.register
def _(node: ast.Break) -> str:
    return "break;"


@translate.register
def _(node: ast.Continue) -> str:
    return "continue;"


@translate.register
def _(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    # TODO: Add default arguments support.
    if len(node.args.kwonlyargs) != 0 or len(node.args.defaults) != 0:
        logger.warning(
            "Unsupport function arguments: keyword only and default arguments are not supported!"
        )
        return ""

    if len(node.decorator_list) != 0:
        logger.warning("Unsupport function: function with decorator is not supported!")
        return ""

    func = Template("$funcname = {params [$args];$body};")
    args = ", ".join(f'"_{arg.arg}"' for arg in node.args.args)
    body = "".join(translate(child) for child in node.body)
    return func.substitute(funcname=node.name, args=args, body=body)


@translate.register
def _(node: ast.Return) -> str:
    return f"{translate(node.value)}" if node.value is not None else ""

def gcd(x: int, y: int) -> int:
    if x > y:
        temp = x
        x = y
        y = temp

    while y != 0:
        temp = x
        x = y
        y = temp % y

    return x

for curator in GLOBAL.allCurators:
    curator.addCuratorEditableObjects(GLOBAL.allMissionObjects("ALL"), True)

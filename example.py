def can_bomb(bomber, target):
    height = GLOBAL.getPosATL(bomber)[2]
    distance = bomber.distance2D(target)
    speed = GLOBAL.speed(bomber) * 1000 / (60 * 60)

    time = (2 * height / 9.8) ** 0.5
    return distance <= speed * time


async def drop_bomb(bomber, target, weapon):
    await can_bomb(bomber, target)

    while bomber.ammo(weapon) != 0:
        BIS_fnc_fire(bomber, weapon)
        GLOBAL.sleep(0.1)

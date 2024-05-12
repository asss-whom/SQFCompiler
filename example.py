def can_bomb(bomber, target):
    height = GLOBAL.getPosATL(bomber)[2]
    distance = bomber.distance2D(target)
    speed = GLOBAL.speed(bomber) * 1000 / (60 * 60)
    time = (2 * height / 9.8) ** 0.5
    GLOBAL.hint(f"d = {distance}, v = {speed}, t = {time}")
    return distance <= speed * time


async def drop_bomb(bomber, target, weapon):
    await can_bomb(bomber, target)

    count = 0
    while bomber.ammo(weapon) > 0:
        bomber.selectWeapon(weapon)
        bomber.fire(weapon)
        count += 1
        GLOBAL.hint(f"Fired Bomb {count}")
        GLOBAL.sleep(0.5)


drop_bomb(GLOBAL.this, GLOBAL.target, "BombCluster_02_F")

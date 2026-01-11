for target in GLOBAL.vehicles:
    if GLOBAL.side(GLOBAL.player).getFriend(GLOBAL.side(target)) < 0.6:
        if target.isKindOf("Land") or target.isKindOf("Ship"):
            missile = GLOBAL.createVehicle(
                "ammo_Missile_Cruise_01",
                GLOBAL.player.modelToWorld(0, 0, 100),
                [],
                0,
                "CAN_COLLIDE",
            )
            missile.setDir(GLOBAL.player.getDir(target))
            missile.setMissileTarget(target, True)
        if target.isKindOf("Air"):
            missile = GLOBAL.createVehicle(
                "ammo_Missile_mim145",
                GLOBAL.player.modelToWorld(0, 0, 100),
                [],
                0,
                "CAN_COLLIDE",
            )
            missile.setDir(GLOBAL.player.getDir(target))
            missile.setMissileTarget(target, True)

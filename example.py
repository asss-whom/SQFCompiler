for obj in GLOBAL.vehicles:
    if GLOBAL.side(GLOBAL.player).getFriend(GLOBAL.side(obj)) < 0.6:
        if obj.isKindOf("Land") or obj.isKindOf("Ship"):
            missile = GLOBAL.createVehicle(
                "Missile_AGM_01_F",
                GLOBAL.player.modelToWorld(0, 0, 100),
                [],
                0,
                "CAN_COLLIDE",
            )
            missile.setDir(GLOBAL.getDir(GLOBAL.player))
            missile.setMissileTarget(obj, True)
        if obj.isKindOf("Air"):
            missile = GLOBAL.createVehicle(
                "Missile_AA_03_F",
                GLOBAL.player.modelToWorld(0, 0, 100),
                [],
                0,
                "CAN_COLLIDE",
            )
            missile.setDir(GLOBAL.getDir(GLOBAL.player))
            missile.setMissileTarget(obj, True)

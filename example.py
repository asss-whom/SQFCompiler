jet = GLOBAL.vehicle(GLOBAL.this)
for target in GLOBAL.vehicles:
    if GLOBAL.side(GLOBAL.this).getFriend(GLOBAL.side(target)) < 0.6:
        if GLOBAL.side(GLOBAL.this) == GLOBAL.blufor:
            if target.isKindOf("Land") or target.isKindOf("Ship"):
                missile = GLOBAL.createVehicle(
                    "Missile_AGM_02_F",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)
            if target.isKindOf("Air"):
                missile = GLOBAL.createVehicle(
                    "ammo_Missile_AMRAAM_D",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)
        if GLOBAL.side(GLOBAL.this) == GLOBAL.opfor:
            if target.isKindOf("Land") or target.isKindOf("Ship"):
                missile = GLOBAL.createVehicle(
                    "Missile_AGM_01_F",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)
            if target.isKindOf("Air"):
                missile = GLOBAL.createVehicle(
                    "ammo_Missile_AA_R77",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)
        if GLOBAL.side(GLOBAL.this) == GLOBAL.independent:
            if target.isKindOf("Land") or target.isKindOf("Ship"):
                missile = GLOBAL.createVehicle(
                    "Missile_AGM_02_F",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)
            if target.isKindOf("Air"):
                missile = GLOBAL.createVehicle(
                    "ammo_Missile_AMRAAM_C",
                    jet.modelToWorld(0, 0, -5),
                    [],
                    0,
                    "CAN_COLLIDE",
                )
                missile.setDir(GLOBAL.getDir(jet))
                missile.setMissileTarget(target, True)

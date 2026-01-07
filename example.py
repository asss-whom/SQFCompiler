jet = GLOBAL.vehicle(GLOBAL.this)
for obj in GLOBAL.vehicles:
    if GLOBAL.side(GLOBAL.this).getFriend(GLOBAL.side(obj)) < 0.6:
        missile = GLOBAL.createVehicle(
            "ammo_Missile_Cruise_01",
            jet.modelToWorld(0, 0, -5),
            [],
            0,
            "CAN_COLLIDE",
        )
        missile.setDir(GLOBAL.getDir(jet))
        missile.setMissileTarget(obj, True)

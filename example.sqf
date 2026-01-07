_jet = vehicle this;
{
    private _obj = _x;
    if (side this getFriend side _obj < 0.6) then {
        _missile = createVehicle ["ammo_Missile_Cruise_01", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
        _missile setDir getDir _jet;
        _missile setMissileTarget [_obj, true];
    };
} forEach vehicles;
{
    private _obj = _x;
    if (side player getFriend side _obj < 0.6) then {
        if (_obj isKindOf "Land" || _obj isKindOf "Ship") then {
            _missile = createVehicle ["Missile_AGM_01_F", player modelToWorld [0, 0, 100], [], 0, "CAN_COLLIDE"];
            _missile setDir getDir player;
            _missile setMissileTarget [_obj, true];
        };
        if (_obj isKindOf "Air") then {
            _missile = createVehicle ["Missile_AA_03_F", player modelToWorld [0, 0, 100], [], 0, "CAN_COLLIDE"];
            _missile setDir getDir player;
            _missile setMissileTarget [_obj, true];
        };
    };
} forEach vehicles;
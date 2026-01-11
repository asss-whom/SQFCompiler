{
    private _target = _x;
    if (side player getFriend side _target < 0.6) then {
        if (_target isKindOf "Land" || _target isKindOf "Ship") then {
            _missile = createVehicle ["ammo_Missile_Cruise_01", player modelToWorld [0, 0, 100], [], 0, "CAN_COLLIDE"];
            _missile setDir player getDir _target;
            _missile setMissileTarget [_target, true];
        };
        if (_target isKindOf "Air") then {
            _missile = createVehicle ["ammo_Missile_mim145", player modelToWorld [0, 0, 100], [], 0, "CAN_COLLIDE"];
            _missile setDir player getDir _target;
            _missile setMissileTarget [_target, true];
        };
    };
} forEach vehicles;
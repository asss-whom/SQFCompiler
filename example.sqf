_jet = vehicle this;
{
    private _target = _x;
    if (side this getFriend side _target < 0.6) then {
        if (side this == blufor) then {
            if (_target isKindOf "Land" || _target isKindOf "Ship") then {
                _missile = createVehicle ["Missile_AGM_02_F", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
            if (_target isKindOf "Air") then {
                _missile = createVehicle ["ammo_Missile_AMRAAM_D", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
        };
        if (side this == opfor) then {
            if (_target isKindOf "Land" || _target isKindOf "Ship") then {
                _missile = createVehicle ["Missile_AGM_01_F", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
            if (_target isKindOf "Air") then {
                _missile = createVehicle ["ammo_Missile_AA_R77", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
        };
        if (side this == independent) then {
            if (_target isKindOf "Land" || _target isKindOf "Ship") then {
                _missile = createVehicle ["Missile_AGM_02_F", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
            if (_target isKindOf "Air") then {
                _missile = createVehicle ["ammo_Missile_AMRAAM_C", _jet modelToWorld [0, 0, -5], [], 0, "CAN_COLLIDE"];
                _missile setDir getDir _jet;
                _missile setMissileTarget [_target, true];
            };
        };
    };
} forEach vehicles;
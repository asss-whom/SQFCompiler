can_bomb = {
    params ["_bomber", "_target"];
    _height = getPosATL _bomber [select|get] 2;
    _distance = _bomber distance2D _target;
    _speed = speed _bomber * 1000 / 60 * 60;
    _time = 2 * _height / 9.8 ^ 0.5;
    _distance <= _speed * _time
};
drop_bomb = {
    params ["_bomber", "_target", "_weapon"];
    waitUntil {
        [_bomber, _target] call can_bomb
    };
    while {
        _bomber ammo _weapon != 0
    } do {
        [_bomber, _weapon] call BIS_fnc_fire;
        sleep 0.1;
    };
};

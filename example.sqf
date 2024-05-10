gcd = {
    params ["_x","_y"];
    if (_x > _y) then {
        _temp = _x;
        _x = _y;
        _y = _temp;
    };
    while {
        _y != 0
    } do {
        _temp = _x;
        _x = _y;
        _y = _temp mod _y;
    };
    _x
};
{
    private _curator = _x;
    _curator addCuratorEditableObjects [allMissionObjects "ALL", true];
} forEach allCurators;
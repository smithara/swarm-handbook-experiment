SPACECRAFT = {
    "CASSIOPE_e-POP": ("CASSIOPE_e-POP (Swarm-E)",),
    "CHAMP": ("CHAMP",),
    "Combined_Mission_Data": ("Combined_Mission_Data",),
    "CryoSat-2": ("CryoSat-2",),
    "CSES": ("CSES-01",),
    "GOCE": ("GOCE",),
    "GRACE": ("GRACE-A", "GRACE-B",),
    "GRACE-FO": ("GRACE-FO-1", "GRACE-FO-2",),
    "Miscellaneous": ("Miscellaneous",),
    "Swarm": ("Swarm-A", "Swarm-B", "Swarm-C"),
}  
# Build reverse mapping
SC2MISSIONS = {}
for _mission, _spacecraft_set in SPACECRAFT.items():
    for _spacecraft in _spacecraft_set:
        SC2MISSIONS[_spacecraft] = _mission
        # print(f'"{_spacecraft}",')

THEMATIC_AREAS = [
    'Magnetic measurements',
    'Plasma measurements',
    'Space Weather',
    'Ionosphere/Magnetosphere',
    'Thermosphere',
    'Lithosphere',
    'Core field',
    'Ocean Tides',
    'Mantle',
    'Geodesy/Gravity',
    'Acceleration measurements',
    'Attitude information',
    'Orbit information',
    'Ephemeris',
    'GNSS measurements',
    'HK data',
]
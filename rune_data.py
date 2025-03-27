"""
This module contains data structures for rune mappings and characteristic identifiers.
"""

runeNames = {
    "Vitality": ["vi", "pa_vi", "ra_vi"],
    "Strength": ["fo", "pa_fo", "ra_fo"],
    "Chance": ["cha", "pa_cha", "ra_cha"],
    "Intelligence": ["ine", "pa_ine", "ra_ine"],
    "Agility": ["agi", "pa_agi", "ra_agi"],
    "Wisdom": ["sa", "pa_sa", "ra_sa"],
    "Fire Damage": ["do_feu", "pa_do_feu"],
    "Air Damage": ["do_air", "pa_do_air"],
    "Water Damage": ["do_eau", "pa_do_eau"],
    "Earth Damage": ["do_terre", "pa_do_terre"],
    "Neutral Damage": ["do_neutre", "pa_do_neutre"],
    "Initiative": ["ini", "pa_ini", "ra_ini"],
    "Range": ["po"],
    "Prospecting": ["prospe", "pa_prospe"],
    "AP": ["pa"],
    "MP": ["pm"],
    "Summons": ["invoc"],
    "% Neutral Resistance": ["re_per_neutre"],
    "% Earth Resistance": ["re_per_terre"],
    "% Water Resistance": ["re_per_eau"],
    "% Air Resistance": ["re_per_air"],
    "% Fire Resistance": ["re_per_feu"],
    "Fire Resistance": ["re_feu", "pa_re_feu", "ra_re_feu"],
    "Air Resistance": ["re_air", "pa_re_air", "ra_re_air"],
    "Water Resistance": ["re_eau", "pa_re_eau", "ra_re_eau"],
    "Earth Resistance": ["re_terre", "pa_re_terre", "ra_re_terre"],
    "Neutral Resistance": ["re_neutre", "pa_re_neutre", "ra_re_neutre"],
    "Lock": ["tac", "pa_tac"],
    "Dodge": ["fui", "pa_fui"],
    "Heals": ["so", "pa_so"],
    "Critical": ["cri"],
    "Puissance": ["pui", "pa_pui", "ra_pui"],
    "Critical Resistance": ["re_cri", "pa_re_cri", "ra_re_cri"],
    "Pushback Resistance": ["re_pou", "pa_re_pou", "ra_re_pou"],
    "% Spell Damage": ["do_per_so"],
}

runeNumbers = {
    "Vitality": [1, 2, 3],
    "Strength": [4, 5, 6],
    "Chance": [7, 8, 9],
    "Intelligence": [10, 11, 12],
    "Agility": [13, 14, 15],
    "Wisdom": [16, 17, 18],
    "Fire Damage": [19, 20],
    "Air Damage": [21, 22],
    "Water Damage": [23, 24],
    "Earth Damage": [25, 26],
    "Neutral Damage": [27, 28],
    "Critical Damage": [29, 30],
    "Initiative": [31, 32, 33],
    "Range": [34],
    "Prospecting": [35, 36],
    "AP": [37],
    "MP": [38],
    "Summons": [39],
    "% Neutral Resistance": [40],
    "% Earth Resistance": [41],
    "% Water Resistance": [42],
    "% Air Resistance": [43],
    "% Fire Resistance": [44],
    "Fire Resistance": [45, 46, 47],
    "Air Resistance": [48, 49, 50],
    "Water Resistance": [51, 52, 53],
    "Earth Resistance": [54, 55, 56],
    "Neutral Resistance": [57, 58, 59],
    "Lock": [60, 61],
    "Dodge": [62, 63],
    "AP Parry": [64, 65],
    "MP Parry": [66, 67],
    "AP Reduction": [68, 69],
    "MP Reduction": [70, 71],
    "Heals": [72, 73],
    "Critical": [74],
    "Power (traps)": [75, 76, 77],
    "Trap Damage": [78, 79],
    "Power": [80, 81, 82],
    "Critical Resistance": [83, 84, 85],
    "Pushback Resistance": [86, 87, 88],
    "% Spell Damage": [89],
    "% Ranged Damage": [90],
    "% Melee Damage": [91],
    "% Ranged Resistance": [92],
    "% Melee Resistance": [93],
    "% Weapon Damage": [94],
    "Pods": [95, 96, 97],
    "Hunting": [98],
    "Damage": [99],
}

# Map each characteristic name to a unique ID
caracId = {
    "Vitality": 1,
    "Strength": 2,
    "Chance": 3,
    "Intelligence": 4,
    "Agility": 5,
    "Wisdom": 6,
    "Fire Damage": 7,
    "Air Damage": 8,
    "Water Damage": 9,
    "Earth Damage": 10,
    "Neutral Damage": 11,
    "Critical Damage": 12,
    "Initiative": 13,
    "Range": 14,
    "Prospecting": 15,
    "AP": 16,
    "MP": 17,
    "Summons": 18,
    "% Neutral Resistance": 19,
    "% Earth Resistance": 20,
    "% Water Resistance": 21,
    "% Air Resistance": 22,
    "% Fire Resistance": 23,
    "Fire Resistance": 24,
    "Air Resistance": 25,
    "Water Resistance": 26,
    "Earth Resistance": 27,
    "Neutral Resistance": 28,
    "Lock": 29,
    "Dodge": 30,
    "AP Parry": 31,
    "MP Parry": 32,
    "AP Reduction": 33,
    "MP Reduction": 34,
    "Heals": 35,
    "Critical": 36,
    "Power (traps)": 37,
    "Trap Damage": 38,
    "Power": 39,
    "Critical Resistance": 40,
    "Pushback Resistance": 41,
    "% Spell Damage": 42,
    "% Ranged Damage": 43,
    "% Melee Damage": 44,
    "% Ranged Resistance": 45,
    "% Melee Resistance": 46,
    "% Weapon Damage": 47,
    "Pods": 48,
    "Hunting": 49,
    "Damage": 50,
}

# Hard-coded runeIds mapping caracId keys to runeNumbers values
runeIds = {
    1: [1, 2, 3],        # Vitality
    2: [4, 5, 6],        # Strength
    3: [7, 8, 9],        # Chance
    4: [10, 11, 12],     # Intelligence
    5: [13, 14, 15],     # Agility
    6: [16, 17, 18],     # Wisdom
    7: [19, 20],         # Fire Damage
    8: [21, 22],         # Air Damage
    9: [23, 24],         # Water Damage
    10: [25, 26],        # Earth Damage
    11: [27, 28],        # Neutral Damage
    12: [29, 30],        # Critical Damage
    13: [31, 32, 33],    # Initiative
    14: [34],            # Range
    15: [35, 36],        # Prospecting
    16: [37],            # AP
    17: [38],            # MP
    18: [39],            # Summons
    19: [40],            # % Neutral Resistance
    20: [41],            # % Earth Resistance
    21: [42],            # % Water Resistance
    22: [43],            # % Air Resistance
    23: [44],            # % Fire Resistance
    24: [45, 46, 47],    # Fire Resistance
    25: [48, 49, 50],    # Air Resistance
    26: [51, 52, 53],    # Water Resistance
    27: [54, 55, 56],    # Earth Resistance
    28: [57, 58, 59],    # Neutral Resistance
    29: [60, 61],        # Lock
    30: [62, 63],        # Dodge
    31: [64, 65],        # AP Parry
    32: [66, 67],        # MP Parry
    33: [68, 69],        # AP Reduction
    34: [70, 71],        # MP Reduction
    35: [72, 73],        # Heals
    36: [74],            # Critical
    37: [75, 76, 77],    # Power (traps)
    38: [78, 79],        # Trap Damage
    39: [80, 81, 82],    # Power
    40: [83, 84, 85],    # Critical Resistance
    41: [86, 87, 88],    # Pushback Resistance
    42: [89],            # % Spell Damage
    43: [90],            # % Ranged Damage
    44: [91],            # % Melee Damage
    45: [92],            # % Ranged Resistance
    46: [93],            # % Melee Resistance
    47: [94],            # % Weapon Damage
    48: [95, 96, 97],    # Pods
    49: [98],            # Hunting
    50: [99],            # Damage
}

# Map rune IDs to their weights
runeWeight = {
    1: 1.0,     # vi (Vitality)
    2: 3.0,     # pa_vi (Vitality)
    3: 10.0,    # ra_vi (Vitality)
    4: 1.0,     # fo (Strength)
    5: 3.0,     # pa_fo (Strength)
    6: 10.0,    # ra_fo (Strength)
    7: 1.0,     # cha (Chance)
    8: 3.0,     # pa_cha (Chance)
    9: 10.0,    # ra_cha (Chance)
    10: 1.0,    # ine (Intelligence)
    11: 3.0,    # pa_ine (Intelligence)
    12: 10.0,   # ra_ine (Intelligence)
    13: 1.0,    # agi (Agility)
    14: 3.0,    # pa_agi (Agility)
    15: 10.0,   # ra_agi (Agility)
    16: 3.0,    # sa (Wisdom)
    17: 9.0,    # pa_sa (Wisdom)
    18: 30.0,   # ra_sa (Wisdom)
    19: 5.0,    # do_feu (Fire Damage)
    20: 15.0,   # pa_do_feu (Fire Damage)
    21: 5.0,    # do_air (Air Damage)
    22: 15.0,   # pa_do_air (Air Damage)
    23: 5.0,    # do_eau (Water Damage)
    24: 15.0,   # pa_do_eau (Water Damage)
    25: 5.0,    # do_terre (Earth Damage)
    26: 15.0,   # pa_do_terre (Earth Damage)
    27: 5.0,    # do_neutre (Neutral Damage)
    28: 15.0,   # pa_do_neutre (Neutral Damage)
    29: 5.0,    # Critical Damage
    30: 15.0,   # Critical Damage
    31: 1.0,    # ini (Initiative)
    32: 3.0,    # pa_ini (Initiative)
    33: 10.0,   # ra_ini (Initiative)
    34: 51.0,   # po (Range)
    35: 3.0,    # prospe (Prospecting)
    36: 9.0,    # pa_prospe (Prospecting)
    37: 100.0,  # pa (AP)
    38: 90.0,   # pm (MP)
    39: 30.0,   # invoc (Summons)
    40: 6.0,    # re_per_neutre (% Neutral Resistance)
    41: 6.0,    # re_per_terre (% Earth Resistance)
    42: 6.0,    # re_per_eau (% Water Resistance)
    43: 6.0,    # re_per_air (% Air Resistance)
    44: 6.0,    # re_per_feu (% Fire Resistance)
    45: 2.0,    # re_feu (Fire Resistance)
    46: 6.0,    # pa_re_feu (Fire Resistance)
    47: 18.0,   # ra_re_feu (Fire Resistance)
    48: 2.0,    # re_air (Air Resistance)
    49: 6.0,    # pa_re_air (Air Resistance)
    50: 18.0,   # ra_re_air (Air Resistance)
    51: 2.0,    # re_eau (Water Resistance)
    52: 6.0,    # pa_re_eau (Water Resistance)
    53: 18.0,   # ra_re_eau (Water Resistance)
    54: 2.0,    # re_terre (Earth Resistance)
    55: 6.0,    # pa_re_terre (Earth Resistance)
    56: 18.0,   # ra_re_terre (Earth Resistance)
    57: 2.0,    # re_neutre (Neutral Resistance)
    58: 6.0,    # pa_re_neutre (Neutral Resistance)
    59: 18.0,   # ra_re_neutre (Neutral Resistance)
    60: 4.0,    # tac (Lock)
    61: 12.0,   # pa_tac (Lock)
    62: 4.0,    # fui (Dodge)
    63: 12.0,   # pa_fui (Dodge)
    64: 7.0,    # AP Parry
    65: 21.0,   # pa_AP Parry
    66: 7.0,    # MP Parry
    67: 21.0,   # pa_MP Parry
    68: 7.0,    # AP Reduction
    69: 21.0,   # pa_AP Reduction
    70: 7.0,    # MP Reduction
    71: 21.0,   # pa_MP Reduction
    72: 10.0,   # so (Heals)
    73: 30.0,   # pa_so (Heals)
    74: 10.0,   # cri (Critical)
    75: 2.0,    # Power (traps)
    76: 6.0,    # pa_Power (traps)
    77: 18.0,   # ra_Power (traps)
    78: 5.0,    # Trap Damage
    79: 15.0,   # pa_Trap Damage
    80: 2.0,    # pui (Power)
    81: 6.0,    # pa_pui (Power)
    82: 18.0,   # ra_pui (Power)
    83: 2.0,    # re_cri (Critical Resistance)
    84: 6.0,    # pa_re_cri (Critical Resistance)
    85: 18.0,   # ra_re_cri (Critical Resistance)
    86: 2.0,    # re_pou (Pushback Resistance)
    87: 6.0,    # pa_re_pou (Pushback Resistance)
    88: 18.0,   # ra_re_pou (Pushback Resistance)
    89: 15.0,   # do_per_so (% Spell Damage)
    90: 15.0,   # % Ranged Damage
    91: 15.0,   # % Melee Damage
    92: 15.0,   # % Ranged Resistance
    93: 15.0,   # % Melee Resistance
    94: 15.0,   # % Weapon Damage
    95: 2.5,    # Pods
    96: 7.5,    # pa_Pods
    97: 25.0,   # ra_Pods
    98: 5.0,    # Hunting
    99: 5.0,    # Damage
}

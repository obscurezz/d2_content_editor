# settings.py
VISIBLE_FIELDS_GUNITS = [
    'UNIT_ID',
    'UNIT_CAT',
    'LEVEL',
    'RACE_ID',
    'SUBRACE',
    'BRANCH',
    'ENROLL_C',
    'NAME_TXT',
    'DESC_TXT',
    'ABIL_TXT',
    'ATCK_TWICE',
    'HIT_POINT',
    'ARMOR',
    'REGEN',
    'REVIVE_C',
    'HEAL_C',
    'TRAINING_C',
    'XP_KILLED',
    'UPGRADE_B',
    'XP_NEXT',
    'MOVE',
    'SCOUT',
    'LEADERSHIP',
    'NEGOTIATE',
    'LEADER_CAT',
    'DYN_UPG1',
    'DYN_UPG_LV',
    'DYN_UPG2'
]

VISIBLE_FIELDS_GATTACKS = [
    'ATT_ID',
    'INITIATIVE',
    'SOURCE',
    'CLASS',
    'POWER',
    'REACH',
    'QTY_HEAL',
    'QTY_DAM',
    'LEVEL',
    'INFINITE',
    'QTY_WARDS',
    'WARD1',
    'WARD2',
    'WARD3',
    'WARD4',
    'CRIT_HIT',
    'DAM_RATIO',
    'DR_REPEAT',
    'DAM_SPLIT',
    'CRIT_DAM',
    'CRIT_POWER'
]

FIELD_TYPES = {
    67: {'widget': 'Entry'},     # C - Character (строка)
    78: {'widget': 'Spinbox'},  # N - Numeric (число)
    76: {'widget': 'Checkbutton'}  # L - Logical (булевый)
}

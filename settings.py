# settings.py
VISIBLE_FIELDS = [
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
    'ATTACK_ID',
    'ATTACK2_ID',
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

FIELD_TYPES = {
    67: {'widget': 'Entry'},     # C - Character (строка)
    78: {'widget': 'Spinbox'},  # N - Numeric (число)
    76: {'widget': 'Checkbutton'}  # L - Logical (булевый)
}
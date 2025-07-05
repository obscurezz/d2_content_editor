import dbf
import os
from dbf import is_deleted


class DatabaseManager:
    def __init__(self):
        self.GUNITS_TABLE = None
        self.GATTACKS_TABLE = None
        self.GIMMU_TABLE = None
        self.GIMMUC_TABLE = None

        self.LSUBRACE_TABLE = None
        self.subrace_options = {}

        self.LATTS_TABLE = None
        self.attack_source_options = {}

        self.LATTC_TABLE = None
        self.attack_class_options = {}

        self.LATTR_TABLE = None
        self.attack_reach_options = {}

        self.LIMMUNE_TABLE = None
        self.immunity_options = {}

    def open_databases(self, directory):
        # Искать файлы в вложенном каталоге Globals
        globals_dir = os.path.join(directory, 'Globals')
        if not os.path.exists(globals_dir):
            return False

        gunits_path = None
        gattacks_path = None
        gimmu_path = None
        gimmuc_path = None
        lsubrace_path = None
        latts_path = None
        lattc_path = None
        lattr_path = None
        limmune_path = None

        for filename in os.listdir(globals_dir):
            if filename.lower() == 'gunits.dbf':
                gunits_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'gattacks.dbf':
                gattacks_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'gimmu.dbf':
                gimmu_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'gimmuc.dbf':
                gimmuc_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'lsubrace.dbf':
                lsubrace_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'latts.dbf':
                latts_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'lattc.dbf':
                lattc_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'lattr.dbf':
                lattr_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'limmune.dbf':
                limmune_path = os.path.join(globals_dir, filename)

        if gunits_path:
            self.GUNITS_TABLE = dbf.Table(gunits_path)
            self.GUNITS_TABLE.open(mode=dbf.READ_WRITE)
        else:
            return False

        if gattacks_path:
            self.GATTACKS_TABLE = dbf.Table(gattacks_path)
            self.GATTACKS_TABLE.open(mode=dbf.READ_WRITE)
        else:
            return False

        if gimmu_path:
            self.GIMMU_TABLE = dbf.Table(gimmu_path)
            self.GIMMU_TABLE.open(mode=dbf.READ_WRITE)
        else:
            return False

        if gimmuc_path:
            self.GIMMUC_TABLE = dbf.Table(gimmuc_path)
            self.GIMMUC_TABLE.open(mode=dbf.READ_WRITE)
        else:
            return False

        if lsubrace_path:
            self.LSUBRACE_TABLE = dbf.Table(lsubrace_path)
            self.LSUBRACE_TABLE.open(mode=dbf.READ_ONLY)
            self.subrace_options = {rec.ID: rec.TEXT for rec in self.LSUBRACE_TABLE if not is_deleted(rec)}
        else:
            return False

        if latts_path:
            self.LATTS_TABLE = dbf.Table(latts_path)
            self.LATTS_TABLE.open(mode=dbf.READ_ONLY)
            self.attack_source_options = {rec.ID: rec.TEXT for rec in self.LATTS_TABLE if not is_deleted(rec)}
        else:
            return False

        if lattc_path:
            self.LATTC_TABLE = dbf.Table(lattc_path)
            self.LATTC_TABLE.open(mode=dbf.READ_ONLY)
            self.attack_class_options = {rec.ID: rec.TEXT for rec in self.LATTC_TABLE if not is_deleted(rec)}
        else:
            return False

        if lattr_path:
            self.LATTR_TABLE = dbf.Table(lattr_path)
            self.LATTR_TABLE.open(mode=dbf.READ_ONLY)
            self.attack_reach_options = {rec.ID: rec.TEXT for rec in self.LATTR_TABLE if not is_deleted(rec)}
        else:
            return False

        if limmune_path:
            self.LIMMUNE_TABLE = dbf.Table(limmune_path)
            self.LIMMUNE_TABLE.open(mode=dbf.READ_ONLY)
            self.immunity_options = {rec.ID: rec.TEXT for rec in self.LIMMUNE_TABLE if not is_deleted(rec)}
        else:
            return False

        return True

    def fetch_record_by_unit_id(self, unit_id):
        for record in self.GUNITS_TABLE:
            if not is_deleted(record) and record.UNIT_ID == unit_id:
                return record
        return None

    def fetch_attack_by_att_id(self, att_id):
        for attack in self.GATTACKS_TABLE:
            if not is_deleted(attack) and attack.ATT_ID == att_id:
                return attack
        return None

    def fetch_source_immunities_by_unit_id(self, unit_id):
        summary = []
        for record in self.GIMMU_TABLE:
            if not is_deleted(record) and record.UNIT_ID == unit_id:
                summary.append(record)
        return summary

    def fetch_class_immunities_by_unit_id(self, unit_id):
        summary = []
        for record in self.GIMMUC_TABLE:
            if not is_deleted(record) and record.UNIT_ID == unit_id:
                summary.append(record)
        return summary

    def get_catalog_options(self, catalog):
        if catalog.lower() == 'subrace':
            return self.subrace_options
        if catalog.lower() == 'source':
            return self.attack_source_options
        if catalog.lower() == 'class':
            return self.attack_class_options
        if catalog.lower() == 'reach':
            return self.attack_reach_options
        if catalog.lower() == 'immunecat':
            return self.immunity_options
        return {}

    def get_catalog_id(self, catalog, text):
        return next((key for key, val in self.get_catalog_options(catalog).items() if val == text), None)

    def update_record(self, record, changes):
        with record:
            for key, value in changes.items():
                if value == '':
                    value = None
                setattr(record, key, value)

    def restore_original_state(self, table, current_record, original_record):
        with current_record:
            for field in table.field_names:
                setattr(current_record, field, getattr(original_record, field))

    def delete_record(self, record):
        dbf.delete(record)

    def add_record(self, table: dbf.Table, data: tuple):
        table.append(data=data)

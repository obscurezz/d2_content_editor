import dbf
import os
from dbf import is_deleted


class DatabaseManager:
    def __init__(self):
        self.GUNITS_TABLE = None
        self.GATTACKS_TABLE = None
        self.GIMMU_TABLE = None
        self.GIMMUC_TABLE = None
        self.GDYNUPGR_TABLE = None

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

    def open_databases(self, directory: str) -> bool:
        """
        :param directory: root directory for Dis2 game as string
        :return: nothing, just open the table in their mods
        """
        globals_dir = os.path.join(directory, 'Globals')
        if not os.path.exists(globals_dir):
            return False

        self.GUNITS_TABLE = self.open_database(globals_dir, 'gunits.dbf')
        self.GATTACKS_TABLE = self.open_database(globals_dir, 'gattacks.dbf')
        self.GIMMU_TABLE = self.open_database(globals_dir, 'gimmu.dbf')
        self.GIMMUC_TABLE = self.open_database(globals_dir, 'gimmuc.dbf')
        self.GDYNUPGR_TABLE = self.open_database(globals_dir, 'gdynupgr.dbf')
        self.LSUBRACE_TABLE = self.open_database(globals_dir, 'lsubrace.dbf')
        self.LATTS_TABLE = self.open_database(globals_dir, 'latts.dbf')
        self.LATTC_TABLE = self.open_database(globals_dir, 'lattc.dbf')
        self.LATTR_TABLE = self.open_database(globals_dir, 'lattr.dbf')
        self.LIMMUNE_TABLE = self.open_database(globals_dir, 'limmune.dbf')
        self.GMODIF_TABLE = self.open_database(globals_dir, 'gmodif.dbf')
        self.GUMODIF_TABLE = self.open_database(globals_dir, 'gumodif.dbf')

        self.subrace_options = {rec.ID: rec.TEXT for rec in self.LSUBRACE_TABLE if not is_deleted(rec)}
        self.attack_source_options = {rec.ID: rec.TEXT for rec in self.LATTS_TABLE if not is_deleted(rec)}
        self.attack_class_options = {rec.ID: rec.TEXT for rec in self.LATTC_TABLE if not is_deleted(rec)}
        self.attack_reach_options = {rec.ID: rec.TEXT for rec in self.LATTR_TABLE if not is_deleted(rec)}
        self.immunity_options = {rec.ID: rec.TEXT for rec in self.LIMMUNE_TABLE if not is_deleted(rec)}

        return True

    @staticmethod
    def open_database(directory: str, db_name: str) -> dbf.Table | None:
        for filename in os.listdir(directory):
            if filename.lower() == db_name.lower():
                filepath = os.path.join(directory, filename)
                if db_name.lower().startswith('g'):
                    return dbf.Table(filepath).open(dbf.READ_WRITE)
                if db_name.lower().startswith('l'):
                    return dbf.Table(filepath).open(dbf.READ_ONLY)
        return None

    @staticmethod
    def restore_original_state(table: dbf.Table, current_record: dbf.Record, original_record: dbf.Record):
        with current_record:
            for field in table.field_names:
                setattr(current_record, field, getattr(original_record, field))

    @staticmethod
    def delete_record(record: dbf.Record):
        dbf.delete(record)

    @staticmethod
    def add_record(table: dbf.Table, data: dict):
        table.append(data=data)

    @staticmethod
    def update_record(record: dbf.Record, changes: dict):
        with record:
            for key, value in changes.items():
                if value == '':
                    value = None
                setattr(record, key, value)

    @staticmethod
    def get_record_by_id(record_id: str, table: dbf.Table, id_column: str) -> dbf.Record | list[dbf.Record] | None:
        summary: list = []

        for record in table:
            if not is_deleted(record) and getattr(record, id_column) == record_id:
                summary.append(record)

        if len(summary) == 1:
            return summary[0]
        return summary

    def get_catalog_options(self, catalog: str) -> dict:
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

    def get_catalog_id(self, catalog: str, text: str) -> int | None:
        return next((key for key, val in self.get_catalog_options(catalog).items() if val == text), None)

    def close_tables(self):
        for t in self.__dict__:
            if isinstance(getattr(self, t), dbf.Table):
                calling = getattr(t, 'close')
                calling()

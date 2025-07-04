import dbf
import os


class DatabaseManager:
    def __init__(self):
        self.GUNITS_TABLE = None
        self.LSUBRACE_TABLE = None
        self.subrace_options = {}

    def open_databases(self, directory):
        # Искать файлы в вложенном каталоге Globals
        globals_dir = os.path.join(directory, 'Globals')
        if not os.path.exists(globals_dir):
            return False

        gunits_path = None
        lsubrace_path = None

        for filename in os.listdir(globals_dir):
            if filename.lower() == 'gunits.dbf':
                gunits_path = os.path.join(globals_dir, filename)
            elif filename.lower() == 'lsubrace.dbf':
                lsubrace_path = os.path.join(globals_dir, filename)

        if gunits_path:
            self.GUNITS_TABLE = dbf.Table(gunits_path)
            self.GUNITS_TABLE.open(mode=dbf.READ_WRITE)
        else:
            return False

        if lsubrace_path:
            self.LSUBRACE_TABLE = dbf.Table(lsubrace_path)
            self.LSUBRACE_TABLE.open(mode=dbf.READ_ONLY)
            self.subrace_options = {rec.ID: rec.TEXT for rec in self.LSUBRACE_TABLE}
        else:
            return False

        return True

    def fetch_record_by_unit_id(self, unit_id):
        for record in self.GUNITS_TABLE:
            if record.UNIT_ID == unit_id:
                return record
        return None

    def get_subrace_options(self):
        return self.subrace_options

    def get_subrace_id(self, text):
        return next((key for key, val in self.subrace_options.items() if val == text), None)

    def update_record(self, record, changes):
        with record:
            for key, value in changes.items():
                if value == '':
                    value = None
                setattr(record, key, value)

    def restore_original_state(self, current_record, original_record):
        with current_record:
            for field in current_record.fields:
                setattr(current_record, field.name, getattr(original_record, field.name))
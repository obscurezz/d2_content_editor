import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox

import dbf

import DatabaseManager
import settings


class AppInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('D2ContentEditor')
        self.geometry('1024x768')
        self.widgets = {}

        self.current_gunit = None
        self.original_gunit = None

        self.current_gattack_1 = None
        self.original_gattack_1 = None

        self.current_gattack_2 = None
        self.original_gattack_2 = None

        self.current_gattack_alt = None
        self.original_gattack_alt = None

        self.first_upgrade_widgets = {}
        self.second_upgrade_widgets = {}

        self.current_upgrade_1 = None
        self.original_upgrade_1 = None

        self.current_upgrade_2 = None
        self.original_upgrade_2 = None

        self.source_immunities_widgets = {}
        self.class_immunities_widgets = {}
        self.source_immunities = None
        self.class_immunities = None

        self.db_manager = DatabaseManager.DatabaseManager()

        self.create_ui()

    def create_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        """
        Top segment includes:
        1. Choosing directory entry and button
        2. Choosing unit ID entry and button
        """
        top_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))

        directory_label = tk.Label(top_segment, text='Absolute game path:', font=('Arial', 12))
        directory_label.pack(side='left', padx=10)
        self.directory_entry = tk.Entry(top_segment, width=50)
        self.directory_entry.pack(side='left', padx=10)

        select_dir_btn = tk.Button(top_segment, text='Choose the directory', command=self.select_directory)
        select_dir_btn.pack(side='left', padx=10)

        unit_id_label = tk.Label(top_segment, text='Unit ID:', font=('Arial', 12))
        unit_id_label.pack(side='left', padx=10)
        self.unit_id_entry = tk.Entry(top_segment, width=30)
        self.unit_id_entry.pack(side='left', padx=10)

        load_btn = tk.Button(top_segment, text='Load the record', command=self.load_and_show_record)
        load_btn.pack(side='left', padx=10)

        top_segment.pack(side=tk.TOP, fill='x')

        """
        Center segment includes:
        1. Main unit info from GUnits.dbf
        2. Attack1, attack2, alternative attack info from Gattacks.dbf
        3. Upgrade1, upgrade2 info from GDynUpgr.dbf
        4. Resistances info from Gimmu.dbf and GimmuC.dbf. Each immunity has its delete button.
        """
        center_segment = tk.Frame(main_frame)

        self.data_frame_left = tk.LabelFrame(center_segment, text="Main", relief='groove', borderwidth=1,
                                             width=int(self.winfo_width() * 0.166))
        self.data_frame_left.grid(row=0, column=0, sticky='nsew')

        self.data_frame_mid_1 = tk.LabelFrame(center_segment, text="Attack 1", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.166))
        self.data_frame_mid_1.grid(row=0, column=1, sticky='nsew')

        self.data_frame_mid_2 = tk.LabelFrame(center_segment, text="Attack 2", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.166))
        self.data_frame_mid_2.grid(row=0, column=2, sticky='nsew')

        self.data_frame_mid_3 = tk.LabelFrame(center_segment, text="Alternative attack", relief='groove',
                                              borderwidth=1, width=int(self.winfo_width() * 0.166))
        self.data_frame_mid_3.grid(row=0, column=3, sticky='nsew')

        self.data_frame_mid_4 = tk.LabelFrame(center_segment, text="Upgrades", relief='groove',
                                              borderwidth=1, width=int(self.winfo_width() * 0.166))
        self.data_frame_mid_4.grid(row=0, column=4, sticky='nsew')

        """
        These are inner frames of upgrades section, displaying upgrade1 and upgrade2
        """
        self.first_upgrade_frame = tk.LabelFrame(self.data_frame_mid_4, text="Upgrade 1", relief='groove',
                                                 borderwidth=1)
        self.first_upgrade_frame.grid(row=0, sticky='nsew', padx=10, pady=10)

        self.second_upgrade_frame = tk.LabelFrame(self.data_frame_mid_4, text="Upgrade 2", relief='groove',
                                                  borderwidth=1)
        self.second_upgrade_frame.grid(row=1, sticky='nsew', padx=10, pady=10)

        self.data_frame_right = tk.LabelFrame(center_segment, text="Resistances", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.166))
        self.data_frame_right.grid(row=0, column=5, sticky='nsew')

        """
        These are inner frames of resistances section, including buttons to add resistance and info frames
        """
        add_source_btn = tk.Button(self.data_frame_right, text="Add source resistance", height=1,
                                   command=lambda: self.open_add_window('SOURCE'))
        add_source_btn.grid(row=0, sticky='nsew', padx=10, pady=10)

        add_class_btn = tk.Button(self.data_frame_right, text="Add class resistance", height=1,
                                  command=lambda: self.open_add_window('CLASS'))
        add_class_btn.grid(row=1, sticky='nsew', padx=10, pady=10)

        self.immunity_source_frame = tk.LabelFrame(self.data_frame_right, text="Sources", relief='groove',
                                                   borderwidth=1)
        self.immunity_source_frame.grid(row=2, column=0, sticky='nsew')

        self.immunity_class_frame = tk.LabelFrame(self.data_frame_right, text="Classes", relief='groove', borderwidth=1)
        self.immunity_class_frame.grid(row=3, column=0, sticky='nsew')

        for row in (2, 3):
            self.data_frame_right.rowconfigure(row, weight=1)

        for col in range(6):
            center_segment.columnconfigure(col, uniform="1", weight=1)

        center_segment.pack(expand=True, fill='both')

        """
        Bottom segment includes:
        1. Commit button
        2. Cancel button
        3. Rollback button
        """
        bottom_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))

        apply_btn = tk.Button(bottom_segment, text='Commit changes', command=self.save_changes)
        apply_btn.pack(side='left', padx=10)

        cancel_btn = tk.Button(bottom_segment, text='Cancel changes', command=self.cancel_changes)
        cancel_btn.pack(side='left', padx=10)

        rollback_btn = tk.Button(bottom_segment, text='Rollback changes', command=self.rollback_changes)
        rollback_btn.pack(side='left', padx=10)

        bottom_segment.pack(side=tk.BOTTOM, fill='x')

    @staticmethod
    def destroy_widgets(frame: tk.Frame | tk.LabelFrame):
        for widget in frame.winfo_children():
            widget.destroy()

    @staticmethod
    def cleanup_widget_array(hash_table: dict):
        hash_table.clear()

    def open_add_window(self, immu_type: str):
        unit_id = self.unit_id_entry.get().strip()

        new_window = tk.Toplevel(master=self)
        new_window.title(f"Add {immu_type} record for {unit_id}")
        new_window.geometry("400x150")

        inner_widgets = {}

        for i in (0, 1):
            if i == 0:
                text = immu_type
            else:
                text = 'IMMUNECAT'
            names_array = self.db_manager.get_catalog_options(text)

            name_label = tk.Label(new_window, text=f'{text}: ')
            name_label.grid(row=i, column=0, sticky='e')

            name_var = tk.StringVar()
            names_widget = Combobox(new_window, values=list(names_array.values()), textvariable=name_var)
            names_widget.bind('<<ComboboxSelected>>', self.update_combobox_field())
            names_widget.grid(row=i, column=1, padx=(5, 10), sticky='we')

            inner_widgets[i] = (names_widget, name_var)

        apply_button = tk.Button(new_window, text="Apply", command=lambda: self.add_immunity(
            data={'UNIT_ID': unit_id,
                  'IMMUNITY': self.db_manager.get_catalog_id(immu_type, inner_widgets.get(0)[1].get()),
                  'IMMUNECAT': self.db_manager.get_catalog_id('IMMUNECAT', inner_widgets.get(1)[1].get())},
            immu_type=immu_type))
        apply_button.grid(row=4, column=0)
        cancel_button = tk.Button(new_window, text="Cancel", command=lambda: new_window.destroy())
        cancel_button.grid(row=4, column=1)

    def select_directory(self):
        directory = self.directory_entry.get().strip()
        if not directory:
            messagebox.showwarning(title='WARNING', message='You have to enter the game\'s absolute path.')
            return

        result = self.db_manager.open_databases(directory)
        if result:
            messagebox.showinfo(title='INFO', message='DBF files opened successfully.')
        else:
            messagebox.showerror(title='ERROR', message='Could not open DBF files.')

    def load_and_show_record(self):

        unit_id = self.unit_id_entry.get().strip()
        if not unit_id:
            messagebox.showwarning(title='WARNING', message='You have to enter unit ID.')
            return

        record = self.db_manager.fetch_record_by_unit_id(unit_id)
        if record:
            self.original_gunit = self.current_gunit
            self.current_gunit = record

            first_attack_id = getattr(record, 'ATTACK_ID')
            second_attack_id = getattr(record, 'ATTACK2_ID')

            first_attack = self.db_manager.fetch_attack_by_att_id(first_attack_id)
            second_attack = self.db_manager.fetch_attack_by_att_id(
                second_attack_id) if second_attack_id != 'g000000000' else None

            alternate_attack_id = getattr(first_attack, 'ALT_ATTACK')
            alternate_attack = self.db_manager.fetch_attack_by_att_id(
                alternate_attack_id) if alternate_attack_id != 'g000000000' else None

            first_upgrade_id = getattr(record, 'DYN_UPG1')
            second_upgrade_id = getattr(record, 'DYN_UPG2')

            first_upgrade = self.db_manager.fetch_upgrade_by_upg_id(first_upgrade_id)
            second_upgrade = self.db_manager.fetch_upgrade_by_upg_id(second_upgrade_id)

            self.original_upgrade_1 = self.current_upgrade_1
            self.current_upgrade_1 = first_upgrade

            self.original_upgrade_2 = self.current_upgrade_2
            self.current_upgrade_2 = second_upgrade

            # if first_attack:
            self.original_gattack_1 = self.current_gattack_1
            self.current_gattack_1 = first_attack

            # if second_attack:
            self.original_gattack_2 = self.current_gattack_2
            self.current_gattack_2 = second_attack

            # if alternate_attack:
            self.original_gattack_alt = self.current_gattack_alt
            self.current_gattack_alt = alternate_attack

            self.source_immunities = self.db_manager.fetch_source_immunities_by_unit_id(unit_id)
            self.class_immunities = self.db_manager.fetch_class_immunities_by_unit_id(unit_id)

            for t in (self.widgets, self.first_upgrade_widgets, self.second_upgrade_widgets,
                      self.source_immunities_widgets, self.class_immunities_widgets):
                self.cleanup_widget_array(t)

            for f in (self.data_frame_left, self.data_frame_mid_1, self.data_frame_mid_2, self.data_frame_mid_3,
                      self.first_upgrade_frame, self.second_upgrade_frame, self.immunity_source_frame,
                      self.immunity_class_frame):
                self.destroy_widgets(f)

            self.cancel_changes()
        else:
            messagebox.showerror(title='ERROR', message=f'The record UNIT_ID={unit_id} was not found.')

    def display_fields(self):
        for fields_frame in [self.data_frame_left, self.data_frame_mid_1, self.data_frame_mid_2, self.data_frame_mid_3]:
            self.widgets[fields_frame] = {}
            visible = []
            record = None
            table = None
            if fields_frame == self.data_frame_left:
                visible = settings.VISIBLE_FIELDS_GUNITS
                record = self.current_gunit
                table = self.db_manager.GUNITS_TABLE
            if fields_frame == self.data_frame_mid_1:
                visible = settings.VISIBLE_FIELDS_GATTACKS
                record = self.current_gattack_1
                table = self.db_manager.GATTACKS_TABLE
            if fields_frame == self.data_frame_mid_2:
                visible = settings.VISIBLE_FIELDS_GATTACKS
                record = self.current_gattack_2
                table = self.db_manager.GATTACKS_TABLE
            if fields_frame == self.data_frame_mid_3:
                visible = settings.VISIBLE_FIELDS_GATTACKS
                record = self.current_gattack_alt
                table = self.db_manager.GATTACKS_TABLE

            if record:
                for idx, field in enumerate(visible):
                    label_text = field + ': '
                    field_code = table.field_info(field)[0]
                    widget_type = settings.FIELD_TYPES.get(field_code, {'widget': 'Entry'})

                    label = tk.Label(fields_frame, text=label_text)
                    label.grid(row=idx, column=0, sticky='e')

                    value = getattr(record, field)

                    if field in ('SUBRACE', 'SOURCE', 'CLASS', 'REACH'):
                        catalog_options = self.db_manager.get_catalog_options(field)
                        var = tk.StringVar(value=catalog_options.get(value, ''))
                        widget = Combobox(fields_frame, values=list(catalog_options.values()), textvariable=var)
                        widget.bind('<<ComboboxSelected>>', self.update_combobox_field)
                        self.widgets[fields_frame][field] = (widget, var)
                    elif widget_type['widget'] == 'Checkbutton':
                        var = tk.BooleanVar(value=value)
                        widget = tk.Checkbutton(fields_frame, variable=var)
                        self.widgets[fields_frame][field] = (widget, var)
                    elif widget_type['widget'] == 'Spinbox':
                        var = tk.IntVar(value=value)
                        widget = tk.Spinbox(fields_frame, from_=-999999, to=999999, textvariable=var)
                        self.widgets[fields_frame][field] = (widget, var)
                    else:
                        var = tk.StringVar(value=value)
                        widget = tk.Entry(fields_frame, textvariable=var)
                        if idx == 0:
                            widget.configure(state='readonly')
                        self.widgets[fields_frame][field] = (widget, var)

                    widget.grid(row=idx, column=1, padx=(5, 10), sticky='we')

    def display_immunities(self, immu_type: str):
        if immu_type == 'SOURCE':
            frame = self.immunity_source_frame
            records = self.source_immunities
            widgets = self.source_immunities_widgets
        elif immu_type == 'CLASS':
            frame = self.immunity_class_frame
            records = self.class_immunities
            widgets = self.class_immunities_widgets
        else:
            return

        if records:
            for x, record in enumerate(records):
                self.immunity_frame = tk.LabelFrame(frame, text=f"{immu_type} {str(x + 1)}", relief='groove',
                                                    borderwidth=1)
                self.immunity_frame.grid(row=x, column=0, sticky='nsew')
                for idx, field in enumerate(['IMMUNITY', 'IMMUNECAT']):
                    label_text = field + ': '

                    label = tk.Label(self.immunity_frame, text=label_text)
                    label.grid(row=idx, column=0, sticky='e')

                    value = getattr(record, field)

                    if field == 'IMMUNITY':
                        catalog_options = self.db_manager.get_catalog_options(immu_type)
                    else:
                        catalog_options = self.db_manager.get_catalog_options(field)

                    widget = tk.Entry(self.immunity_frame)
                    widget.insert(0, catalog_options.get(value, '') or '')
                    widgets[field] = widget

                    widget.grid(row=idx, column=1, padx=(5, 10), sticky='we')
                delete_btn = tk.Button(self.immunity_frame, text='Delete',
                                       command=lambda i=x: self.delete_immunity(records[i], immu_type))
                delete_btn.grid(row=4)

    def display_upgrades(self, upgrade: str):
        table = self.db_manager.GDYNUPGR_TABLE
        if upgrade == 'UPGRADE1':
            frame = self.first_upgrade_frame
            widgets = self.first_upgrade_widgets
            record = self.current_upgrade_1
        elif upgrade == 'UPGRADE2':
            frame = self.second_upgrade_frame
            widgets = self.second_upgrade_widgets
            record = self.current_upgrade_2
        else:
            return

        if record:
            for idx, field in enumerate(settings.VISIBLE_FIELDS_GDYNUPGR):
                label_text = field + ': '
                field_code = table.field_info(field)[0]
                widget_type = settings.FIELD_TYPES.get(field_code, {'widget': 'Entry'})

                label = tk.Label(frame, text=label_text)
                label.grid(row=idx, column=0, sticky='e')

                value = getattr(record, field)

                if widget_type['widget'] == 'Checkbutton':
                    var = tk.BooleanVar(value=value)
                    widget = tk.Checkbutton(frame, variable=var)
                    widgets[field] = (widget, var)
                elif widget_type['widget'] == 'Spinbox':
                    var = tk.IntVar(value=value)
                    widget = tk.Spinbox(frame, from_=-999999, to=999999, textvariable=var)
                    widgets[field] = (widget, var)
                else:
                    var = tk.StringVar(value=value)
                    widget = tk.Entry(frame, textvariable=var)
                    if idx == 0:
                        widget.configure(state='readonly')
                    widgets[field] = (widget, var)

                widget.grid(row=idx, column=1, padx=(5, 10), sticky='we')

    def update_combobox_field(self, event=None):
        pass

    def save_changes(self):
        for frame, frame_data in self.widgets.items():
            changes = {}
            for field_name, widget in frame_data.items():
                if isinstance(widget, tuple):
                    if isinstance(widget[0], Combobox):
                        changes[field_name] = self.db_manager.get_catalog_id(field_name, widget[0].get())
                    else:
                        _, bool_var = widget
                        changes[field_name] = bool_var.get()
                else:
                    changes[field_name] = widget.get()

            if frame == self.data_frame_left and self.current_gunit:
                self.db_manager.update_record(self.current_gunit, changes)
            if frame == self.data_frame_mid_1 and self.current_gattack_1:
                self.db_manager.update_record(self.current_gattack_1, changes)
            if frame == self.data_frame_mid_2 and self.current_gattack_2:
                self.db_manager.update_record(self.current_gattack_2, changes)
            if frame == self.data_frame_mid_3 and self.current_gattack_alt:
                self.db_manager.update_record(self.current_gattack_alt, changes)

        for u in [self.first_upgrade_widgets, self.second_upgrade_widgets]:
            changes = {}
            for field_name, widget in u.items():
                if isinstance(widget, tuple):
                    _, bool_var = widget
                    changes[field_name] = bool_var.get()
                else:
                    changes[field_name] = widget.get()

            if u == self.first_upgrade_widgets and self.current_upgrade_1:
                self.db_manager.update_record(self.current_upgrade_1, changes)
            if u == self.second_upgrade_frame and self.current_upgrade_2:
                self.db_manager.update_record(self.current_upgrade_2, changes)

        messagebox.showinfo(title='INFO', message='Data saved successfully.')

    def cancel_changes(self):
        self.display_fields()
        self.display_upgrades('UPGRADE1')
        self.display_upgrades('UPGRADE2')
        self.display_immunities('SOURCE')
        self.display_immunities('CLASS')

    def rollback_changes(self):
        tables_rollbacked = 0
        if self.current_gunit != self.original_gunit:
            self.db_manager.restore_original_state(table=self.db_manager.GUNITS_TABLE,
                                                   current_record=self.current_gunit,
                                                   original_record=self.original_gunit)
            tables_rollbacked += 1
        if self.current_gattack_1 != self.original_gattack_1:
            self.db_manager.restore_original_state(table=self.db_manager.GATTACKS_TABLE,
                                                   current_record=self.current_gattack_1,
                                                   original_record=self.original_gattack_1)
            tables_rollbacked += 1
        if self.current_gattack_2 != self.original_gattack_2:
            self.db_manager.restore_original_state(table=self.db_manager.GATTACKS_TABLE,
                                                   current_record=self.current_gattack_2,
                                                   original_record=self.original_gattack_2)
            tables_rollbacked += 1
        if self.current_gattack_alt != self.original_gattack_alt:
            self.db_manager.restore_original_state(table=self.db_manager.GATTACKS_TABLE,
                                                   current_record=self.current_gattack_alt,
                                                   original_record=self.original_gattack_alt)
            tables_rollbacked += 1

        if tables_rollbacked > 0:
            messagebox.showinfo(title='INFO', message='Rollback completed successfully.')
        else:
            messagebox.showinfo(title='INFO', message='Nothing to rollback.')

    def delete_immunity(self, record: dbf.Record, immu_type: str):
        self.db_manager.delete_record(record)

        text_list = []
        for item in record:
            text_list.append(str(item))
        text = ' '.join(text_list)
        messagebox.showinfo(title='INFO', message=f'Immunity "{text}" with type {immu_type} has been deleted.')

    def add_immunity(self, data: dict, immu_type: str):
        table = None
        if immu_type == 'SOURCE':
            table = self.db_manager.GIMMU_TABLE
        if immu_type == 'CLASS':
            table = self.db_manager.GIMMUC_TABLE

        self.db_manager.add_record(table=table, data=data)

        text_list = []
        for item in data.values():
            text_list.append(str(item))
        text = ' '.join(text_list)
        messagebox.showinfo(title='INFO', message=f'Immunity "{text}" with type {immu_type} has been added.')

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
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

        self.source_immunities_widgets = {}
        self.class_immunities_widgets = {}
        self.source_immunities = None
        self.class_immunities = None

        self.db_manager = DatabaseManager.DatabaseManager()

        self.create_ui()

    def create_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        # Верхний сегмент (примерно 10%) - панель ввода
        top_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))

        # Директория
        directory_label = tk.Label(top_segment, text='Absolute game path:', font=('Arial', 12))
        directory_label.pack(side='left', padx=10)
        self.directory_entry = tk.Entry(top_segment, width=50)
        self.directory_entry.pack(side='left', padx=10)

        # Кнопка "Выбрать директорию"
        select_dir_btn = tk.Button(top_segment, text='Choose the directory', command=self.select_directory)
        select_dir_btn.pack(side='left', padx=10)

        # ID
        unit_id_label = tk.Label(top_segment, text='Unit ID:', font=('Arial', 12))
        unit_id_label.pack(side='left', padx=10)
        self.unit_id_entry = tk.Entry(top_segment, width=30)
        self.unit_id_entry.pack(side='left', padx=10)

        # Кнопка "Загрузить запись"
        load_btn = tk.Button(top_segment, text='Load the record', command=self.load_and_show_record)
        load_btn.pack(side='left', padx=10)

        top_segment.pack(side=tk.TOP, fill='x')

        # Центральный сегмент (примерно 80%) - зона отображения данных
        center_segment = tk.Frame(main_frame)

        # Левая колонка
        self.data_frame_left = tk.LabelFrame(center_segment, text="Main", relief='groove', borderwidth=1,
                                             width=int(self.winfo_width() * 0.2))
        self.data_frame_left.grid(row=0, column=0, sticky='nsew')

        # Центральная колонка 1
        self.data_frame_mid_1 = tk.LabelFrame(center_segment, text="Attack 1", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.2))
        self.data_frame_mid_1.grid(row=0, column=1, sticky='nsew')

        # Центральная колонка 2
        self.data_frame_mid_2 = tk.LabelFrame(center_segment, text="Attack 2", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.2))
        self.data_frame_mid_2.grid(row=0, column=2, sticky='nsew')

        # Центральная колонка 2
        self.data_frame_mid_3 = tk.LabelFrame(center_segment, text="Alternative attack", relief='groove',
                                              borderwidth=1, width=int(self.winfo_width() * 0.2))
        self.data_frame_mid_3.grid(row=0, column=3, sticky='nsew')

        # Правая колонка
        self.data_frame_right = tk.LabelFrame(center_segment, text="Resistances", relief='groove', borderwidth=1,
                                              width=int(self.winfo_width() * 0.2))
        self.data_frame_right.grid(row=0, column=4, sticky='nsew')

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

        for col in range(5):
            center_segment.columnconfigure(col, uniform="1", weight=1)

        center_segment.pack(expand=True, fill='both')

        # Нижний сегмент (примерно 10%) - панель управления
        bottom_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))

        # Кнопка "Применить изменения"
        apply_btn = tk.Button(bottom_segment, text='Commit changes', command=self.save_changes)
        apply_btn.pack(side='left', padx=10)

        # Кнопка "Отменить изменения"
        cancel_btn = tk.Button(bottom_segment, text='Cancel changes', command=self.cancel_changes)
        cancel_btn.pack(side='left', padx=10)

        # Кнопка "Откатить изменения"
        rollback_btn = tk.Button(bottom_segment, text='Rollback changes', command=self.rollback_changes)
        rollback_btn.pack(side='left', padx=10)

        bottom_segment.pack(side=tk.BOTTOM, fill='x')

    def open_add_window(self, immu_type):
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

    def destroy_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def cleanup_widget_array(self, hash_table):
        hash_table.clear()

    def load_and_show_record(self):

        unit_id = self.unit_id_entry.get().strip()
        if not unit_id:
            messagebox.showwarning(title='WARNING', message='You have to enter unit ID.')
            return

        record = self.db_manager.fetch_record_by_unit_id(unit_id)
        if record:
            self.original_gunit = self.current_gunit
            self.current_gunit = record

            # Загрузка данных атак
            first_attack_id = getattr(record, 'ATTACK_ID')
            second_attack_id = getattr(record, 'ATTACK2_ID')

            first_attack = self.db_manager.fetch_attack_by_att_id(first_attack_id)
            second_attack = self.db_manager.fetch_attack_by_att_id(
                second_attack_id) if second_attack_id != 'g000000000' else None

            alternate_attack_id = getattr(first_attack, 'ALT_ATTACK')
            alternate_attack = self.db_manager.fetch_attack_by_att_id(
                alternate_attack_id) if alternate_attack_id != 'g000000000' else None

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

            for t in (self.widgets, self.source_immunities_widgets, self.class_immunities_widgets):
                self.cleanup_widget_array(t)

            for f in (self.data_frame_left, self.data_frame_mid_1, self.data_frame_mid_2, self.data_frame_mid_3,
                      self.immunity_source_frame, self.immunity_class_frame):
                self.destroy_widgets(f)

            self.display_fields()
            self.display_immunities('SOURCE')
            self.display_immunities('CLASS')
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
                        self.widgets[fields_frame][field] = (widget, var)

                    widget.grid(row=idx, column=1, padx=(5, 10), sticky='we')

    def display_immunities(self, immu_type):
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
                for idx, field in enumerate(self.db_manager.GIMMU_TABLE.field_names):
                    if field == 'UNIT_ID':
                        pass
                    else:
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

        messagebox.showinfo(title='INFO', message='Data saved successfully.')

    def cancel_changes(self):
        self.display_fields()
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

    def delete_immunity(self, record, immu_type):
        self.db_manager.delete_record(record)

        text_list = []
        for item in record:
            text_list.append(str(item))
        text = ' '.join(text_list)
        messagebox.showinfo(title='INFO', message=f'Immunity "{text}" with type {immu_type} has been deleted.')

    def add_immunity(self, data, immu_type):
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

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
        self.db_manager = DatabaseManager.DatabaseManager()

        self.create_ui()

    def create_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        # Верхний сегмент (примерно 10%) - панель ввода
        top_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))
        top_segment.configure(background='lightgreen')

        # Директория
        directory_label = tk.Label(top_segment, text='Путь к родительскому каталогу:', font=('Arial', 12))
        directory_label.pack(side='left', padx=10)
        self.directory_entry = tk.Entry(top_segment, width=50)
        self.directory_entry.pack(side='left', padx=10)

        # Кнопка "Выбрать директорию"
        select_dir_btn = tk.Button(top_segment, text='Выбрать директорию', command=self.select_directory)
        select_dir_btn.pack(side='left', padx=10)

        # ID
        unit_id_label = tk.Label(top_segment, text='ID единицы (UNIT_ID)', font=('Arial', 12))
        unit_id_label.pack(side='left', padx=10)
        self.unit_id_entry = tk.Entry(top_segment, width=30)
        self.unit_id_entry.pack(side='left', padx=10)

        # Кнопка "Загрузить запись"
        load_btn = tk.Button(top_segment, text='Загрузить запись', command=self.load_and_show_record)
        load_btn.pack(side='left', padx=10)

        top_segment.pack(side=tk.TOP, fill='x')

        # Центральный сегмент (примерно 80%) - зона отображения данных
        center_segment = tk.Frame(main_frame)
        center_segment.configure(background='lightblue')

        # Левая колонка
        self.data_frame_left = tk.LabelFrame(center_segment, text="Общее", relief='groove', borderwidth=1)
        self.data_frame_left.grid(row=0, column=0, sticky='nsew')

        # Центральная колонка 1
        self.data_frame_mid_1 = tk.LabelFrame(center_segment, text="Атака 1", relief='groove', borderwidth=1)
        self.data_frame_mid_1.grid(row=0, column=1, sticky='nsew')

        # Центральная колонка 2
        self.data_frame_mid_2 = tk.LabelFrame(center_segment, text="Атака 2", relief='groove', borderwidth=1)
        self.data_frame_mid_2.grid(row=0, column=2, sticky='nsew')

        # Центральная колонка 2
        self.data_frame_mid_3 = tk.LabelFrame(center_segment, text="Альтернативная атака", relief='groove', borderwidth=1)
        self.data_frame_mid_3.grid(row=0, column=3, sticky='nsew')

        # Правая колонка (пока пустая)
        self.data_frame_right = tk.LabelFrame(center_segment, text="Защита", relief='groove', borderwidth=1)
        self.data_frame_right.grid(row=0, column=4, sticky='nsew')

        for col in range(5):
            center_segment.columnconfigure(col, weight=1)

        center_segment.pack(expand=True, fill='both')

        # Нижний сегмент (примерно 10%) - панель управления
        bottom_segment = tk.Frame(main_frame, height=int(self.winfo_screenheight() * 0.1))
        bottom_segment.configure(background='lightgray')

        # Кнопка "Применить изменения"
        apply_btn = tk.Button(bottom_segment, text='Применить изменения', command=self.save_changes)
        apply_btn.pack(side='left', padx=10)

        # Кнопка "Отменить изменения"
        cancel_btn = tk.Button(bottom_segment, text='Отменить изменения', command=self.cancel_changes)
        cancel_btn.pack(side='left', padx=10)

        # Кнопка "Откатить изменения"
        rollback_btn = tk.Button(bottom_segment, text='Откатить изменения', command=self.rollback_changes)
        rollback_btn.pack(side='left', padx=10)

        bottom_segment.pack(side=tk.BOTTOM, fill='x')

    def select_directory(self):
        directory = self.directory_entry.get().strip()
        if not directory:
            messagebox.showwarning('Внимание!', 'Необходимо указать путь к каталогу!')
            return

        result = self.db_manager.open_databases(directory)
        if result:
            messagebox.showinfo('Успех!', 'Базы данных открыты успешно.')
        else:
            messagebox.showerror('Ошибка!', 'Не удалось открыть базы данных.')

    def load_and_show_record(self):
        unit_id = self.unit_id_entry.get().strip()
        if not unit_id:
            messagebox.showwarning('Внимание!', 'Необходимо ввести ID единицы!')
            return

        record = self.db_manager.fetch_record_by_unit_id(unit_id)
        if record:
            self.current_gunit = record
            self.original_gunit = self.current_gunit

            # Загрузка данных атак
            first_attack_id = getattr(record, 'ATTACK_ID')
            second_attack_id = getattr(record, 'ATTACK2_ID')

            first_attack = self.db_manager.fetch_attack_by_att_id(first_attack_id)
            second_attack = self.db_manager.fetch_attack_by_att_id(
                second_attack_id) if second_attack_id != 'g000000000' else None

            alternate_attack_id = getattr(first_attack, 'ALT_ATTACK')
            alternate_attack = self.db_manager.fetch_attack_by_att_id(alternate_attack_id) if alternate_attack_id != 'g000000000' else None

            if first_attack:
                self.current_gattack_1 = first_attack
                self.original_gattack_1 = self.current_gattack_1

            if second_attack:
                self.current_gattack_2 = second_attack
                self.original_gattack_2 = self.current_gattack_2

            if alternate_attack:
                self.current_gattack_alt = alternate_attack
                self.original_gattack_alt = self.current_gattack_alt

            self.display_fields()
        else:
            messagebox.showerror('Ошибка!', f'Запись с UNIT_ID={unit_id} не найдена.')

    def display_fields(self):
        self.widgets.clear()
        for fields_frame in [self.data_frame_left, self.data_frame_mid_1, self.data_frame_mid_2, self.data_frame_mid_3, self.data_frame_right]:
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
                        widget = tk.Spinbox(fields_frame, from_=-999999, to=999999)
                        widget.delete(0, tk.END)
                        widget.insert(0, value or '')
                        self.widgets[fields_frame][field] = widget
                    else:
                        widget = tk.Entry(fields_frame)
                        widget.insert(0, value or '')
                        self.widgets[fields_frame][field] = widget

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

        messagebox.showinfo('Успех!', 'Данные успешно сохранены!')

    def cancel_changes(self):
        self.display_fields()

    def rollback_changes(self):
        if self.current_record != self.original_record:
            self.db_manager.restore_original_state(self.current_record, self.original_record)
            messagebox.showinfo('Успех!', 'Изменения отменены и запись восстановлена.')
        else:
            messagebox.showinfo('Информирование', 'Нет изменений для отката.')

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import DatabaseManager
import settings


class AppInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Редактирование записей GUnits.dbf')
        self.geometry('800x600')
        self.widgets = {}
        self.current_record = None
        self.original_record = None
        self.db_manager = DatabaseManager.DatabaseManager()

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, fill='both')

        # Верхняя панель
        top_panel = tk.Frame(frame)
        top_panel.pack(side='top', anchor='w', pady=10)

        # Вход для директории
        directory_label = tk.Label(top_panel, text='Путь к родительскому каталогу:', font=('Arial', 12))
        directory_label.pack(side='left')
        self.directory_entry = tk.Entry(top_panel, width=50)
        self.directory_entry.pack(side='left', padx=10)

        # Кнопка "Выбрать директорию"
        select_dir_btn = tk.Button(top_panel, text='Выбрать директорию', command=self.select_directory)
        select_dir_btn.pack(side='left', padx=10)

        # Средняя панель
        middle_panel = tk.Frame(frame)
        middle_panel.pack(side='top', anchor='w', pady=10)

        # Вход для ID
        unit_id_label = tk.Label(middle_panel, text='ID единицы (UNIT_ID)', font=('Arial', 12))
        unit_id_label.pack(side='left')
        self.unit_id_entry = tk.Entry(middle_panel, width=30)
        self.unit_id_entry.pack(side='left', padx=10)

        # Кнопка "Загрузить запись"
        load_btn = tk.Button(middle_panel, text='Загрузить запись', command=self.load_and_show_record)
        load_btn.pack(side='left', padx=10)

        # Нижняя панель (переносим в нижний левый угол)
        bottom_panel = tk.Frame(frame)
        bottom_panel.pack(side='bottom', anchor='sw', pady=10)

        # Кнопка "Применить изменения"
        apply_btn = tk.Button(bottom_panel, text='Применить изменения', command=self.save_changes)
        apply_btn.pack(side='left', padx=10)

        # Кнопка "Отменить изменения"
        cancel_btn = tk.Button(bottom_panel, text='Отменить изменения', command=self.cancel_changes)
        cancel_btn.pack(side='left', padx=10)

        # Кнопка "Откатить изменения"
        rollback_btn = tk.Button(bottom_panel, text='Откатить изменения', command=self.rollback_changes)
        rollback_btn.pack(side='left', padx=10)

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
            # Здесь просто сохраним ссылку на оригинальную запись
            self.original_record = record
            self.current_record = record
            # Сохраняем оригинальную запись
            self.display_fields()
        else:
            messagebox.showerror('Ошибка!', f'Запись с UNIT_ID={unit_id} не найдена.')

    def display_fields(self):
        fields_frame = tk.Frame(self)
        fields_frame.pack(expand=True, fill='both')
        self.widgets.clear()

        for idx, field in enumerate(settings.VISIBLE_FIELDS):
            label_text = field + ': '
            field_code = type(getattr(self.current_record, field)).__name__
            widget_type = settings.FIELD_TYPES.get(field_code, {'widget': 'Entry'})
            # widget_class = eval(widget_type['widget'])

            label = tk.Label(fields_frame, text=label_text)
            label.grid(row=idx, column=0, sticky='e')

            value = getattr(self.current_record, field)

            if field == 'SUBRACE':
                # Специальная обработка для поля SUBRACE
                subrace_options = self.db_manager.get_subrace_options()
                var = tk.StringVar(value=subrace_options.get(value, ''))
                widget = Combobox(fields_frame, values=list(subrace_options.values()), textvariable=var)
                widget.config(textvariable=var)
                widget.bind('<<ComboboxSelected>>', self.update_subrace_field)
                self.widgets[field] = (widget, var)
            elif widget_type['widget'] == 'Checkbutton':
                var = tk.BooleanVar(value=value)
                widget = tk.Checkbutton(fields_frame, variable=var)
                self.widgets[field] = (widget, var)
            elif widget_type['widget'] == 'Spinbox':
                widget = tk.Spinbox(fields_frame, from_=-999999, to=999999)
                widget.delete(0, tk.END)
                widget.insert(0, value or '')
                self.widgets[field] = widget
            else:
                widget = tk.Entry(fields_frame)
                widget.insert(0, value or '')
                self.widgets[field] = widget

            widget.grid(row=idx, column=1, padx=(5, 10), sticky='we')

    def update_subrace_field(self, event=None):
        # selection = self.widgets['SUBRACE'][0].get()
        # if selection:
        #     subrace_id = self.db_manager.get_subrace_id(selection)
        #     if subrace_id:
        #         self.current_record.SUBRACE = subrace_id
        pass

    def save_changes(self):
        changes = {}
        for field_name, widget in self.widgets.items():
            if isinstance(widget, tuple):  # Логическое поле или Combobox
                if isinstance(widget[0], Combobox):
                    changes[field_name] = self.db_manager.get_subrace_id(widget[0].get())
                else:
                    _, bool_var = widget
                    changes[field_name] = bool_var.get()
            else:
                changes[field_name] = widget.get()

        self.db_manager.update_record(self.current_record, changes)
        messagebox.showinfo('Успех!', 'Данные успешно сохранены!')

    def cancel_changes(self):
        self.display_fields()

    def rollback_changes(self):
        if self.current_record != self.original_record:
            self.db_manager.restore_original_state(self.current_record, self.original_record)
            messagebox.showinfo('Успех!', 'Изменения отменены и запись восстановлена.')
        else:
            messagebox.showinfo('Информирование', 'Нет изменений для отката.')

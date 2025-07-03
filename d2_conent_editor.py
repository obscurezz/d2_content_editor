import os
from tkinter import *
from tkinter.messagebox import showinfo
import dbf

# Глобальная переменная для таблицы GUnits.dbf
GUNITS_TABLE = None

# Массив полей, доступных для редактирования пользователем
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

# Типы полей и соответствующие типы виджетов
FIELD_TYPES = {
    67: {'widget': Entry},  # C - Character (строка)
    78: {'widget': Spinbox},  # N - Numeric (число)
    76: {'widget': Checkbutton}  # L - Logical (булевый)
}


def open_gunits_table(globals_dir):
    """Открывает таблицу GUnits.dbf в режиме чтения-записи."""
    global GUNITS_TABLE
    gunits_path = None

    for filename in os.listdir(globals_dir):
        if filename.lower() == 'gunits.dbf':
            gunits_path = os.path.join(globals_dir, filename)
            break

    if gunits_path:
        GUNITS_TABLE = dbf.Table(gunits_path)
        GUNITS_TABLE.open(mode=dbf.READ_WRITE)  # Открываем таблицу в режиме чтения-записи
        print(f'Файл GUnits.dbf открыт в режиме rw: {gunits_path}')
    else:
        raise FileNotFoundError('Файл GUnits.dbf не найден.')


def load_and_show_record(unit_id_entry):
    unit_id = unit_id_entry.get().strip()
    if not unit_id:
        showinfo('Ошибка', 'Необходимо ввести ID единицы!')
        return

    global current_record
    try:
        # Поиск записи по UNIT_ID
        records = [rec for rec in GUNITS_TABLE if rec['UNIT_ID'] == unit_id]

        if len(records) > 0:
            current_record = records[0]
            display_fields(current_record, GUNITS_TABLE)  # Передаем таблицу в функцию
        else:
            showinfo('Ошибка', f'Запись с UNIT_ID={unit_id} не найдена.')
    except Exception as e:
        showinfo('Ошибка', str(e))


def display_fields(record, table):
    clear_fields_frame()

    fields_frame.grid(row=1, columnspan=2)
    widgets.clear()

    # Перебираем только интересующие нас поля
    for idx, field in enumerate(VISIBLE_FIELDS):
        label_text = field + ': '
        field_code = table.field_info(field)[0]  # Получаем внутренний код типа поля
        widget_type = FIELD_TYPES.get(field_code, {'widget': Entry})['widget']

        label = Label(fields_frame, text=label_text)
        label.grid(row=idx, column=0, sticky=E)

        value = getattr(record, field)

        if widget_type == Checkbutton:
            var = BooleanVar(value=value)
            widget = Checkbutton(fields_frame, variable=var)
            widgets[field] = (widget, var)
        elif widget_type == Spinbox:
            widget = Spinbox(fields_frame, from_=-999999, to=999999)
            widget.delete(0, END)
            widget.insert(0, value or '')
            widgets[field] = widget
        else:
            widget = Entry(fields_frame)
            widget.insert(0, value or '')
            widgets[field] = widget

        widget.grid(row=idx, column=1, padx=(5, 10), sticky=W + E)


def save_changes():
    global current_record
    changes = {}

    for field_name, widget in widgets.items():
        if isinstance(widget, tuple):  # Логическое поле
            _, bool_var = widget
            changes[field_name] = bool_var.get()
        else:
            changes[field_name] = widget.get()

    # Применяем изменения к записи
    with current_record:
        for key, value in changes.items():
            if value == '':
                value = None
            setattr(current_record, key, value)

    showinfo('Информация', 'Данные успешно сохранены!')


def rollback_changes(table):
    display_fields(current_record, table)  # Передаем таблицу в функцию


def clear_fields_frame():
    for child in fields_frame.winfo_children():
        child.destroy()


# Основная форма
root = Tk()
root.title('Редактирование записей GUnits.dbf')
fields_frame = Frame(root)
widgets = {}
current_record = None


def select_directory():
    global current_gunits_path
    root_dir = entry.get()
    globals_dir = None

    # Регистронезависимый поиск каталога Globals
    for dir_name in os.listdir(root_dir):
        if dir_name.lower() == 'globals':
            globals_dir = os.path.join(root_dir, dir_name)
            break

    if globals_dir:
        try:
            open_gunits_table(globals_dir)  # Пробуем открыть таблицу
        except FileNotFoundError as e:
            print(str(e))
    else:
        print('Каталог Globals не найден.')


# Интерфейс
Label(root, text='Путь к родительскому каталогу:').grid(row=0, column=0, sticky=W)
entry = Entry(root, width=50)
entry.grid(row=0, column=1, pady=10)

Button(root, text='Выбрать директорию', command=select_directory).grid(row=0, column=2, pady=10)

unit_id_label = Label(root, text='ID единицы (UNIT_ID)')
unit_id_label.grid(row=2, column=0, sticky=W)

unit_id_entry = Entry(root)
unit_id_entry.grid(row=2, column=1, pady=10)

search_button = Button(root, text='Загрузить запись', command=lambda: load_and_show_record(unit_id_entry))
search_button.grid(row=2, column=2, pady=10)

save_button = Button(root, text='Применить изменения', command=save_changes)
save_button.grid(row=3, column=1, pady=10)

rollback_button = Button(root, text='Откатить изменения', command=lambda: rollback_changes(GUNITS_TABLE))
rollback_button.grid(row=3, column=2, pady=10)

root.mainloop()

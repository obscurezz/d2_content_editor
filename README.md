# d2_content_editor

### To compile

1. Clone repo with `git clone`

2. Create venv in the local repo with `python -m venv <path>`

3. Install requirements with `pip install -r requirements.txt`

4. Install nuitka with `pip install nuitka`

5. Compile your exe with `nuitka --onefile  --enable-plugin=tk-inter --quiet main.py`

### Download here

https://github.com/obscurezz/d2_content_editor/releases/

## Features

> Now we can add and delete unit resistances (still have to reload unit by its id to change the frames)

> All the values of sources, classes and reaches are binded on their catalogues and available to change

> Added dynamic upgrades section

## BUGS

> rollback still doesn't work - need to find a way how to get field names from Record object


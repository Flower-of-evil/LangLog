from . import db

VALID_LEVELS = ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')


def add_new_language():
    print("\n--- Добавление языка ---")
    name = input("Название языка: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым")
        return None

    print("Уровни: A1, A2, B1, B2, C1, C2")
    level = input("Уровень: ").strip().upper()
    if level not in VALID_LEVELS:
        print("Ошибка: неверный уровень")
        return None

    goal = input("Цель изучения: ").strip()

    lang_id = db.add_language(name, level, goal)
    print(f"Язык '{name}' добавлен с ID {lang_id}")
    return lang_id


def list_languages():
    langs = db.get_all_languages()
    if not langs:
        print("Нет добавленных языков")
        return

    print("\n--- Ваши языки ---")
    for lang in langs:
        print(f"{lang['id']}. {lang['name']} ({lang['level']}) — {lang['goal']}")

    return langs


def choose_language(prompt="Выберите ID языка: "):
    langs = db.get_all_languages()
    if not langs:
        print("Сначала добавьте язык")
        return None
    list_languages()
    try:
        lang_id = int(input(prompt))
        if any(l['id'] == lang_id for l in langs):
            return lang_id
        else:
            print("Неверный ID")
            return None
    except ValueError:
        print("Введите число")
        return None
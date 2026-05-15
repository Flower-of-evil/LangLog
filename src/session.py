from datetime import date
from . import db, language

ACTIVITY_TYPES = ('чтение', 'письмо', 'аудирование', 'говорение', 'грамматика', 'словарный запас')


def add_session_interactive():
    print("\n--- Добавление сессии ---")
    lang_id = language.choose_language()
    if lang_id is None:
        return

    today = date.today().isoformat()
    print(f"Дата (YYYY-MM-DD, Enter = {today})")
    date_str = input(">>> ").strip()
    if not date_str:
        date_str = today

    try:
        duration = int(input("Продолжительность (минуты): "))
        if duration <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: введите положительное число")
        return

    print(f"Типы: {', '.join(ACTIVITY_TYPES)}")
    act_type = input("Тип активности: ").strip().lower()
    if act_type not in ACTIVITY_TYPES:
        print("Неверный тип")
        return

    materials = input("Материалы/ресурсы: ").strip()

    try:
        rating = int(input("Самооценка (1-10): "))
        if rating < 1 or rating > 10:
            raise ValueError
    except ValueError:
        print("Ошибка: введите число от 1 до 10")
        return

    db.add_session(lang_id, date_str, duration, act_type, materials, rating)
    print("Сессия добавлена!")


def view_sessions():
    lang_id = language.choose_language()
    if lang_id is None:
        return

    sessions = db.get_sessions_by_language(lang_id)
    if not sessions:
        print("Нет сессий для этого языка")
        return

    print("\n--- Сортировка ---")
    print("1. По дате (по умолчанию)")
    print("2. По типу активности")
    choice = input(">>> ").strip()

    if choice == "2":
        # lambda + sorted: сортировка по activity_type
        sessions = sorted(sessions, key=lambda s: s['activity_type'])
    else:
        sessions = sorted(sessions, key=lambda s: s['date'])

    print("\n--- Сессии ---")
    for s in sessions:
        print(
            f"{s['date']} | {s['duration_min']} мин | {s['activity_type']} | {s['materials']} | Оценка: {s['effectiveness_rating']}")

        # ========== Lambda и filter для задания ==========

        def get_speaking_sessions(sessions):
            """Пример использования filter с lambda для отбора сессий говорения"""
            return list(filter(lambda s: s['activity_type'] == 'говорение', sessions))

        def get_session_durations(sessions):
            """Пример использования map для извлечения продолжительностей"""
            return list(map(lambda s: s['duration_min'], sessions))

        # ========== Функции для демонстрации требований задания ==========

        def get_sessions_by_type(sessions, activity_type):
            """Фильтрация сессий по типу активности с помощью filter и lambda"""
            return list(filter(lambda s: s['activity_type'] == activity_type, sessions))

        def get_total_duration(sessions):
            """Подсчёт общего времени через map и sum"""
            return sum(map(lambda s: s['duration_min'], sessions))

        def get_activity_types_list(sessions):
            """Извлечение списка типов активностей с помощью map"""
            return list(map(lambda s: s['activity_type'], sessions))

        def sort_sessions_by_rating(sessions):
            """Сортировка сессий по оценке с помощью sorted и lambda"""
            return sorted(sessions, key=lambda s: s['effectiveness_rating'], reverse=True)
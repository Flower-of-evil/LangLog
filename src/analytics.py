from datetime import datetime, timedelta
from . import db, language


# замыкание — фабрика фильтров
def create_language_filter(lang_id):
    return lambda session: session['language_id'] == lang_id


def weekly_report():
    """Еженедельный отчёт по всем языкам"""
    print("\n--- Еженедельный отчёт ---")
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    all_langs = db.get_all_languages()
    if not all_langs:
        print("Нет языков")
        return

    for lang in all_langs:
        sessions = db.get_sessions_by_language(lang['id'])
        # фильтр по дате
        week_sessions = list(filter(
            lambda s: datetime.fromisoformat(s['date']).date() >= week_ago,
            sessions
        ))

        if not week_sessions:
            print(f"\n{lang['name']}: нет сессий за неделю")
            continue

        total_min = sum(map(lambda s: s['duration_min'], week_sessions))
        total_hours = total_min / 60

        # распределение по типам
        activity_counts = {}
        for s in week_sessions:
            act = s['activity_type']
            activity_counts[act] = activity_counts.get(act, 0) + s['duration_min']

        print(f"\n{lang['name']} ({lang['level']}) — всего {total_hours:.1f} часов")
        for act, minutes in activity_counts.items():
            percent = (minutes / total_min) * 100
            bar = "█" * int(percent // 5)  # простая визуализация
            print(f"  {act}: {bar} {percent:.0f}%")

        avg_rating = sum(map(lambda s: s['effectiveness_rating'], week_sessions)) / len(week_sessions)
        print(f"  Средняя самооценка: {avg_rating:.1f}")

    print("\n--- Рекомендации ---")
    # рекомендация: найти язык, где мало говорения
    for lang in all_langs:
        sessions = db.get_sessions_by_language(lang['id'])
        week_sessions = list(filter(
            lambda s: datetime.fromisoformat(s['date']).date() >= week_ago,
            sessions
        ))
        if week_sessions:
            speaking_min = sum(s['duration_min'] for s in week_sessions if s['activity_type'] == 'говорение')
            total_min = sum(s['duration_min'] for s in week_sessions)
            if total_min > 0 and (speaking_min / total_min) < 0.1:
                print(f"⚠️ Вы редко практикуете говорение по {lang['name']} — попробуйте приложение Tandem!")


def check_level_up():
    """Проверка: если набрано N часов на уровне, предложить повысить"""
    # условно: 10 часов для A1, 20 для A2, 80 для B1, 100 для B2 и т.д.
    thresholds = {'A1': 10, 'A2': 20, 'B1': 80, 'B2': 100, 'C1': 150, 'C2': 200}
    all_langs = db.get_all_languages()

    for lang in all_langs:
        sessions = db.get_sessions_by_language(lang['id'])
        total_hours = sum(s['duration_min'] for s in sessions) / 60
        current_level = lang['level']
        needed = thresholds.get(current_level, 999)

        if total_hours >= needed:
            print(f"\n📈 Язык {lang['name']}: вы набрали {total_hours:.1f} часов на уровне {current_level}.")
            new_level = input(f"Предлагаю повысить уровень. Введите новый (например B2) или Enter: ").strip().upper()
            if new_level in ('A1', 'A2', 'B1', 'B2', 'C1', 'C2'):
                # обновляем уровень в БД
                import sqlite3
                from . import config
                with sqlite3.connect(config.get_db_path()) as conn:
                    conn.execute("UPDATE languages SET level = ? WHERE id = ?", (new_level, lang['id']))
                    conn.commit()
                print(f"Уровень обновлён на {new_level}")

                # ========== Функции для демонстрации требований задания ==========

                def get_high_rating_sessions(sessions, min_rating=8):
                    """Отбор сессий с высокой самооценкой с помощью filter и lambda"""
                    return list(filter(lambda s: s['effectiveness_rating'] >= min_rating, sessions))

                def get_durations_list(sessions):
                    """Извлечение продолжительностей через map и lambda"""
                    return list(map(lambda s: s['duration_min'], sessions))

                def get_average_rating(sessions):
                    """Подсчёт средней оценки через map и sum"""
                    if not sessions:
                        return 0
                    return sum(map(lambda s: s['effectiveness_rating'], sessions)) / len(sessions)

                def get_activity_distribution(sessions):
                    """Распределение по типам активностей с использованием map"""
                    activities = list(map(lambda s: s['activity_type'], sessions))
                    result = {}
                    for act in set(activities):
                        result[act] = activities.count(act)
                    return result
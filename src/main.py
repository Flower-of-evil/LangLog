import sys
import logging
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import db, language, session, analytics, export_import, config

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    db.init_db()
    print("=" * 50)
    print("   LangLog — персональный журнал изучения языков")
    print("=" * 50)

    while True:
        print("\nМеню:")
        print("1. Добавить язык")
        print("2. Добавить сессию практики")
        print("3. Просмотреть сессии по языку")
        print("4. Еженедельный отчёт")
        print("5. Проверить повышение уровня")
        print("6. Резервное копирование БД")
        print("7. Экспорт всех данных в ZIP")
        print("8. Импорт из ZIP")
        print("0. Выход")

        choice = input(">>> ").strip()

        try:
            if choice == "1":
                language.add_new_language()
                logging.info("Добавлен новый язык")
            elif choice == "2":
                session.add_session_interactive()
                logging.info("Добавлена сессия")
            elif choice == "3":
                session.view_sessions()
            elif choice == "4":
                analytics.weekly_report()
                logging.info("Сформирован отчёт")
            elif choice == "5":
                analytics.check_level_up()
            elif choice == "6":
                export_import.backup_db()
            elif choice == "7":
                export_import.export_all()
                logging.info("Экспорт в ZIP")
            elif choice == "8":
                zip_path = input("Путь к ZIP-файлу: ").strip()
                export_import.import_from_zip(zip_path)
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный пункт")
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
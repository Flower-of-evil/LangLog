import json
import csv
import zipfile
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime
from . import config, db


def backup_db():
    """Автоматическое резервное копирование в backups/"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_path = backup_dir / f"backup_{timestamp}.sqlite"
    shutil.copy(config.get_db_path(), backup_path)
    print(f"Резервная копия: {backup_path}")
    return backup_path


def export_all(zip_name="langlog_export.zip"):
    """Экспорт в ZIP: JSON, CSV, копия БД"""
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        # 1. JSON со всеми данными
        langs = db.get_all_languages()
        sessions = []
        for lang in langs:
            sess = db.get_sessions_by_language(lang['id'])
            sessions.extend(sess)

        data = {"languages": langs, "sessions": sessions}
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        zipf.writestr("export.json", json_str)

        # 2. CSV: язык, дата, тип, минуты, оценка
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["язык", "дата", "тип", "минуты", "оценка"])
        for s in sessions:
            lang_name = next((l['name'] for l in langs if l['id'] == s['language_id']), "unknown")
            writer.writerow([lang_name, s['date'], s['activity_type'], s['duration_min'], s['effectiveness_rating']])
        zipf.writestr("sessions.csv", csv_buffer.getvalue())

        # 3. Копия БД
        zipf.write(config.get_db_path(), "database_backup.sqlite")

    print(f"Экспорт завершён: {zip_name}")


def import_from_zip(zip_path):
    """Импорт из ZIP (требует чистой БД или осторожности)"""
    # Здесь упрощённая реализация: восстанавливаем БД из бэкапа внутри архива
    if not Path(zip_path).exists():
        print("Файл не найден")
        return

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        if "database_backup.sqlite" in zipf.namelist():
            zipf.extract("database_backup.sqlite", "temp_restore")
            shutil.copy("temp_restore/database_backup.sqlite", config.get_db_path())
            shutil.rmtree("temp_restore")
            print("База данных восстановлена из резервной копии в ZIP")
            # переинициализируем структуру (если нужно)
            db.init_db()
        else:
            print("Не найден файл database_backup.sqlite в архиве")
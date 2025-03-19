import csv
import os
from datetime import datetime

def save_resources_to_csv(resource_manager):
    """
    Сохраняет ресурсы в CSV-файл. Если запись для текущей даты уже существует, она перезаписывается.
    :param resource_manager: Объект ResourceManager с данными о ресурсах.
    """
    filename = "resources.csv"
    fieldnames = ["Дата", "JustKirill", "KirillFarm0", "KirillFarm1", "KirillFarm2", "KirillFarm3", "KirillFarm4", "Итого"]

    # Получаем текущую дату
    current_date = datetime.now().strftime("%d.%m.%Y")

    # Формируем данные для записи
    data = {
        "Дата": current_date,
        "Итого": "; ".join([f"{value / 1000000:.1f}" for value in resource_manager.total_resources.values()])
    }

    # Добавляем данные по каждому аккаунту
    for account in resource_manager.accounts:
        data[account.name] = "; ".join([f"{value / 1000000:.1f}" for value in account.resources.values()])

    # Проверяем, существует ли файл
    file_exists = os.path.isfile(filename)

    # Читаем существующие данные, если файл существует
    rows = []
    if file_exists:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

    # Проверяем, есть ли запись для текущей даты
    updated = False
    for row in rows:
        if row["Дата"] == current_date:
            # Обновляем существующую запись
            row.update(data)
            updated = True
            break

    # Если запись для текущей даты не найдена, добавляем новую
    if not updated:
        rows.append(data)

    # Записываем обновленные данные в файл
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Данные сохранены в {filename}")
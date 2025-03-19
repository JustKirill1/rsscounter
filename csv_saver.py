import csv
import os
from datetime import datetime

def save_resources_to_csv(resource_manager):
    """
    Сохраняет ресурсы в CSV-файл.
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

    # Записываем данные в CSV
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Если файл не существует, записываем заголовки
        if not file_exists:
            writer.writeheader()

        # Записываем данные
        writer.writerow(data)

    print(f"Данные сохранены в {filename}")
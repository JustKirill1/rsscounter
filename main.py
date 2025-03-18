class Account:
    def __init__(self, name, tax_rate):
        self.name = name
        self.tax_rate = tax_rate
        self.resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}

    def add_resources(self, food, wood, stone, gold):
        self.resources["food"] += food * self.tax_rate
        self.resources["wood"] += wood * self.tax_rate
        self.resources["stone"] += stone * self.tax_rate
        self.resources["gold"] += gold * self.tax_rate

    def display_resources(self):
        print(f"\nРесурсы после налога для {self.name}:")
        for key, value in self.resources.items():
            print(f"{key.capitalize()}: {value:.2f}")
        print("-" * 30)


class ResourceManager:
    def __init__(self):
        self.total_resources = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def update_total_resources(self):
        for account in self.accounts:
            for key in self.total_resources:
                self.total_resources[key] += account.resources[key]

    def display_total_resources(self):
        print("\nИтоговые ресурсы:")
        for key, value in self.total_resources.items():
            print(f"{key.capitalize()}: {value:.2f}")
        print("-" * 30)

    def check_needed_resources(self, neededRss):
        print("\nПроверка необходимых ресурсов:")
        for ch, rss in neededRss.items():
            print(f"До {ch}:")
            for rssType, count in rss.items():
                try:
                    needed = count - self.total_resources.get(rssType, 0)
                    print(f"{rssType}: {needed:.2f}" if needed > 0 else "Хватает")
                except:
                    pass
            print("-" * 50 + "\n")


# Создаем аккаунты с налогами
tax_rates = {
    "JustKirill": 1,
    "FarmKirill": 0.81,
    "KirillFarm1": 0.81,
    "KirillFarm2": 0.78
}

neededRss = {
    "23 ратуша":
        {"food": 90.2, "wood": 93.4, "stone": 72.4, "speedUps": "Хватает"},
    "24 ратуша":
        {"food": 218, "wood": 237, "stone": 175, "speedUps": "Хватает"},
    "24 ратуша + стена 24":
        {"food": 345, "wood": 370, "stone": 279, "speedUps": "Хватает"},
    "25 ратуша":
        {"food": 427, "wood": 472, "stone": 361, "speedUps": 147}
}

resource_manager = ResourceManager()

for name, rate in tax_rates.items():
    account = Account(name, rate)
    print(f"\nВвод ресурсов для аккаунта: {name} Налог: {100 - rate * 100}%")
    food = float(input("Пища: "))
    wood = float(input("Дерево: "))
    stone = float(input("Камень: "))
    gold = float(input("Золото: "))

    account.add_resources(food, wood, stone, gold)
    account.display_resources()
    resource_manager.add_account(account)

# Обновляем и отображаем общие ресурсы
resource_manager.update_total_resources()
resource_manager.display_total_resources()
resource_manager.check_needed_resources(neededRss)

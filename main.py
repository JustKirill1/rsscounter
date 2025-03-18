
resources = {
    "food": 0,
    "wood": 0,
    "stone": 0,
    "gold": 0,
    "speedUps": 121

}

def calculate_resources(food, wood, stone, gold, percentage):
    food *= percentage
    wood *= percentage
    stone *= percentage
    gold *= percentage
    return food, wood, stone, gold

tax_rates = {
    "JustKirill": 1,
    "FarmKirill": 0.81,
    "KirillFarm1": 0.81,
    "KirillFarm2": 0.78
}

neededRss = {
    "23 ратуша":
        {
            "food": 90.2,
            "wood": 93.4,
            "stone": 72.4,
            "speedUps": "Хватает"
        },
    "24 ратуша":
        {
            "food": 218,
            "wood": 237,
            "stone": 175,
            "speedUps": "Хватает"
        },
    "24 ратуша + стена 24":
        {
            "food": 345,
            "wood": 370,
            "stone": 279,
            "speedUps": "Хватает"
        },
    "25 ратуша":
        {
            "food": 427,
            "wood": 472,
            "stone": 361,
            "speedUps": 147
        }

}

for account, rate in tax_rates.items():
    print(f"\nВвод ресурсов для аккаунта: {account} Налог: {100 - rate * 100}%")
    food = float(input("Пища: "))
    wood = float(input("Дерево: "))
    stone = float(input("Камень: "))
    gold = float(input("Золото: "))

    taxed_food, taxed_wood, taxed_stone, taxed_gold = calculate_resources(food, wood, stone, gold, rate)

    resources["food"] += taxed_food
    resources["wood"] += taxed_wood
    resources["stone"] += taxed_stone
    resources["gold"] += taxed_gold

    print(f"\nРесурсы после налога для аккаунта {account}:")
    print(f"Пища: {taxed_food}")
    print(f"Дерево: {taxed_wood}")
    print(f"Камень: {taxed_stone}")
    print(f"Золото: {taxed_gold}")
    print("-" * 30)

print("\nИтоговые ресурсы:")
print(f"Пища: {resources['food']:.2f}")
print(f"Дерево: {resources['wood']:.2f}")
print(f"Камень: {resources['stone']:.2f}")
print(f"Золото: {resources['gold']:.2f}")
print("-" * 30)
for ch, rss in neededRss.items():
    print(f"До {ch}:")
    for rssType, count in rss.items():
        try:
            print(f"{rssType}: {(count - resources[f"{rssType}"]):.2f}" if (count - resources[
                f"{rssType}"]) > 0 else "Хватает")
        except:
            pass
    print("-" * 50 + "\n")

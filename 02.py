import csv
import timeit
from BTrees.OOBTree import OOBTree


# 1. Завантаження даних із файлу CSV
def load_data(file_path):
    items = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(
                {
                    "ID": int(row["ID"]),
                    "Name": row["Name"],
                    "Category": row["Category"],
                    "Price": float(row["Price"]),
                }
            )
    return items


# 2. Створення структури OOBTree і словника dict
def add_item_to_tree(tree, item):
    tree[item["ID"]] = item


def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item


# 3. Виконання діапазонного запиту
def range_query_tree(tree, min_price, max_price):
    return list(tree.values(min=min_price, max=max_price))


def range_query_dict(dictionary, min_price, max_price):
    return [
        value
        for value in dictionary.values()
        if min_price <= value["Price"] <= max_price
    ]


# 4. Функція для тестування продуктивності
def measure_performance(tree, dictionary, min_price, max_price, repetitions=100):
    # Час для OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price), number=repetitions
    )

    # Час для dict
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price), number=repetitions
    )

    return tree_time, dict_time


# 5. Основна програма
def main():
    file_path = "generated_items_data.csv"
    items = load_data(file_path)

    # Ініціалізація структур даних
    tree = OOBTree()
    dictionary = {}

    # Додавання товарів у структури
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Налаштування діапазону цін
    min_price = 10.0
    max_price = 50.0

    # Вимірювання продуктивності
    tree_time, dict_time = measure_performance(tree, dictionary, min_price, max_price)

    # Виведення результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")


if __name__ == "__main__":
    main()

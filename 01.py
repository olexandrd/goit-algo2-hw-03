import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    """
    Створює граф на основі заданих даних про пропускні здатності.
    """
    G = nx.DiGraph()

    # Додавання ребер та їх пропускних здатностей
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    super_source = "SuperSource"
    for terminal in ["Термінал 1", "Термінал 2"]:
        G.add_edge(super_source, terminal, capacity=float("inf"))

    super_sink = "SuperSink"
    for store in [
        "Магазин 1",
        "Магазин 2",
        "Магазин 3",
        "Магазин 4",
        "Магазин 5",
        "Магазин 6",
        "Магазин 7",
        "Магазин 8",
        "Магазин 9",
        "Магазин 10",
        "Магазин 11",
        "Магазин 12",
        "Магазин 13",
        "Магазин 14",
    ]:
        G.add_edge(store, super_sink, capacity=float("inf"))

    return G


def calculate_max_flow(graph, source, sink):
    """
    Обчислює максимальний потік у графі.

    Args:
        graph: Граф (мережа потоків)
        source: Джерело потоку
        sink: Сток потоку

    Returns:
        Максимальний потік та шляхи використання
    """

    # Використання алгоритму Едмондса-Карпа для обчислення максимального потоку
    flow_value, flow_dict = nx.maximum_flow(
        graph, source, sink, flow_func=nx.algorithms.flow.edmonds_karp
    )
    return flow_value, flow_dict


def calculate_unused_capacity(graph, flow_dict):
    """
    Підраховує невикористану пропускну здатність для кожного ребра.

    Args:
        graph: Граф (мережа потоків)
        flow_dict: Розподіл потоку

    Returns:
        Словник з невикористаними пропускними здатностями
    """
    unused_capacity = {}
    for u, v, data in graph.edges(data=True):
        flow = flow_dict.get(u, {}).get(v, 0)
        capacity = data["capacity"]
        unused_capacity[(u, v)] = capacity - flow
    return unused_capacity


def visualize_graph(graph, flow_dict):
    """
    Візуалізує граф з потоками.

    Args:
        graph: Граф (мережа потоків)
        flow_dict: Розподіл потоку
    """
    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, "capacity")

    plt.figure(figsize=(12, 8))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        font_size=10,
        font_weight="bold",
    )
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels={
            (u, v): f"{flow}/{labels[(u, v)]}" for u, v, flow in graph.edges(data=True)
        },
    )
    plt.title("Граф мережі потоків")
    plt.show()


def generate_terminal_to_store_summary_with_intermediates(flow_dict):
    """
    Створює зведену таблицю потоків між терміналами та магазинами,
    враховуючи проміжні вузли.

    Args:
        flow_dict: Розподіл потоків

    Returns:
        Зведена таблиця у вигляді списку словників
    """
    summary = {}

    # Перебір всіх джерел (source) та цілей (target) у flow_dict
    for source, targets in flow_dict.items():
        for target, flow in targets.items():
            if flow > 0:  # Враховуємо тільки ненульові потоки
                # Якщо це термінал -> склад, зберігаємо в проміжному словнику
                if source.startswith("Термінал") and target.startswith("Склад"):
                    if target not in summary:
                        summary[target] = {}
                    summary[target][source] = summary[target].get(source, 0) + flow

                # Якщо це склад -> магазин, додаємо до підсумків
                if source.startswith("Склад") and target.startswith("Магазин"):
                    for terminal, terminal_flow in summary.get(source, {}).items():
                        key = (terminal, target)
                        summary[key] = summary.get(key, 0) + min(flow, terminal_flow)

    # Форматуємо результат як список словників
    table = []
    for key, flow in summary.items():
        if isinstance(key, tuple):  # Тільки підсумкові термінал -> магазин
            terminal, store = key
            table.append(
                {
                    "Термінал": terminal,
                    "Магазин": store,
                    "Фактичний Потік (одиниць)": flow,
                }
            )

    return table


def main():
    # Створення графа
    graph = create_graph()

    # Визначення джерела та стоку
    source = "SuperSource"
    sink = "SuperSink"

    # Обчислення максимального потоку
    max_flow, flow_distribution = calculate_max_flow(graph, source, sink)

    # Обчислення невикористаних пропускних здатностей
    unused_capacity = calculate_unused_capacity(graph, flow_distribution)

    summary_table = generate_terminal_to_store_summary_with_intermediates(
        flow_distribution
    )

    print("Максимальний потік:", max_flow)
    print("Таблиця потоків між терміналами та магазинами:")
    for row in summary_table:
        print(row)

    print("\nНевикористані пропускні здатності:")
    for (u, v), capacity in unused_capacity.items():
        if capacity != float("inf") and capacity > 0:
            print(f"{u} -> {v}: {capacity}")

    # Візуалізація графу - вимкнено через велику кількість невпорядкованих ребер
    # visualize_graph(graph, flow_distribution)


if __name__ == "__main__":
    main()

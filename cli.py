from simple_term_menu import TerminalMenu

from contentBasedRecomendationSystem.recomendation_strategy import RecommendationStrategy
from contentBasedRecomendationSystem.recomendattion_system import RecommendationSystem, \
    get_recommendation_after_filtration
from filter import Filter
from map_displayer import display_map
from measure_worker import calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance

options = [
    "Вывести все записи",
    "Визуализировать матрицу расстояний",
    "Поставить лайк",
    "Сбросить лайк",
    "Поставить дизлайк",
    "Сбросить дизлайк",
    "Установить фильтр",
    "Сбросить фильтр",
    "Вывести фильтр",
    "Установить функцию меры",
    "Установить стратегию рекомендации",
    "Получить рекомендацию",
    "Выход"
]

main_filter = Filter()


def main_loop(recommendation_system: RecommendationSystem, liked_items, disliked_items) -> int:
    global main_filter
    terminal_menu = TerminalMenu(options)
    selected_menu_index = terminal_menu.show()
    match selected_menu_index:
        case 0:
            items = recommendation_system.query_all_items(None)
            for i, item in enumerate(items):
                liked = "" if i not in liked_items else "👍"
                disliked = "" if i not in disliked_items else "👎"
                print(
                    f"{i:2}) {liked:1} {disliked:1} {item.name} {item.brand}: {item.color} масса={item.weight} "
                    f"Объем двигателя={item.engine_capacity}")
            return 0
        case 1:
            display_map(recommendation_system.items, 'Euclidean distance', calculate_measure_using_euclidean_distance)
            display_map(recommendation_system.items, 'Cosine distance', calculate_measure_using_cosine_distance)
            return 0
        case 2:
            item_index_str = input()
            try:
                item_index_int = int(item_index_str)
            except:
                print('Ошибка при введении индекса лайка')
                return -1
            if item_index_int in disliked_items:
                print('Мотоцикл уже дизлайк')
                return -1
            elif item_index_int < 0 or item_index_int > len(recommendation_system.query_all_items(None)):
                print('Индекс вне границ')
                return -1
            else:
                liked_items.append(item_index_int)
                print("Лайк мотоцикл")
            return 0
        case 3:
            item_index_str = input()
            try:
                item_index_int = int(item_index_str)
            except:
                print('Ошибка при введении индекса лайка')
                return -1
            if not item_index_int in liked_items:
                print("Мотоцикл вне списка лайков")
                return -1
            else:
                del liked_items[liked_items.index[item_index_int]]
                print('Мотоцикл уделен из списка лайков')
        case 4:
            item_index_str = input()
            try:
                item_index_int = int(item_index_str)
            except:
                print('Ошибка при введении индекса лайка')
                return -1
            if item_index_int in disliked_items:
                print('Мотоцикл уже лайк')
                return -1
            elif item_index_int < 0 or item_index_int > len(recommendation_system.query_all_items(None)):
                print('Индекс вне границ')
                return -1
            else:
                disliked_items.append(item_index_int)
                print("Дизлайк мотоцикл")
        case 5:
            item_index_str = input()
            try:
                item_index_int = int(item_index_str)
            except:
                print('Ошибка при введении индекса лайка')
                return -1
            if not item_index_int in disliked_items:
                print("Мотоцикл вне списка дизлайков")
                return -1
            else:
                del disliked_items[disliked_items.index[item_index_int]]
                print('Мотоцикл уделен из списка дизлайков')
        case 6:
            main_filter = set_filter(main_filter)
            return 0
        case 7:
            main_filter = Filter()
            return 0
        case 8:
            print_current_filter(main_filter)
            return 0
        case 9:
            return choose_measure_function(recommendation_system)
        case 10:
            return choose_recommendation_strategy(recommendation_system)
        case 11:
            all_items = recommendation_system.query_all_items(None)
            liked_items = [item for (i, item) in enumerate(all_items) if i in liked_items]
            disliked_items = [item for (i, item) in enumerate(all_items) if i in disliked_items]
            items = []
            if recommendation_system.recommendation_strategy == RecommendationStrategy.FilterRecommend:
                items = get_recommendation_after_filtration(recommendation_system, liked_items, disliked_items,
                                                            main_filter)
            for i, item in enumerate(items):
                print(
                    f"{i:2}) {item.name} {item.brand}: {item.color} масса={item.weight} "
                    f"Объем двигателя={item.engine_capacity}")
            return 0
        case 12:
            print("Out")
            return 1
        case _:
            print("Invalid menu")

    return 0


def choose_measure_function(recommendation_system: RecommendationSystem):
    choose_measure_option = ["Euclidean", "Cosine"]
    terminal_menu = TerminalMenu(choose_measure_option)
    selected_menu_index = terminal_menu.show()
    if selected_menu_index == 0:
        recommendation_system.calculate_measure_func(calculate_measure_using_euclidean_distance)
    elif selected_menu_index == 1:
        recommendation_system.calculate_measure_func(calculate_measure_using_cosine_distance)
    else:
        print("Choose measure function")

    return 0


def set_filter(filter_element: Filter) -> Filter:
    choose_measure_option = [
        "Название",  # 0
        "Марка",  # 1
        "Масса",  # 2
        "Объем двигателя",  # 3
        "Цвет",  # 4
        "Дорожный просвет",  # 5
        "Высота посадки",  # 6
        "Количество места",  # 7
        "Максимальная скорость",  # 8
        "Мощность",  # 9
        "Объем топливного бака",  # 10
        "Наличие навигатора (Да/Нет)",  # 11
        "Наличие компрессора (Да/Нет)",  # 12
        "Высота",  # 13
        "Наличие фары (Да/Нет)",  # 14
        "Наличие поворотник (Да/Нет)",  # 15
        "Количество цилиндров",  # 16
        "Грузоподъемность",  # 17
        "Трансмиссия (Автоматический/Вариатор)",  # 18
        "Крутящий момент",  # 19
        "Объем багажника",  # 20
        "Наличие аудиосистемы",  # 21
    ]

    terminal_menu = TerminalMenu(choose_measure_option)
    selected_menu_index = terminal_menu.show()
    match selected_menu_index:
        case 0:
            filter_element.name = input("Название мотоцикла : ")
        case 1:
            filter_element.brand = input("Марка: ")
        case 2:
            choose_option = TerminalMenu(["Начальная масса", "Окончательная масса"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.weight_min = float(input("Начальная масса : "))
            else:
                filter_element.weight_max = float(input("Окончательная масса : "))
        case 3:
            choose_option = TerminalMenu(["Начальный объем двигателя", "Окончательный объем двигателя"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.engine_capacity_min = float(input("Начальный объем двигателя : "))
            else:
                filter_element.engine_capacity_min = float(input("Окончательный объем двигателя : "))
        case 4:
            filter_element.color = input("Цвет [Красный, Черный, Синий, Серое, Желтый, Зеленый, Темно-синий, Белый]")
        case 5:
            choose_option = TerminalMenu(["Начальный дорожный просвет", "Окончательный дорожный просвет"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.ground_clearance_min = float(input("Начальный дорожный просвет : "))
            else:
                filter_element.ground_clearance_max = float(input("Окончательный дорожный просвет : "))
        case 6:
            choose_option = TerminalMenu(["Начальная высота посадки", "Окончательная высота посадки"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.landing_height_min = float(input("Начальная высота посадки : "))
            else:
                filter_element.landing_height_max = float(input("Окончательная высота посадки : "))
        case 7:
            choose_option = TerminalMenu(["Начальное количество места", "Окончательное количество места"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.seats_min = float(input("Начальное количество места : "))
            else:
                filter_element.seats_max = float(input("Окончательное количество места : "))
        case 8:
            choose_option = TerminalMenu(["Начальная максимальная скорость", "Окончательная максимальная скорость"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.max_speed_min = float(input("Начальная максимальная скорость : "))
            else:
                filter_element.max_speed_max = float(input("Окончательная максимальная скорость : "))
        case 9:
            choose_option = TerminalMenu(["Начальная мощность", "Окончательная мощность"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.power_min = float(input("Начальная мощность : "))
            else:
                filter_element.power_max = float(input("Окончательная мощность : "))
        case 10:
            choose_option = TerminalMenu(["Начальный объем топливного бака", "Окончательный объем топливного бака"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.fuel_tank_capacity_min = float(input("Начальный объем топливного бака : "))
            else:
                filter_element.fuel_tank_capacity_max = float(input("Окончательный объем топливного бака : "))
        case 11:
            exist_element_input = input("Наличие навигатора Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_navigator = True
            elif exist_element_input == "Нет":
                filter_element.exist_navigator = False
            else:
                print("Наличие навигатора Да или Нет")
        case 12:
            exist_element_input = input("Наличие компрессора Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_compressor = True
            elif exist_element_input == "Нет":
                filter_element.exist_compressor = False
            else:
                print("Наличие компрессора Да или Нет")
        case 13:
            choose_option = TerminalMenu(["Начальная высота", "Окончательная высота"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.height_min = float(input("Начальная высота : "))
            else:
                filter_element.height_max = float(input("Окончательная высота : "))
        case 14:
            exist_element_input = input("Наличие фары Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_headlight = True
            elif exist_element_input == "Нет":
                filter_element.exist_headlight = False
            else:
                print("Наличие фары Да или Нет")
        case 15:
            exist_element_input = input("Наличие поворотник Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_turn_signal = True
            elif exist_element_input == "Нет":
                filter_element.exist_turn_signal = False
            else:
                print("Наличие поворотник Да или Нет")
        case 16:
            choose_option = TerminalMenu(["Начальное количество цилиндров", "Окончательное количество цилиндров"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.cylinder_number_min = float(input("Начальное количество цилиндров : "))
            else:
                filter_element.cylinder_number_max = float(input("Окончательное количество цилиндров : "))
        case 17:
            choose_option = TerminalMenu(["Начальная грузоподъемность", "Окончательная грузоподъемность"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.load_capacity_min = float(input("Начальная грузоподъемность : "))
            else:
                filter_element.load_capacity_max = float(input("Окончательная грузоподъемность : "))
        case 18:
            choose_option = TerminalMenu(["[0] Автоматический", "[1] Вариатор", "[2] Не важно"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.transmission = "Автоматический"
            elif selected_index == 1:
                filter_element.transmission = "Вариатор"
            else:
                filter_element.transmission = "Empty"
        case 19:
            choose_option = TerminalMenu(["Начальный Крутящий момент", "Окончательный Крутящий момент"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.torque_min = float(input("Начальный Крутящий момент : "))
            else:
                filter_element.torque_max = float(input("Окончательный Крутящий момент : "))
        case 20:
            choose_option = TerminalMenu(["Начальный объем багажника", "Окончательный объем багажника"])
            selected_index = choose_option.show()
            if selected_index == 0:
                filter_element.trunk_volume_min = float(input("Начальный объем багажника : "))
            else:
                filter_element.trunk_volume_max = float(input("Окончательный объем багажника : "))
        case 21:
            exist_element_input = input("Наличие аудиосистемы Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_radio_system = True
            elif exist_element_input == "Нет":
                filter_element.exist_radio_system = False
            else:
                print("Наличие аудиосистемы Да или Нет")

    return filter_element


def choose_recommendation_strategy(recommendation_system: RecommendationSystem):
    choose_strategy_option = ["Фильтрация -> Рекомендация", "Рекомендация -> Фильтрация"]
    terminal_menu = TerminalMenu(choose_strategy_option)
    selected_index = terminal_menu.show()

    if selected_index == 0:
        recommendation_system.recommendation_strategy = RecommendationStrategy.FilterRecommend
    elif selected_index == 1:
        recommendation_system.recommendation_strategy = RecommendationStrategy.RecommendFilter
    else:
        choose_recommendation_strategy(recommendation_system)
    return 0


def print_current_filter(filter_element: Filter):
    print("\n FILTER \n")
    print("Название мотоцикла: ", filter_element.name)
    print("Марка мотоцикла: ", filter_element.brand)
    print("[MIN] Масса: ", filter_element.weight_min)
    print("[MAX] Масса: ", filter_element.weight_max)
    print("[MIN] Объем двигателя: ", filter_element.engine_capacity_min)
    print("[MAX] Объем двигателя: ", filter_element.engine_capacity_max)
    print("Цвет: ", filter_element.color)
    print("[MIN] Дорожный просвет: ", filter_element.ground_clearance_min)
    print("[MAX] Дорожный просвет: ", filter_element.ground_clearance_max)
    print("[MIN] Высота посадки: ", filter_element.landing_height_min)
    print("[MAX] Высота посадки: ", filter_element.landing_height_max)
    print("[MIN] Количество места: ", filter_element.seats_min)
    print("[MAX] Количество места: ", filter_element.seats_max)
    print("[MIN] Максимальная скорость: ", filter_element.max_speed_min)
    print("[MAX] Максимальная скорость: ", filter_element.max_speed_max)
    print("[MIN] Мощность: ", filter_element.power_min)
    print("[MAX] Мощность: ", filter_element.power_max)
    print("[MIN] Объем топливного бака: ", filter_element.fuel_tank_capacity_min)
    print("[MAX] Объем топливного бака: ", filter_element.fuel_tank_capacity_max)
    print("Наличие навигатора (Да/Нет): ", filter_element.exist_navigator)
    print("Наличие компрессора (Да/Нет): ", filter_element.exist_compressor)
    print("[MIN] Высота: ", filter_element.height_min)
    print("[MAX] Высота: ", filter_element.height_max)
    print("Наличие фары (Да/Нет): ", filter_element.exist_headlight)
    print("Наличие поворотник (Да/Нет): ", filter_element.exist_turn_signal)
    print("[MIN] Количество цилиндров: ", filter_element.cylinder_number_min)
    print("[MAX] Количество цилиндров: ", filter_element.cylinder_number_max)
    print("[MIN] Грузоподъемность: ", filter_element.load_capacity_min)
    print("[MAX] Грузоподъемность: ", filter_element.load_capacity_max)
    print("Трансмиссия: ", filter_element.transmission)
    print("[MIN] Крутящий момент: ", filter_element.torque_min)
    print("[MAX] Крутящий момент: ", filter_element.torque_max)
    print("[MIN] Объем багажника: ", filter_element.trunk_volume_min)
    print("[MAX] Объем багажника: ", filter_element.trunk_volume_max)
    print("Наличие аудиосистемы (Да/Нет): ", filter_element.exist_compressor)

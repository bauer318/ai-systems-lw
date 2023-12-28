from InquirerPy import inquirer

from contentBasedRecomendationSystem.recomendation_strategy import RecommendationStrategy
from contentBasedRecomendationSystem.recomendattion_system import RecommendationSystem, \
    get_recommendation_after_filtration, get_recommendation_before_filtration
from filter import Filter
from map_displayer import display_map
from measure_worker import calculate_measure_using_euclidean_distance, calculate_measure_using_cosine_distance
from util import get_motorcycle_type

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
    selected_menu = inquirer.select(
        message="",
        choices=options
    ).execute()
    match selected_menu:
        case "Вывести все записи":
            items = recommendation_system.query_all_items(None)
            for i, item in enumerate(items):
                liked = "" if i not in liked_items else "👍"
                disliked = "" if i not in disliked_items else "👎"
                print(
                    f"{i:2}) {liked:1} {disliked:1} {item.name} {item.brand}: {item.color} масса={item.weight} "
                    f"Объем двигателя={item.engine_capacity}")
            return 0
        case "Визуализировать матрицу расстояний":
            display_map(recommendation_system.items, 'Euclidean distance', calculate_measure_using_euclidean_distance)
            display_map(recommendation_system.items, 'Cosine distance', calculate_measure_using_cosine_distance)
            return 0
        case "Поставить лайк":
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
        case "Сбросить лайк":
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
                del liked_items[liked_items.index(item_index_int)]
                print('Мотоцикл уделен из списка лайков')
        case "Поставить дизлайк":
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
        case "Сбросить дизлайк":
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
                del disliked_items[disliked_items.index(item_index_int)]
                print('Мотоцикл уделен из списка дизлайков')
        case "Установить фильтр":
            main_filter = set_filter(main_filter)
            return 0
        case "Сбросить фильтр":
            main_filter = Filter()
            return 0
        case "Вывести фильтр":
            print_current_filter(main_filter)
            return 0
        case "Установить функцию меры":
            return choose_measure_function(recommendation_system)
        case "Установить стратегию рекомендации":
            return choose_recommendation_strategy(recommendation_system)
        case "Получить рекомендацию":
            all_items = recommendation_system.query_all_items(None)
            liked_items = [item for (i, item) in enumerate(all_items) if i in liked_items]
            disliked_items = [item for (i, item) in enumerate(all_items) if i in disliked_items]
            if recommendation_system.recommendation_strategy == RecommendationStrategy.FilterRecommend:
                print("\n========== Рекомендация ==========\n")
                for i, item in enumerate(
                        get_recommendation_after_filtration(recommendation_system, liked_items, disliked_items,
                                                            main_filter)):
                    print(
                        f"{i:2}) {item.name} {item.brand}: {item.color} масса={item.weight} "
                        f"Объем двигателя={item.engine_capacity} type:{get_motorcycle_type(item)}")
                return 0
            else:
                print("\n========== Рекомендация ==========\n")
                for i, item in enumerate(
                        get_recommendation_before_filtration(recommendation_system, liked_items, disliked_items,
                                                             main_filter)):
                    print(
                        f"{i:2}) {item.name} {item.brand}: {item.color} масса={item.weight} "
                        f"Объем двигателя={item.engine_capacity} type:{get_motorcycle_type(item)}")
                return 0
        case "Выход":
            print("Out")
            return 1
        case _:
            print("Invalid menu")

    return 0


def choose_measure_function(recommendation_system: RecommendationSystem):
    choose_measure_option = ["Euclidean", "Cosine"]
    selected_menu = inquirer.select(
        message="",
        choices=choose_measure_option
    ).execute()
    if selected_menu == "Euclidean":
        recommendation_system.calculate_measure_func(calculate_measure_using_euclidean_distance)
    elif selected_menu == "Cosine":
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

    selected_menu = inquirer.select(
        message="",
        choices=choose_measure_option
    ).execute()
    match selected_menu:
        case "Название":
            filter_element.name = input("Название мотоцикла : ")
        case "Марка":
            filter_element.brand = input("Марка: ")
        case "Масса":
            choose_option = ["Маленькая", "Очень не большая", "Средняя", "Не очень большая", "Большая"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Маленькая":
                filter_element.weight_max = 100
            elif selected_menu == "Очень не большая":
                filter_element.weight_min = 100
                filter_element.weight_max = 150
            elif selected_menu == "Средняя":
                filter_element.weight_min = 150
                filter_element.weight_max = 215
            elif selected_menu == "Не очень большая":
                filter_element.weight_min = 215
                filter_element.weight_max = 320
            else:
                filter_element.weight_min = 320
        case "Объем двигателя":
            choose_option = ["Начальный объем двигателя", "Окончательный объем двигателя"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальный объем двигателя":
                filter_element.engine_capacity_min = float(input("Начальный объем двигателя : "))
            else:
                filter_element.engine_capacity_min = float(input("Окончательный объем двигателя : "))
        case "Цвет":
            filter_element.color = input("Цвет [Красный, Черный, Синий, Серое, Желтый, Зеленый, Темно-синий, Белый]")
        case "Дорожный просвет":
            choose_option = ["Начальный дорожный просвет", "Окончательный дорожный просвет"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальный дорожный просвет":
                filter_element.ground_clearance_min = float(input("Начальный дорожный просвет : "))
            else:
                filter_element.ground_clearance_max = float(input("Окончательный дорожный просвет : "))
        case "Высота посадки":
            choose_option = ["Начальная высота посадки", "Окончательная высота посадки"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальная высота посадки":
                filter_element.landing_height_min = float(input("Начальная высота посадки : "))
            else:
                filter_element.landing_height_max = float(input("Окончательная высота посадки : "))
        case "Количество места":
            choose_option = ["Начальное количество места", "Окончательное количество места"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальное количество места":
                filter_element.seats_min = float(input("Начальное количество места : "))
            else:
                filter_element.seats_max = float(input("Окончательное количество места : "))
        case "Максимальная скорость":
            choose_option = ["Начальная максимальная скорость", "Окончательная максимальная скорость"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальная максимальная скорость":
                filter_element.max_speed_min = float(input("Начальная максимальная скорость : "))
            else:
                filter_element.max_speed_max = float(input("Окончательная максимальная скорость : "))
        case "Мощность":
            choose_option = ["Начальная мощность", "Окончательная мощность"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальная мощность":
                filter_element.power_min = float(input("Начальная мощность : "))
            else:
                filter_element.power_max = float(input("Окончательная мощность : "))
        case "Объем топливного бака":
            choose_option = ["Начальный объем топливного бака", "Окончательный объем топливного бака"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальный объем топливного бака":
                filter_element.fuel_tank_capacity_min = float(input("Начальный объем топливного бака : "))
            else:
                filter_element.fuel_tank_capacity_max = float(input("Окончательный объем топливного бака : "))
        case "Наличие навигатора (Да/Нет)":
            exist_element_input = input("Наличие навигатора Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_navigator = True
            elif exist_element_input == "Нет":
                filter_element.exist_navigator = False
            else:
                print("Наличие навигатора Да или Нет")
        case "Наличие компрессора (Да/Нет)":
            exist_element_input = input("Наличие компрессора Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_compressor = True
            elif exist_element_input == "Нет":
                filter_element.exist_compressor = False
            else:
                print("Наличие компрессора Да или Нет")
        case "Высота":
            choose_option = ["Начальная высота", "Окончательная высота"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальная высота":
                filter_element.height_min = float(input("Начальная высота : "))
            else:
                filter_element.height_max = float(input("Окончательная высота : "))
        case "Наличие фары (Да/Нет)":
            exist_element_input = input("Наличие фары Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_headlight = True
            elif exist_element_input == "Нет":
                filter_element.exist_headlight = False
            else:
                print("Наличие фары Да или Нет")
        case "Наличие поворотник (Да/Нет)":
            exist_element_input = input("Наличие поворотник Да или Нет")
            if exist_element_input == "Да":
                filter_element.exist_turn_signal = True
            elif exist_element_input == "Нет":
                filter_element.exist_turn_signal = False
            else:
                print("Наличие поворотник Да или Нет")
        case "Количество цилиндров":
            choose_option = ["Начальное количество цилиндров", "Окончательное количество цилиндров"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальное количество цилиндров":
                filter_element.cylinder_number_min = float(input("Начальное количество цилиндров : "))
            else:
                filter_element.cylinder_number_max = float(input("Окончательное количество цилиндров : "))
        case "Грузоподъемность":
            choose_option = ["Начальная грузоподъемность", "Окончательная грузоподъемность"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальная грузоподъемность":
                filter_element.load_capacity_min = float(input("Начальная грузоподъемность : "))
            else:
                filter_element.load_capacity_max = float(input("Окончательная грузоподъемность : "))
        case "Трансмиссия (Автоматический/Вариатор)":
            choose_option = ["Автоматический", "Вариатор", "Не важно"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Автоматический":
                filter_element.transmission = "Автоматический"
            elif selected_menu == "Вариатор":
                filter_element.transmission = "Вариатор"
            else:
                filter_element.transmission = "Empty"
        case "Крутящий момент":
            choose_option = ["Начальный Крутящий момент", "Окончательный Крутящий момент"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальный Крутящий момент":
                filter_element.torque_min = float(input("Начальный Крутящий момент : "))
            else:
                filter_element.torque_max = float(input("Окончательный Крутящий момент : "))
        case "Объем багажника":
            choose_option = ["Начальный объем багажника", "Окончательный объем багажника"]
            selected_menu = inquirer.select(
                message="",
                choices=choose_option
            ).execute()
            if selected_menu == "Начальный объем багажника":
                filter_element.trunk_volume_min = float(input("Начальный объем багажника : "))
            else:
                filter_element.trunk_volume_max = float(input("Окончательный объем багажника : "))
        case "Наличие аудиосистемы":
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
    selected_menu = inquirer.select(
        message="",
        choices=choose_strategy_option
    ).execute()

    if selected_menu == "Фильтрация -> Рекомендация":
        recommendation_system.recommendation_strategy = RecommendationStrategy.FilterRecommend
    elif selected_menu == "Рекомендация -> Фильтрация":
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

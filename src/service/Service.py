import logging

from src.repository import CanteenRepo

logging.basicConfig(level=logging.INFO)


def get_all_options():
    return CanteenRepo.get_all_options_repo()


def get_all_options_by_food_category(food_category):
    match food_category:
        case "all":
            return CanteenRepo.get_all_options_repo()
        case "veg" | "non_veg" | "desert":
            return CanteenRepo.get_all_options_by_food_category_repo(food_category)


def get_order_item_by_id(item_id):
    return CanteenRepo.get_order_item_by_id_repo(item_id)

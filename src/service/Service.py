import logging

from src.repository.CanteenRepo import get_index_route_repo, get_order_item_by_id_repo

logging.basicConfig(level=logging.INFO)


def get_index_route_data():
    logging.error("10................")
    return get_index_route_repo()


def get_order_item_by_id(item_id):
    logging.error("10................")
    return get_order_item_by_id_repo(item_id)

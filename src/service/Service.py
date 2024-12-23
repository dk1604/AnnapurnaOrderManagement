import logging
from src.repository.CanteenRepo import get_index_route_repo


def get_index_route_data():
    logging.info("10................")
    return get_index_route_repo()

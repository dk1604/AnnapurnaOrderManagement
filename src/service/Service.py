import logging

from src.repository.CanteenRepo import get_index_route_repo

logging.basicConfig(level=logging.INFO)


def get_index_route_data():
    logging.error("10................")
    return get_index_route_repo()

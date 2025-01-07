from src.repository.OrderRepo import save_order_details_repo, get_order_details_repo


def save_order_details_service(customer_order_detail):
    return save_order_details_repo(customer_order_detail)


def get_order_details_service(start_time, end_time):
    return get_order_details_repo(start_time, end_time)

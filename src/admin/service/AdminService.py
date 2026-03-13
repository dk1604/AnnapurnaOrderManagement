import math

from Demos.mmapfile_demo import offset

from src.admin.repository.AdminRepo import save_repo, save_all_repo, save_vendor_expense_repo, get_vendor_expense_repo, \
    get_all_menu_repo


def save_service(data):
    return save_repo(data)

def save_all_service():
    return save_all_repo()

def save_vendor_expense_service(data):
    return save_vendor_expense_repo(data)

def get_vendor_expense_service(page, page_size):
    vendor_expense = get_vendor_expense_repo()
    total_records = len(vendor_expense)
    offset = (page - 1) * page_size
    paginated_data = vendor_expense[offset: offset + page_size]
    total_pages = math.ceil(total_records / page_size)

    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": paginated_data
    }

def get_all_menu_service():
    return get_all_menu_repo()

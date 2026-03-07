from src.admin.repository.AdminRepo import save_repo, save_all_repo, save_vendor_expense_repo, get_vendor_expense_repo, \
    get_all_menu_repo


def save_service(data):
    return save_repo(data)

def save_all_service():
    return save_all_repo()

def save_vendor_expense_service(data):
    return save_vendor_expense_repo(data)

def get_vendor_expense_service():
    return get_vendor_expense_repo()

def get_all_menu_service():
    return get_all_menu_repo()

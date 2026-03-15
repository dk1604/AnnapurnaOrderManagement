import math

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

    total_expense = 0
    total_paid = 0
    total_balance  = 0

    for expense in vendor_expense:
        payment_mode = expense.get("payment_mode")
        amount = float(expense.get("amount", 0))

        if payment_mode in ["purchase_pay_cash", "purchase_pay_online"]:
            total_expense += amount
            total_paid += amount
        elif payment_mode == "purchase_on_credit":
            total_expense += amount
        elif payment_mode in ["vendor_payment_cash", "vendor_payment_online"]:
            total_paid += amount

    total_balance = total_expense - total_paid

    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": paginated_data,
        "total_expense": total_expense,
        "total_paid": total_paid,
        "total_balance": total_balance
    }

def get_all_menu_service():
    return get_all_menu_repo()

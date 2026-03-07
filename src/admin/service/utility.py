import re


def parse_insert_statement(sql_line):
    """
    Parse a simple INSERT INTO statement and return a dict.
    Assumes format like:
    insert into schema.table ("name", "description", "price", "food_category") values ('Boiled Egg', 'snacks', '20', 'egg');
    """
    pattern = r'insert into .* \((.*?)\) values \((.*?)\);'
    match = re.match(pattern, sql_line.strip(), re.IGNORECASE)
    if not match:
        return None

    columns = [c.strip().strip('"') for c in match.group(1).split(',')]
    values = [v.strip().strip("'") for v in match.group(2).split(',')]

    # Convert price to int if column is price
    data = {}
    for col, val in zip(columns, values):
        if col.lower() == "price":
            val = int(val)
        data[col] = val
    return data

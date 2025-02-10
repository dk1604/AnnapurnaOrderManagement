import os

# db_type='mysql'
# host='localhost'
# port='3306'
# user='root'
# password='root'
# database='annapurna_caterers'

# local postgres
# db_type = 'postgres'
# host = '127.0.0.1'
# port = '61720'
# user = 'postgres'
# password = 'admin'
# database = 'canteen'

# render
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

db_type = os.getenv("db_type").lower()
host = "dpg-cul3akjqf0us738pqrh0-a.oregon-postgres.render.com"
port = "5432"
database = "menu_i8cw"
user = "root"
password = "HwVzJAZ12Okh827U3ErYVFUc5y4w3s2r"
internal_database_url = "postgresql://root:HwVzJAZ12Okh827U3ErYVFUc5y4w3s2r@dpg-cul3akjqf0us738pqrh0-a/menu_i8cw"
external_database_url = "postgresql://root:TYKxWnrB2utOK65pHKq0Xuh1YeDngwm8@dpg-ctk3halumphs73fe6i5g-a.oregon-postgres.render.com/menu_sjop"
psql_command = "PGPASSWORD=HwVzJAZ12Okh827U3ErYVFUc5y4w3s2r psql -h dpg-cul3akjqf0us738pqrh0-a.oregon-postgres.render.com -U root menu_i8cw"

time_to_nullify_session = os.getenv("time_to_nullify_session")
base_url = "https://annapurnaordermanagement.onrender.com"


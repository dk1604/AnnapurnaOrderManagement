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
db_type = os.getenv("db_type").lower()
host = "dpg-ctk3halumphs73fe6i5g-a"
port = "5432"
database = "menu_sjop"
user = "root"
password = "TYKxWnrB2utOK65pHKq0Xuh1YeDngwm8"
internal_database_url = "postgresql://root:TYKxWnrB2utOK65pHKq0Xuh1YeDngwm8@dpg-ctk3halumphs73fe6i5g-a/menu_sjop"
external_database_url = "postgresql://root:TYKxWnrB2utOK65pHKq0Xuh1YeDngwm8@dpg-ctk3halumphs73fe6i5g-a.oregon-postgres.render.com/menu_sjop"
psql_command = "PGPASSWORD=TYKxWnrB2utOK65pHKq0Xuh1YeDngwm8 psql -h dpg-ctk3halumphs73fe6i5g-a.oregon-postgres.render.com -U root menu_sjop"


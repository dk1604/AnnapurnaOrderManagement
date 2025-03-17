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
host = "dpg-cvc0stij1k6c73e3a1jg-a.oregon-postgres.render.com"
port = "5432"
database = "menu_y9ts"
user = "root"
password = "NfxfbIaVkRxd84n6NPR5wQjPouu4yvqW"
internal_database_url = "postgresql://root:NfxfbIaVkRxd84n6NPR5wQjPouu4yvqW@dpg-cvc0stij1k6c73e3a1jg-a/menu_y9ts"
external_database_url = "postgresql://root:NfxfbIaVkRxd84n6NPR5wQjPouu4yvqW@dpg-cvc0stij1k6c73e3a1jg-a.oregon-postgres.render.com/menu_y9ts"
psql_command = "PGPASSWORD=NfxfbIaVkRxd84n6NPR5wQjPouu4yvqW psql -h dpg-cvc0stij1k6c73e3a1jg-a.oregon-postgres.render.com -U root menu_y9ts"

time_to_nullify_session = os.getenv("time_to_nullify_session")
base_url = "https://annapurnaordermanagement.onrender.com"


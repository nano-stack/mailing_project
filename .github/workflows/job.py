import os
import snowflake.connector
import pandas as pd

# Leer variables de entorno definidas por los secrets de GitHub
user = os.environ["SNOWFLAKE_USER"]
password = os.environ["SNOWFLAKE_PASSWORD"]
account = os.environ["SNOWFLAKE_ACCOUNT"]
database = os.environ["SNOWFLAKE_DATABASE"]
warehouse = os.environ["SNOWFLAKE_WAREHOUSE"]

# Conexión inicial a Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    database=database,
    warehouse=warehouse,
)

# Consulta: Conteo de folios distintos
query = """
SELECT COUNT(DISTINCT FOLIO) AS total_folios_analizados
FROM OPX.P_DESA_OPX.FP_SII_SCRAPP_BHE_TODO
"""

try:
    df = pd.read_sql(query, conn)
    print(df)
finally:
    conn.close()

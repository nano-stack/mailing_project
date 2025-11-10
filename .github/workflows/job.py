import os
import snowflake.connector
import pandas as pd
import win32com.client
from datetime import datetime

# Leer secrets
user = os.environ["SNOWFLAKE_USER"]
password = os.environ["SNOWFLAKE_PASSWORD"]
account = os.environ["SNOWFLAKE_ACCOUNT"]
database = os.environ["SNOWFLAKE_DATABASE"]
warehouse = os.environ["SNOWFLAKE_WAREHOUSE"]
mail_to = os.environ["MAIL_TO"].split(",")
mail_from = os.environ["MAIL_FROM"]

# Conexión a Snowflake
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

# Ejecutar y guardar en DataFrame
df = pd.read_sql(query, conn)

# Cerrar conexión
conn.close()

# Exportar a Excel
archivo_excel = f"reporte_folios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(archivo_excel, index=False)

# Enviar correo con Outlook
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)
mail.To = "; ".join(mail_to)
mail.Subject = "Reporte de folios analizados"
mail.Body = "Adjunto reporte de conteo total de folios analizados."
mail.Attachments.Add(archivo_excel)
mail.Send()

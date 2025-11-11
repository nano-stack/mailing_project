import os
import snowflake.connector
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Leer secrets
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")  # Debe ser ISAPRE_COLMENA o isapre_colmena.us-east-1
database = os.getenv("SNOWFLAKE_DATABASE")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
mail_to = os.getenv("MAIL_TO").split(",")
mail_from = os.getenv("MAIL_FROM")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", 587))
smtp_password = os.getenv("SMTP_PASSWORD")

# Conexión a Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    database=database,
    warehouse=warehouse,
    schema=schema
)

# Consulta
query = """
SELECT COUNT(DISTINCT FOLIO) AS total_folios_analizados
FROM OPX.P_DESA_OPX.FP_SII_SCRAPP_BHE_TODO
"""

# Ejecutar y guardar en DataFrame
df = pd.read_sql(query, conn)
conn.close()

# Exportar a Excel
archivo_excel = f"reporte_folios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(archivo_excel, index=False)

# Enviar correo con SMTP
msg = MIMEMultipart()
msg['From'] = mail_from
msg['To'] = ", ".join(mail_to)
msg['Subject'] = "Reporte de folios analizados"
msg.attach(MIMEText("Adjunto reporte de conteo total de folios analizados.", 'plain'))

# Adjuntar archivo
with open(archivo_excel, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={archivo_excel}')
    msg.attach(part)

# Enviar correo
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(mail_from, smtp_password)
server.sendmail(mail_from, mail_to, msg.as_string())
server.quit()

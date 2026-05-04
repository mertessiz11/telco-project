import oracledb
import pandas as pd

conn = oracledb.connect(user="system", password="password123", dsn="localhost:1521/XE")
cursor = conn.cursor()

# CUSTOMERS import
df = pd.read_csv('CUSTOMERS.csv')
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO CUSTOMERS (CUSTOMER_ID, NAME, CITY, SIGNUP_DATE, TARIFF_ID)
        VALUES (:1, :2, :3, TO_DATE(:4, 'DD/MM/YYYY'), :5)
    """, (int(row['CUSTOMER_ID']), str(row['NAME']), str(row['CITY']), str(row['SIGNUP_DATE']), int(row['TARIFF_ID'])))

conn.commit()
print(f"CUSTOMERS: {len(df)} satır eklendi!")

# MONTHLY_STATS import
df2 = pd.read_csv('MONTHLY_STATS.csv')
for _, row in df2.iterrows():
    cursor.execute("""
        INSERT INTO MONTHLY_STATS (ID, CUSTOMER_ID, DATA_USAGE, MINUTE_USAGE, SMS_USAGE, PAYMENT_STATUS)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, (int(row['ID']), int(row['CUSTOMER_ID']), float(row['DATA_USAGE']), int(row['MINUTE_USAGE']), int(row['SMS_USAGE']), str(row['PAYMENT_STATUS'])))

conn.commit()
print(f"MONTHLY_STATS: {len(df2)} satır eklendi!")

cursor.close()
conn.close()
print("Tamamlandı!")
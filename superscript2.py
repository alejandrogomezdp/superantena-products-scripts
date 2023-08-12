import openai
import mysql.connector

openai.api_key = "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"

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
host="localhost",
user="phpmyadmin",
password="eminem92AA!!",
database="superantena_bd"
)

cursor = db.cursor()

# Recuperar los datos del producto
cursor.execute("SELECT name, description FROM neco_product_lang WHERE id_product = 3081 AND id_shop = 1 AND id_lang = 1")
product = cursor.fetchone()

# Generar la descripción del producto
response = openai.Completion.create(
engine="text-davinci-003",
prompt=f"Product Name: {product[0]}\nMeta Description: {product[1]}\n\nPlease write a product description that includes keywords, benefits, and h1, h2, h3 headers.",
max_tokens=900
)

# Actualizar la base de datos del producto
cursor.execute("UPDATE neco_product_lang SET description = %s WHERE id_product = 3081 AND id_shop = 1 AND id_lang = 1", (response.choices[0].text,))
db.commit()
import mysql.connector
import openai

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
  host="localhost",
  user="phpmyadmin",
  password="eminem92AA!!",
  database="superantena"
)

cursor = db.cursor()

# Recuperar los datos del producto
cursor.execute("SELECT description, description FROM products WHERE id = 1")
product = cursor.fetchone()

# Generar la descripción del producto
response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=f"Product Title: {product[0]}\nMeta Description: {product[1]}\n\nPlease write a 600 to 1000 word product description that includes keywords, benefits, and h1, h2, h3 headers.",
  max_tokens=1000
)

# Actualizar la base de datos del producto
cursor.execute("UPDATE products SET description = %s WHERE id = 1", (response.choices[0].text,))
db.commit()

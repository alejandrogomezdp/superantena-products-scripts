import openai
import mysql.connector

openai.api_key = "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"

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
host="localhost",
user="alejandro",
password="eminem92AA!!",
database="superantena_bd"
)

cursor = db.cursor()

# Recorrer los productos del ID 100 al 300 x e.j.
for product_id in range(40, 50):
    # Recuperar los datos del producto
    cursor.execute("SELECT name, description FROM neco_product_lang WHERE id_product = %s AND id_shop = 1 AND id_lang = 1", (product_id,))
    product = cursor.fetchone()

    if product is None:
        continue

    # Generar la descripción del producto
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Product Name: {product[0]}\{product[1]}\n\nPor favor escríbe una descripción de el producto, buscalo en internet, consigue la máxima información y haz la mejor descripción de producto y beneficios que puedas que incluya h1, h2, h3 y una imagen del producto. Escríbelo en html.",
    max_tokens=500
    )

    # Generar un título atractivo
    title_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Product Name: {product[0]}\nPor favor escríbe un titulo y meta-titulo atractivo para este producto haz que el meta-titulo y el titulo sean igual.",
    max_tokens=30
    )

    # Generar 7 beneficios en puntos cortos
    benefits_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Product Name: {product[0]}\nPor favor, enumera 7 beneficios breves de este producto, cada beneficio debe tener menos de 35 caracteres. En español un poco informal",
    max_tokens=70
    )

    # Generar palabras clave
    keywords_response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Product Name: {product[0]}\nPor favor, prediga las palabras clave que la gente va a buscar en google para encontrar este producto.",
    max_tokens=30
    )

    # Actualizar la base de datos del producto
    cursor.execute("UPDATE neco_product_lang SET description = %s, meta_title = %s, description_short = %s, meta_keywords = %s WHERE id_product = %s AND id_shop = 1 AND id_lang = 1", 
    (response.choices[0].text, title_response.choices[0].text, benefits_response.choices[0].text, keywords_response.choices[0].text, product_id))
    
    db.commit()

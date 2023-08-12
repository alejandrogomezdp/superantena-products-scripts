import openai
import mysql.connector
import time

# Nunca expongas directamente tus credenciales en el código.
# Considera usar un archivo de configuración o variables de entorno.
openai.api_key = "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"

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="alejandro",
    password="eminem92AA!!",
    database="superantena_bd"
)

cursor = db.cursor()

def call_openai(prompt, max_tokens, engine="text-davinci-003"):
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens
        )
        time.sleep(3)  # Retraso de 3 segundos para evitar llegar al límite de la API.
        return response.choices[0].text
    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return None

# Recorrer los productos del ID 40 al 50
for product_id in range(50, 68):
    try:
        # Recuperar los datos del producto
        cursor.execute("SELECT name, description FROM neco_product_lang WHERE id_product = %s AND id_shop = 1 AND id_lang = 1", (product_id,))
        product = cursor.fetchone()
        
        if product is None:
            continue

        # Hacer las llamadas a la API
        description_prompt = f"Product Name: {product[0]}\\{product[1]}\n\nPor favor escríbe una descripción del producto, buscalo en internet..."
        title_prompt = f"Product Name: {product[0]}\nPor favor escríbe un titulo atractivo..."
        benefits_prompt = f"Product Name: {product[0]}\nPor favor, enumera 7 beneficios breves de este producto..."
        keywords_prompt = f"Product Name: {product[0]}\nPor favor, prediga las palabras clave que la gente va a buscar..."
        meta_description = f"Product Name: {product[0]}\nPor favor, prediga la meta descripcion que posicione la página en las primeras posiciones en google..."


        description = call_openai(description_prompt, 500)
        title = call_openai(title_prompt, 30)
        benefits = call_openai(benefits_prompt, 70)
        keywords = call_openai(keywords_prompt, 30)
        meta_description = call_openai(keywords_prompt, 30)


        if all([description, title, benefits, keywords, meta_description]):  # Si todas las llamadas fueron exitosas
            cursor.execute("UPDATE neco_product_lang SET description = %s, meta_title = %s, description_short = %s, meta_keywords = %s, meta_description = %s WHERE id_product = %s AND id_shop = 1 AND id_lang = 1", 
                           (description, title, benefits, keywords, meta_description, product_id))
            db.commit()
    except Exception as e:
        print(f"Error al actualizar el producto con ID {product_id}: {e}")

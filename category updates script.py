import openai
import mysql.connector
import time

# Configuración inicial
openai.api_key = "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"

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
        time.sleep(3)  # Evita llegar al límite de la API.
        return response.choices[0].text
    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return None

# Actualización de Categorías
for category_id in range(1, 100):  # Modifica el rango según tus necesidades
    try:
        # Recuperar nombre de la categoría
        cursor.execute("SELECT name FROM neco_category_lang WHERE id_category = %s AND id_shop = 1 AND id_lang = 1", (category_id,))
        category = cursor.fetchone()

        if category is None:
            continue

        # Hacer las llamadas a la API
        description_prompt = f"Category Name: {category[0]}\nPor favor, escribe una extensa y buena redacción sobre lo que las personas encontrarán en esta categoría..."
        keywords_prompt = f"Category Name: {category[0]}\nPor favor, prediga las palabras clave más buscadas que permitan encontrar esta categoría..."
        meta_description_prompt = f"Category Name: {category[0]}\nPor favor, prediga la meta descripción adecuada que posicione esta categoría en las primeras posiciones en Google..."

        description = call_openai(description_prompt, 1000)
        keywords = call_openai(keywords_prompt, 70)
        meta_description = call_openai(meta_description_prompt, 160)  # 160 caracteres es el límite recomendado para las meta descripciones

        if all([description, keywords, meta_description]):
            cursor.execute("UPDATE neco_category_lang SET description = %s, meta_keywords = %s, meta_description = %s WHERE id_category = %s AND id_shop = 1 AND id_lang = 1", 
                           (description, keywords, meta_description, category_id))
            db.commit()
    except Exception as e:
        print(f"Error al actualizar la categoría con ID {category_id}: {e}")

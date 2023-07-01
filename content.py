import psycopg2
import random

DB_NAME = 'huwebshop'
USER = 'postgres'
password = 'kaas'
table_name = 'recommendations'
id = input('geef een id op: ')

num_recommendations = 4

def create_table(DB_NAME, USER, password, table_name):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, product_id VARCHAR, recommendation_id VARCHAR, description VARCHAR, discount INTEGER)")

    conn.commit()
    cur.close()
    conn.close()


def insert_recommendation(DB_NAME, USER, password, product_id, recommendation_id, description, discount):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()

    cur.execute(f"INSERT INTO {table_name} (product_id, recommendation_id, description, discount) VALUES (%s, %s, %s, %s)",
                (product_id, recommendation_id, description, discount))

    conn.commit()
    cur.close()
    conn.close()


def connect_to_database(DB_NAME, USER, password, id, num_recommendations):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    row = cur.fetchone()
    product_subsubcategory = row[6]
    product_brand = row[2]
    product_category = row[4]

    todo = "SELECT * FROM products WHERE subsubcategory = %s AND brand = %s AND category = %s AND id != %s"
    cur.execute(todo, (product_subsubcategory, product_brand, product_category, id))
    recommendations = cur.fetchall()

    if len(recommendations) > 0:
        chosen_recommendations = random.sample(recommendations, min(num_recommendations, len(recommendations)))
        for recommendation in chosen_recommendations:
            recommendation_id = recommendation[0]
            description = recommendation[1]
            discount = recommendation[9]

            insert_recommendation(DB_NAME, USER, password, id, recommendation_id, description, discount)
    else:
        print("Geen aanbevelingen beschikbaar.")

    cur.close()
    conn.close()





create_table(DB_NAME, USER, password, table_name)

connect_to_database(DB_NAME, USER, password, id, num_recommendations)

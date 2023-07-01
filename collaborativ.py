import psycopg2
import random

DB_NAME = 'huwebshop'
USER = 'postgres'
password = 'kaas'
table_name = 'recommendations'

def create_table(DB_NAME, USER, password, table_name):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, product_id VARCHAR, recommendation_id VARCHAR, description VARCHAR)")
    conn.commit()
    cur.close()
    conn.close()


def insert_recommendation(DB_NAME, USER, password, product_id, recommendation_id, description):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (product_id, recommendation_id, description) VALUES (%s, %s, %s, %s)",(product_id, recommendation_id, description))
    conn.commit()
    cur.close()
    conn.close()



def connect_to_database(DB_NAME, USER, password, id, num_recommendations):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles_previously_viewed WHERE prodid = %s", (id,))
    rows = cur.fetchall()
    
    viewed_product_ids = [row[1] for row in rows]
    
    todo = "SELECT * FROM profiles_previously_viewed WHERE prodid != %s AND prodid = ANY(%s)"
    cur.execute(todo, (id, viewed_product_ids))
    recommendations = cur.fetchall()
    
    if len(recommendations) > 0:
        chosen_recommendations = random.sample(recommendations, min(num_recommendations, len(recommendations)))
        for recommendation in chosen_recommendations:
            recommendation_id = recommendation[1]
            description = recommendation[2]
            insert_recommendation(DB_NAME, USER, password, id, recommendation_id, description)
    else:
        print("Geen aanbevelingen beschikbaar.")

    cur.close()
    conn.close()

id = input('geef een product id op: ')
num_recommendations = 4

create_table(DB_NAME, USER, password, table_name)

connect_to_database(DB_NAME, USER, password, id, num_recommendations)

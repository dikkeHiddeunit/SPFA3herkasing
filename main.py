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
    cur.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, product_id VARCHAR, description VARCHAR)")
    conn.commit()
    cur.close()
    conn.close()


def insert_recommendation(DB_NAME, USER, password, product_id, description):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (product_id, description) VALUES (%s, %s)", (product_id, description))
    conn.commit()
    cur.close()
    conn.close()


def content_based_filtering(DB_NAME, USER, password, id, num_recommendations):
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
            insert_recommendation(DB_NAME, USER, password, recommendation_id, description)
            print(f"Aanbevolen product ID: {recommendation_id}")
            print(f"Beschrijving: {description}")
            print("------------------------------")
    else:
        print("Geen aanbevelingen beschikbaar.")

    cur.close()
    conn.close()

def collaborative_filtering(DB_NAME, USER, password, id, num_recommendations):
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{USER}' host='localhost' password='{password}'")
    cur = conn.cursor()
    cur.execute("SELECT profid FROM profiles_previously_viewed WHERE prodid = %s", (id,))
    rows = cur.fetchall()

    viewed_profiles = [row[0] for row in rows]

    if len(viewed_profiles) > 0:
        todo = "SELECT DISTINCT prodid FROM profiles_previously_viewed WHERE profid != %s AND profid = ANY(%s)"
        cur.execute(todo, (viewed_profiles[0], viewed_profiles))
        recommendations = cur.fetchall()

        if len(recommendations) > 0:
            chosen_recommendations = random.sample(recommendations, min(num_recommendations, len(recommendations)))
            for recommendation in chosen_recommendations:
                recommendation_id = recommendation[0]
                cur.execute("SELECT * FROM products WHERE id = %s", (recommendation_id,))
                product_row = cur.fetchone()
                description = product_row[1]
                insert_recommendation(DB_NAME, USER, password, recommendation_id, description)
                print(f"Aanbevolen product ID: {recommendation_id}")
                print(f"Beschrijving: {description}")
                print("------------------------------")
        else:
            print("Geen aanbevelingen beschikbaar.")
    else:
        print("Geen aanbevelingen beschikbaar.")

    cur.close()
    conn.close()



choice = input("Kies de filteringsoptie (content/collaborative): ")
if choice == "collaborative" or choice == "content":
    id = input("Geef een product ID op: ")
else:
    print("fout")
    exit()

num_recommendations = 4

create_table(DB_NAME, USER, password, table_name)

if choice == "content":
    content_based_filtering(DB_NAME, USER, password, id, num_recommendations)
elif choice == "collaborative":
    collaborative_filtering(DB_NAME, USER, password, id, num_recommendations)


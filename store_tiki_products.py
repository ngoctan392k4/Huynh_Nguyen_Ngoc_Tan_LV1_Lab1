import psycopg2
from config import load_config
import os
import json

def insert_data():
    config = load_config()
    sql = """INSERT INTO products (id, name, url_key, price, description, images)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                # List all file in output folder
                for file in os.listdir('output'):
                    # check if the file is json type or not
                    if file.endswith('.json'):
                        path = os.path.join('output', file)
                        try: # Exception Handling when opening and reading
                            with open (path, "r", encoding='utf-8') as readfile:
                                products = json.load(readfile)
                                for product in products:
                                    try: # Exception Handling when inserting products into database
                                        cur.execute(sql, (product.get("id"),
                                                product.get("name"),
                                                product.get("url_key"),
                                                product.get("price"),
                                                product.get("description"),
                                                product.get("images")))
                                    except (psycopg2.DatabaseError, Exception) as insert_err:
                                        print(f"Error when inserting product ID {product.get("id")}")
                                conn.commit()
                        except (json.JSONDecodeError) as j_err:
                            print(f"Error when opening and reading {path}: {j_err}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":
    insert_data() # call insert function to insert all data into the table in DTB

    # check the number of data in the table: expected output: 198942
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                select* from products;
                            """)
                rows = cur.rowcount
                print(rows)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

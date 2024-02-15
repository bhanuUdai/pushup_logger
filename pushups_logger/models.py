import psycopg2
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, email, password, name):
        self.id = user_id
        self.email = email
        self.password = password
        self.name = name
        
def get_user_by_id(user_id):
    # Implement the logic to retrieve a user by ID from your database
    # Use psycopg2 or your preferred database library

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()

            if user_data:
                return User(user_data[0], user_data[1], user_data[2], user_data[3])

    return None

def get_db_connection():
    return psycopg2.connect(database="push_up",
                        user="udaibhanu",
                        password="Bhanu@26",
                        host="localhost", port="5432")

def close_db_connection(conn, cur):
    cur.close()
    conn.close()

# conn = psycopg2.connect(database="push_up",
#                         user="udaibhanu",
#                         password="Bhanu@26",
#                         host="localhost", port="5432")

# cur = conn.cursor()

# cur.execute("SELECT * FROM users")
# print(cur.fetchall())

# conn.commit()

# cur.close()
# conn.close()



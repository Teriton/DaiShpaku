import psycopg2
from psycopg2 import Error



def connect_to_database() -> int:
    try:
        # Connect to an existing database
        global connection
        connection = psycopg2.connect(user="postgres",
                                    password="dai-shpaku",
                                    host="db",
                                    port="5432",
                                    database="daishpakudb")

        # Create a cursor to perform database operations
        global cursor
        cursor = connection.cursor()

        return 0

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return -1

def close_db_connection():
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def show_users():
    cursor.execute("SELECT * FROM users")
    record = cursor.fetchall()
    print("Result ", record)

def add_user(name: str, bio: str,user_tg_id:str, gender:str):
    insert_query = """INSERT INTO users(name,user_tg_id,bio,gender) VALUES ('{}','{}','{}','{}');""".format(name,user_tg_id,bio,gender)
    cursor.execute(insert_query)
    connection.commit()
    print("User has been added!")

def who_wants_to_fuck(user_id: int) -> int:
    try:
        select_query = """SELECT u.user_id, u.name FROM users u JOIN relations r ON u.user_id = r.sender_id WHERE r.reciever_id = {};""".format(user_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        # print("Result ", record)
        return 0
    except (Exception, Error) as error:
        print("who_wants_to_fuckm", error)
        return -1

def check_upvote(sender_id:int, reciever_id:int) -> int:
    try:
        select_query = """SELECT * FROM relations WHERE sender_id={} AND reciever_id={};""".format(sender_id,reciever_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return len(record)
    except (Exception, Error) as error:
        print("upvote", error)
        return -1

def upvote(sender_id:int, reciever_id:int) -> int:
    try:
        insert_query = """INSERT INTO relations(sender_id, reciever_id) VALUES ({},{});""".format(sender_id,reciever_id)
        cursor.execute(insert_query)
        connection.commit()
        # print("Nice try!")
        return 0
    except (Exception, Error) as error:
        print("upvote", error)
        return -1

def delete_upvote(sender_id:int, reciever_id:int) -> int:
    try:
        insert_query = """DELETE FROM relations WHERE sender_id={} AND reciever_id={};""".format(sender_id,reciever_id)
        cursor.execute(insert_query)
        connection.commit()
        # print("Sectore clear")
        return 0
    except (Exception, Error) as error:
        print("upvote", error)
        return -1

def get_random_user(gender:str):
    try:
        select_query = """SELECT * FROM users WHERE gender='{}' ORDER BY random() LIMIT 1;""".format(gender)
        if gender == "A":
            select_query = """SELECT * FROM users ORDER BY random() LIMIT 1;"""
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record
    except (Exception, Error) as error:
        print("get_random_user", error)
        return []
    
def check_user(user_name:str) -> int:
    try:
        select_query = """SELECT * FROM users WHERE user_tg_id='{}';""".format(user_name)
        cursor.execute(select_query)
        record = cursor.fetchall()
        # print("Result ", record)
        if (len(record) == 1):
            return 0
        else:
            return 1
    except (Exception, Error) as error:
        print("check_user", error)
        return -1

def update_name(user_tg_id:str,name:str):
    try:
        update_query = """UPDATE users SET name='{}' WHERE user_tg_id='{}';""".format(name,user_tg_id)
        cursor.execute(update_query)
        connection.commit()
        # print("Bio updated!")
    except (Exception, Error) as error:
        print("update_bio", error)
        return -1

def update_gender(user_tg_id:str,gender:str):
    try:
        update_query = """UPDATE users SET gender='{}' WHERE user_tg_id='{}';""".format(gender,user_tg_id)
        if gender == "M":
            update_query += """UPDATE users SET interested_in_gender='F' WHERE user_tg_id='{}';""".format(user_tg_id)
        if gender == "F":
            update_query += """UPDATE users SET interested_in_gender='M' WHERE user_tg_id='{}';""".format(user_tg_id)
        cursor.execute(update_query)
        connection.commit()
        # print("Gender updated!")
    except (Exception, Error) as error:
        print("update_gender", error)
        return -1
    
def update_interested_in_gender(user_tg_id:str,gender:str):
    try:
        update_query = """UPDATE users SET interested_in_gender='{}' WHERE user_tg_id='{}';""".format(gender,user_tg_id)
        cursor.execute(update_query)
        connection.commit()
        # print("Gender updated!")
    except (Exception, Error) as error:
        print("update_gender", error)
        return -1
    
def update_current_user(user_tg_id:str,current_user:str):
    try:
        update_query = """UPDATE users SET current_user_id='{}' WHERE user_tg_id='{}';""".format(current_user,user_tg_id)
        cursor.execute(update_query)
        connection.commit()
    except (Exception, Error) as error:
        print("update_current_user", error)
        return -1

def update_bio(user_tg_id:str,bio:str):
    try:
        update_query = """UPDATE users SET bio='{}' WHERE user_tg_id='{}';""".format(bio,user_tg_id)
        cursor.execute(update_query)
        connection.commit()
        # print("Bio updated!")
    except (Exception, Error) as error:
        print("update_bio", error)
        return -1
    
def get_id_by_tg_id(user_tg_id:str):
    try:
        select_query = """SELECT user_id FROM users WHERE user_tg_id='{}';""".format(user_tg_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record[0][0]
    except (Exception, Error) as error:
        print("get_id_by_tg_id", error)
        return -1
    
def get_tg_id_by_id(user_id:str):
    try:
        select_query = """SELECT user_tg_id FROM users WHERE user_id='{}';""".format(user_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record[0][0]
    except (Exception, Error) as error:
        print("get_id_by_tg_id", error)
        return -1
    
def get_current_user_by_tg_id(user_tg_id:str):
    try:
        select_query = """SELECT current_user_id FROM users WHERE user_tg_id='{}';""".format(user_tg_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record[0][0]
    except (Exception, Error) as error:
        print("get_current_user_by_tg_id", error)
        return -1
    
def get_list_interested_users(user_id:str):
    try:
        select_query = """SELECT * FROM relations r INNER JOIN users u ON u.user_id=r.sender_id WHERE r.reciever_id={};""".format(user_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record
    except (Exception, Error) as error:
        print("get_current_user_by_tg_id", error)
        return -1
    
def get_interested_in_gender_by_tg_id(tg_id:str):
    try:
        select_query = """SELECT interested_in_gender FROM users WHERE user_tg_id='{}';""".format(tg_id)
        cursor.execute(select_query)
        record = cursor.fetchall()
        return record[0][0]
    except (Exception, Error) as error:
        print("get_interested_in_gender_by_tg_id", error)
        return -1
    
connect_to_database()
import pymysql

def connect_to_user_info_database():
    """Connect to the MySQL database and return the connection object."""
    try:
        db = pymysql.connect(
            host='localhost',
            user='recipe-recommend-db-manager',
            port=3306,
            password='12345',
            database='recipe-recommend-db'
        )
        print("Connection to the database was successful.")
        return db
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def add_user(user_id, user_name, user_password):
    """Add a new user to the database."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO `user-info` (`user-id`, `user-name`, `user-password`) VALUES (%s, %s, %s)",
                (user_id, user_name, user_password)
            )
            db.commit()
            print("User added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding user: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
def get_all_users():
    """Retrieve all users from the database."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM `user-info`")
            users = cursor.fetchall()
            print(users)
            print(type(users))
            return users
        except pymysql.MySQLError as e:
            print(f"Error retrieving users: {e}")
            return []
        finally:
            cursor.close()
            db.close()
            
if __name__ == "__main__":
    pass
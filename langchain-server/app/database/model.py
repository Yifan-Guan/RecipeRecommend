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
            return users
        except pymysql.MySQLError as e:
            print(f"Error retrieving users: {e}")
            return []
        finally:
            cursor.close()
            db.close()
            
def get_all_history_info():
    """Retrieve all history information from the database."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM `chat-history-info`")
            history_info = cursor.fetchall()
            print(history_info)
            return history_info
        except pymysql.MySQLError as e:
            print(f"Error retrieving history info: {e}")
            return []
        finally:
            cursor.close()
            db.close()

def get_history_content_by_id(history_id):
    """Retrieve history content by history ID."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM `chat-history-content` WHERE `history-id` = %s ORDER BY `message-index`", (history_id,))
            history_content = cursor.fetchall()
            print(history_content)
            return history_content
        except pymysql.MySQLError as e:
            print(f"Error retrieving history content: {e}")
            return None
        finally:
            cursor.close()
            db.close()
            
def add_history_info(history_id, history_name, user_id):
    """Add history information to the database."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO `chat-history-info` (`chat-history-id`, `chat-history-name`, `chat-user-id`) VALUES (%s, %s, %s)",
                (history_id, history_name, user_id)
            )
            db.commit()
            print("History info added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding history info: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
def add_history_content(id, index, role, content):
    """Add history content to the database."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO `chat-history-content` (`history-id`, `message-index`, `message-role`, `message-content`) VALUES (%s, %s, %s, %s)",
                (id, index, role, content)
            )
            db.commit()
            print("History content added successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding history content: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
def delete_history_info(history_id):
    """Delete history information by history ID."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM `chat-history-content` WHERE `history-id` = %s", (history_id,))
            db.commit()
            print("History content deleted successfully.")
            cursor.execute("DELETE FROM `chat-history-info` WHERE `chat-history-id` = %s", (history_id,))
            db.commit()
            print("History info deleted successfully.")
        except pymysql.MySQLError as e:
            print(f"Error deleting history info: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
def update_history_name_by_id(history_id, new_name):
    """Update history name by history ID."""
    db = connect_to_user_info_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE `chat-history-info` SET `chat-history-name` = %s WHERE `chat-history-id` = %s", (new_name, history_id))
            db.commit()
            print("History name updated successfully.")
        except pymysql.MySQLError as e:
            print(f"Error updating history name: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()
            
if __name__ == "__main__":
    add_history_info("12345", "Test History", "user1")
    add_history_content("12345", 1, "user", "This is a test message.")
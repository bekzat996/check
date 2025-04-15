# import sqlite3

# class DatabaseManager:
#     def __init__(self, db_path):
#         self.db_path = db_path
#         self.connection = None
#         self.cursor = None

#     def open_connection(self):
#         try:
#             self.connection = sqlite3.connect(self.db_path)
#             self.cursor = self.connection.cursor()
#             print("Соединение с базой данных открыто.")
#         except sqlite3.Error as e:
#             print(f"Ошибка при подключении к базе данных: {e}")

#     def close_connection(self):
#         if self.cursor:
#             self.cursor.close()
#         if self.connection:
#             self.connection.close()
#             print("Соединение с базой данных закрыто.")
            
            
            
import sqlite3

class User:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        self.connection.commit()

    def add_user(self, name, email):
        try:
            self.cursor.execute('''
                INSERT INTO users (name, email)
                VALUES (?, ?)
            ''', (name, email))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Ошибка добавления пользователя: {e}")
            return None

    def get_user_by_id(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "email": row[2]}
        return None

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.connection.commit()
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()
        self.connection.close()
if __name__ == "__main__":
    user_manager = User("my_database.db")

    new_id = user_manager.add_user("А.С. Пушкин", "push@mail.com")
    print(f"Добавлен пользователь с ID: {new_id}")

    user = user_manager.get_user_by_id(new_id)
    print("Полученный пользователь:", user)

    deleted = user_manager.delete_user(new_id)
    print(f"Удалено пользователь: {deleted}")
    user_manager.close()
    
"""Реализуйте классы Admin и Customer, которые будут наследовать от класса User. Добавьте дополнительные поля для каждой роли и методы
для работы с соответствующими таблицами admins и customers."""

class Admin(User):
    def __init__(self, db_path):
        super().__init__(db_path)
        self._create_admin_table()

    def _create_admin_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                role TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def add_admin(self, name, email, role):
        user_id = self.add_user(name, email)
        if user_id:
            self.cursor.execute('''
                INSERT INTO admins (user_id, role)
                VALUES (?, ?)
            ''', (user_id, role))
            self.connection.commit()
        return user_id

    def get_admin_by_id(self, user_id):
        self.cursor.execute('''
            SELECT users.id, users.name, users.email, admins.role
            FROM users
            JOIN admins ON users.id = admins.user_id
            WHERE users.id = ?
        ''', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3]
            }
        return None

    def delete_admin(self, user_id):
        return self.delete_user(user_id)


class Customer(User):
    def __init__(self, db_path):
        super().__init__(db_path)
        self._create_customer_table()

    def _create_customer_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                user_id INTEGER PRIMARY KEY,
                address TEXT,
                phone TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def add_customer(self, name, email, address, phone):
        user_id = self.add_user(name, email)
        if user_id:
            self.cursor.execute('''
                INSERT INTO customers (user_id, address, phone)
                VALUES (?, ?, ?)
            ''', (user_id, address, phone))
            self.connection.commit()
        return user_id

    def get_customer_by_id(self, user_id):
        self.cursor.execute('''
            SELECT users.id, users.name, users.email, customers.address, customers.phone
            FROM users
            JOIN customers ON users.id = customers.user_id
            WHERE users.id = ?
        ''', (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "address": row[3],
                "phone": row[4]
            }
        return None

    def delete_customer(self, user_id):
        return self.delete_user(user_id)
    
if __name__ == "__main__":
    db_path = "my_database.db"

    print("=== Admin ===")
    admin = Admin(db_path)
    admin_id = admin.add_admin("Bekzat", "bekzat@admin.com", "admin")
    print("Admin added:", admin.get_admin_by_id(admin_id))

    print("=== Customer ===")
    customer = Customer(db_path)
    cust_id = customer.add_customer("Uran", "uranus@mail.com", "ул. Буркан 45", "+996 558-979-754")
    print("Customer added:", customer.get_customer_by_id(cust_id))

    # admin.delete_admin(admin_id)
    # customer.delete_customer(cust_id)

    admin.close()
    customer.close()


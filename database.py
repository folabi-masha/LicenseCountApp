import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("init.db")
        self.cursor = self.conn.cursor()

    def create_database(self):
        return self.conn

    def load(self):
        products = """CREATE TABLE if not exists products (
                        product_id integer PRIMARY KEY AUTOINCREMENT, 
                        product_name text NOT NULL UNIQUE, 
                        allowance integer NOT NULL)"""

        licenses = """CREATE TABLE if not exists active_licenses (
                        id integer PRIMARY KEY AUTOINCREMENT, 
                        product_name text NOT NULL, 
                        name text NOT NULL UNIQUE, 
                        FOREIGN KEY (product_name) REFERENCES products(product_name))"""

        self.cursor.execute(products)
        self.cursor.execute(licenses)

    # def default_selection(self):
    #     default_select = "INSERT OR IGNORE INTO products (product_name, allowance) VALUES ('Select Software', 0)"
    #
    #     self.cursor.execute(default_select)
    #
    #     self.conn.commit()

    def add_software(self, software, allowance):
        entry = (software, allowance)

        add_product = "INSERT OR IGNORE INTO products (product_name, allowance) VALUES (?, ?)"

        self.cursor.execute(add_product, entry)

        self.conn.commit()

    def add_user(self, software, user):
        entry = (software, user)

        add_product = "INSERT OR IGNORE INTO active_licenses (product_name, name) VALUES (?, ?)"

        self.cursor.execute(add_product, entry)

        self.conn.commit()

    def show_licenses(self, software):
        add_product = "SELECT * FROM products"

        self.cursor.execute(add_product)

        allowance = self.cursor.fetchall()

        for sw in allowance:
            if sw[1] == software:
                default_allowance = sw[2]
                return default_allowance

    def show_software(self):
        self.cursor.execute("SELECT product_name FROM products")

        softwares = self.cursor.fetchall()

        software_list = []

        for sw in softwares:
            software_list.append(sw[0])

        return software_list

    def show_users(self, software):
        self.cursor.execute("SELECT * FROM active_licenses")

        softwares = self.cursor.fetchall()

        users = []

        for sw in softwares:
            if sw[1] == software:
                users.append(sw[2])

        return users

    def remaining_licenses(self, software):
        add_product = "SELECT product_name FROM active_licenses"

        self.cursor.execute(add_product)

        allowance = self.cursor.fetchall()

        counter = 0

        for sw in allowance:
            if sw[0] == software:
                counter += 1

        return counter

    def delete_user(self, name):
        delete = (name,)

        delete_user = "DELETE FROM active_licenses WHERE name = ?"

        self.cursor.execute(delete_user, delete)

        self.conn.commit()

    def delete_software(self, software):
        delete = (software,)

        delete_user = "DELETE FROM active_licenses WHERE product_name = ?"
        delete_software = "DELETE FROM products WHERE product_name = ?"

        self.cursor.execute(delete_user, delete)
        self.cursor.execute(delete_software, delete)

        self.conn.commit()

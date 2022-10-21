import sqlite3


class DbManager:
    def __init__(self, database: str):
        self.database = database
        self.con = sqlite3.connect(self.database)
        self.update_availability()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

    def columns_names(self, table_name: str) -> list:
        columns = []
        for column in self.con.execute(f"SELECT * from {table_name}").description:
            columns.append(column[0].capitalize())
        return columns

    def count(self, table_name, count='columns') -> int:
        if count == 'columns':
            return len(self.columns_names(table_name))
        elif count == 'rows':
            return len(self.con.execute(f"SELECT * from {table_name}").fetchall())

    def product_is_available(self, product_id: int) -> bool:
        av = self.con.execute("SELECT availability FROM Products WHERE product_id = ?", (product_id,)).fetchone()[0]
        if av == 'Available':
            return True
        return False

    def update_availability(self):
        self.con.execute("UPDATE Products set availability = 'Un Available' where stock = 0 ")
        self.commit()

    def add_product(self, product_id: int, product_name: str, stock=None, price=None, manufacture="unknown",
                    availability='Available', statue='add new') -> None:
        if statue == 'add new':
            try:
                self.con.execute(
                        "insert into Products (product_id, name, stock, price, manufacture, availability) values (?,?,?,?,?,?)",
                        (product_id, product_name, stock, price, manufacture, availability))
                print('added successfully')
            except sqlite3.IntegrityError:
                pass
        else:
            self.con.execute(
                    "update Products set (name, stock, manufacture, availability) = (?,?,?,?) where product_id = ?",
                    (product_name, stock, manufacture, availability, product_id))
            print('updated successfully')
        self.commit()

    def sell_product(self, product_id: int, quantity: int) -> str:
        stock = self.con.execute("SELECT stock FROM Products WHERE product_id = ?", (product_id,)).fetchone()[0]
        if self.product_is_available(product_id):
            if stock < quantity:
                print('no enough products in stock')
                return "error1"
            else:
                self.con.execute("UPDATE products set stock = ? where product_id = ?", (stock - quantity, product_id))
                self.update_availability()
                print('successfully sell')
            self.commit()
        else:
            print('this product not available')
            return "error2"

    def remove_product(self, product_id: int) -> None:
        q = self.con.execute("delete from Products where product_id = ?", (product_id,))

    def all_data(self, table_name) -> list:
        return self.con.execute(f"select * from {table_name}").fetchall()

    def search(self, pattern: str):
        return self.con.execute(f"SELECT * FROM Products where name like '%{pattern}%'").fetchall()

    def filter(self, table_name: str, filter='available') -> list:
        if filter == 'available':
            return self.con.execute(f"SELECT * FROM {table_name} WHERE availability = 'Available'").fetchall()
        if filter == 'un available':
            return self.con.execute(f"SELECT * FROM {table_name} WHERE availability = 'Un Available'").fetchall()

    def product_details(self, primary_key, column_name):
        # print(self.con.execute(f"SELECT {column_name} from Products where product_id = {primary_key}").fetchone()[0])
        return self.con.execute(f"SELECT {column_name} from Products where product_id = {primary_key}").fetchone()[0]

    # Customers methods

    def add_member(self, member_name: str) -> None:
        self.con.execute("insert into Customers (member_id, member) values (?)", (member_name,))
        print('added successfully')
        self.commit()

    def add_product_to_member(self, member_id, product_id, quantity):
        member = self.con.execute(f"select member from Customers where member_id = {member_id}").fetchone()[0]
        product = self.product_details(product_id, 'name')
        price = self.product_details(product_id, 'price')
        self.con.execute("insert into Customers(member_id, member, product_id, product, quantity, price) "
                         "values(?,?,?,?,?,?)", (member_id, member, product_id, product, quantity, price))

    def total_member_payments(self, member_id):
        return sum(self.con.execute("select price from member where member_id = ?", (member_id,)).fetchall()[0])

    def get_member_details(self, member_name=None, data_type='name') -> str | list:
        if data_type == 'name':
            print(self.con.execute("select member from Customers").fetchall())
            return self.con.execute("select member from Customers").fetchall()
        elif data_type == 'id':
            print(self.con.execute("select member_id from Customers where member = ?", (member_name,)).fetchone()[0])
            return self.con.execute("select member_id from Customers where member = ?", (member_name,)).fetchone()[0]

    # statistics

    def statistics(self) -> dict:
        stats_dic = {}
        stats_dic['All Products'] = len(self.con.execute("select * from Products").fetchall())
        stats_dic['All customers'] = len(self.con.execute("select * from Customers").fetchall())
        stats_dic['Total price of all products'] = sum(
                [price for i in self.con.execute("select price from Products").fetchall() for price in i])
        return stats_dic


if __name__ == '__main__':
    myDb = DbManager('database.sqlite3')
    myDb.add_product(4545, 'a12', 5, 'samsung', 'Available', statue='exist')
    # print(myDb.product_is_available(4545))
    # myDb.sell_product(4545, 1)
    print(myDb.columns_names('Products'))
    myDb.all_data()
    myDb.close()

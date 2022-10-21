import db_manager

db = db_manager.DbManager('database.sqlite3')

with open(r'C:\Users\20106\Desktop\Sales_September_2019.csv') as file:
    file.readline()
    file.readline()
    for line in file.readlines():
        print(line)
        split = line.split(',')
        print(split)
        db.add_product(product_id=int(split[0]),
                       product_name=split[1],
                       stock=int(split[2]),
                       price=int(float(split[3])))

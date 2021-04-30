import pyodbc
from config import *
import random
import mysql.connector

def number_gen(size=9):
    return random.randint(10**(size-1), (10**size)-1)

# Regresa una seleccion random de un archivo
def file_gen(cat):
    with open(f"{cat}.txt", errors="ignore") as space:
        space = space.readlines()
        return random.choice(space)

# Genera datos de personas random, para clientes y empleados
def person_gen():
    with open('people.txt', errors="ignore") as f:
        for line in f.readlines():
            name = line.split(', ')
            if len(name) < 2:
                name.extend(['Smith', 'Dickson'])
            yield { 
                'zipcode': number_gen(),
                'name': name,
                'title': random.choice(['Mr.', 'Mrs.', 'Dr.', 'Ing.', 'Lic.']),
                'city': file_gen('cities'),
                'state': 'Georgia',
                'phone': str(number_gen(10))
            }

# genera Datos de libros, al azar de el archivo books.txt
def book_gen():
    with open('books.txt', errors="ignore") as f:
        for line in f.readlines():
            num = ''.join(list(str(number_gen(13))))
            data = line.split('-')
            yield {
                'title': data[0],
                'isbn': num,
                'year': data[2],
                'author': data[1],
                'price': num[-3:],
                'pages': num[:3],
                'description': random.choice(['Good', 'Bad', 'Decent', 'Mint'])
            }
    
def main():
    # Barnes and Nobles Data
    conn = pyodbc.connect(winsql['string']+"DATABASE=BarnesNoble;", autocommit=True)
    cur = conn.cursor()

    # Definir datos "Estaticos"
    i = 0
    categories = ['Mysteries', 'Romance', 'Thrillers', 'Science Fiction', 'Fantasy', 'Historical Fiction']
    for cat in categories:
        cur.execute(f"INSERT INTO Category (CategoryId, CategoryDescription) VALUES ({i}, '{cat}')")
        i += 1

    i = 0
    for b in book_gen():
        category = random.randint(0,len(categories)-1)
        querys = [
            f"INSERT INTO Author (AuthorId, AuthorName) VALUES ({i}, '{b['author']}');",
            f"INSERT INTO Book (BookId, CategoryId, Title, isbn, year, price, nopages, bookdescription) VALUES ({i},{category}, '{b['title']}','{b['isbn']}','{b['year']}',{b['price']},{b['pages']},'{b['description']}')",
            f"INSERT INTO Author_Book (AuthorId, BookId) VALUES ({i}, {i});"]

        for q in querys:
            cur.execute(q)
        i += 1
    
    i = 0
    for p in person_gen():
        cur.execute(f"INSERT INTO Customer (CustomerId, FirstName, LastName, ZipCode, City, State) VALUES ({i}, '{p['name'][1]}', '{p['name'][0]}', '{p['zipcode']}', '{p['city']}', '{p['state']}');")
        i += 1

    cur.close()
    conn.close()

    # Eluktronics Data
    conn = mysql.connector.connect(
        host=sql['host'],
        user=sql['user'],
        password=sql['password'],
        database='eluktronics'
    )

    cur = conn.cursor()

    # definir datos "Estaticos"
    payments = ['Cash', 'Check', 'Credit Card', 'Debit Card']
    brands = {
        'eluktronics': ['RP15', 'RP17'],
        'hp': ['Surface', 'Omen'],
    }
    shipping = ['dhl', 'fedex', 'fedex priority', 'ups', 'usps']

    i = 0
    for pay in payments:
        cur.execute(f"INSERT INTO Payment_Method (PaymentMethodId, PaymentMethod) VALUES ({i}, '{pay}')")
        i += 1
    
    i = 0
    for ship in shipping:
        cur.execute(f"INSERT INTO Shipping_Methods (ShippingMethodId, ShippingMethod) VALUES ({i}, '{ship}')")
        i += 1

    i = 0
    j = 0
    for name, prods in brands.items():
        cur.execute(f"INSERT INTO Brands (BrandId, BrandDescription) VALUES ({i}, '{name}')")
        conn.commit()
        for prod in prods:
            cur.execute(f"INSERT INTO Products (ProductId, BrandId, ProductName) VALUES ({j}, {i}, '{prod}')")
            j += 1
        i += 1
    
    i = 0
    for p in person_gen():
        cur.execute(f"INSERT INTO Customers (CustomerId, ContactName, CompanyName, City, State, PostalCode, PhoneNumber) VALUES ({i}, '{p['name'][1][0:40]}', '{p['name'][0][0:40]}', '{p['city']}', '{p['state']}', '{p['zipcode']}', '{p['phone']}');")
        i += 1
    
    i = 0
    for p in person_gen():
        cur.execute(f"INSERT INTO Employees (EmployeeId, FirstName, LastName, Title, WorkPhone) VALUES ({i}, '{p['name'][1][0:40]}', '{p['name'][0][0:40]}', '{p['title']}', '{p['phone']}');")
        i += 1

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
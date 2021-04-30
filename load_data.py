import pyodbc
from config import *
import random
import mysql.connector
from datetime import datetime  
from datetime import timedelta

# Barnes And Noble data
conn = pyodbc.connect(winsql['string']+"DATABASE=BarnesNoble;", autocommit=True)
cur = conn.cursor()

# Sacar numero de datos para sacar ids siguientes y elegir al azar Books y Clients
cur.execute("Select count(*) from Book;")
books = cur.fetchone()[0]
cur.execute("Select count(*) from Customer;")
customers = cur.fetchone()[0]
cur.execute("Select count(*) from Book_Order;")
orders = cur.fetchone()[0]

n = 100 if flag_100 else 5
date = datetime.now()

for _ in range(n):
    orders += 1
    customer = random.randint(0, customers-1)
    time = date.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(f"INSERT INTO Book_Order (OrderId, CustomerId, OrderDate) VALUES ({orders}, {customer}, '{time}')")
    book = random.randint(0, books-1)
    cur.execute(f"Select Price from Book where BookId = {book}")
    price = cur.fetchone()[0]

    cur.execute(f"INSERT INTO Ordering (BookId, OrderId, Price) VALUES ({book}, {orders}, {price})")
    date = datetime.now() + timedelta(days=1)

cur.close() # Cerrar Conexion
conn.close()

# Eluktronics data
conn = mysql.connector.connect(
        host=sql['host'],
        user=sql['user'],
        password=sql['password'],
        database='eluktronics'
    )
cur = conn.cursor(buffered=True)

cur.execute("Select count(*) from Shipping_Methods;")
shipping = cur.fetchone()[0]
cur.execute("Select count(*) from Payment_Method;")
payments = cur.fetchone()[0]
cur.execute("Select count(*) from Products;")
products = cur.fetchone()[0]
cur.execute("Select count(*) from Employees;")
employees = cur.fetchone()[0]
cur.execute("Select count(*) from Customers;")
customers = cur.fetchone()[0]
cur.execute("Select count(*) from Orders;")
orders = cur.fetchone()[0]

n = 100 if flag_100 else 5
date = datetime.now()

for _ in range(n):
    orders += 1
    customer = random.randint(0, customers-1)
    employee = random.randint(0, employees-1)
    ship = random.randint(0, shipping-1)
    product = random.randint(0, products-1)
    quantity = random.randint(1,5)
    unitprice = random.randint(2345,14567)
    discount = 0
    payment = random.randint(0, payments-1)
    time = date.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(f"INSERT INTO Orders (OrderId, ShippingMethodId, EmployeeId, CustomerId, OrderDate) VALUES ({orders}, {ship}, {employee}, {customer}, '{time}')")
    conn.commit()
    cur.execute(f"INSERT INTO Order_Details (OrderId, ProductId, OrderDetailId, Quantity, UnitPrice, Discount) VALUES ({orders}, {product}, {orders}, {quantity}, {unitprice}, {discount})")
    conn.commit()
    cur.execute(f"INSERT INTO Payment (PaymentMethodId, OrderId, PaymentId, PaymentAmount, PaymentDate) VALUES ({payment}, {orders}, {orders}, {quantity*unitprice}, '{time}')")
    conn.commit()

    date = datetime.now() + timedelta(days=1)

cur.close() # Cerrar Conexion
conn.close()
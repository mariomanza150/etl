import pyodbc
import mysql.connector
import pymongo
from config import *

class Etl():
    def __init__(self):
        # Definir Conecciones a Bases de datos
        self.ms = pyodbc.connect(winsql['string']+"DATABASE=BarnesNoble;")
        self.sql = conn = mysql.connector.connect(
                host=sql['host'],
                user=sql['user'],
                password=sql['password'],
                database='eluktronics'
            )
        self.mongo = pymongo.MongoClient(mongodb['conn'])["myetl"]
    
    # cargar datos a tabla Dim_Products, con identificador b y e para Books y Electronics respectivamente y evitar colisiones
    def import_products(self):
        book_cur = self.ms.cursor()
        electr_cur = self.sql.cursor()
        prod_cur = self.mongo["Dim_Products"]

        book_cur.execute("SELECT Book.BookId, Book.Title, Category.CategoryId, Category.CategoryDescription FROM Book INNER JOIN Category ON Book.CategoryId=Category.CategoryId;")
        electr_cur.execute("SELECT Products.ProductId, Products.ProductName, Brands.BrandId, Brands.BrandDescription FROM Products INNER JOIN Brands ON  Products.BrandId=Brands.BrandId;")

        for el in book_cur:
            try:
                prod_cur.insert_one({"_id": f"{el[0]}b", "ProductName": el[1], "CategoryName": el[2], "CategoryName": el[3]})
            except Exception as ex:
                pass

        for el in electr_cur:
            try:
                prod_cur.insert_one({"_id": f"{el[0]}e", "ProductName": el[1], "CategoryName": el[2], "CategoryName": el[3]})
            except Exception as ex:
                pass
    
    # cargar datos a tabla Dim_Locations, con identificador b y e para Books y Electronics respectivamente y evitar colisiones
    def import_locations(self):
        book_cur = self.ms.cursor()
        electr_cur = self.sql.cursor()
        prod_cur = self.mongo["Dim_Locations"]

        book_cur.execute("SELECT ZipCode, City, State FROM Customer;")
        electr_cur.execute("SELECT PostalCode, City, State FROM Customers;")

        for el in book_cur:
            try:
                prod_cur.insert_one({"_id": el[0], "TerritoryId": el[1], "TerritoryName": el[1], "RegionId": el[2], "RegionName": el[2]})
            except Exception as ex:
                pass

        for el in electr_cur:
            try:
                prod_cur.insert_one({"_id": el[0], "TerritoryId": el[1], "TerritoryName": el[1], "RegionId": el[2], "RegionName": el[2]})
            except Exception as ex:
                pass
    
    def import_customers(self):
        book_cur = self.ms.cursor()
        electr_cur = self.sql.cursor()
        prod_cur = self.mongo["Dim_Customer"]

        book_cur.execute("SELECT CustomerId, FirstName, LastName FROM Customer;")
        electr_cur.execute("SELECT CustomerId, CompanyName, ContactName FROM Customers;")

        for el in book_cur:
            try:
                prod_cur.insert_one({"_id": f"{el[0]}b", "CustomerName": f"{el[1]} {el[2]}"})
            except Exception as ex:
                pass

        for el in electr_cur:
            try:
                prod_cur.insert_one({"_id": f"{el[0]}e", "CustomerName": f"{el[1]} {el[2]}"})
            except Exception as ex:
                pass

    # Utilidad para cargar Dim_Time cuando la fecha no existe
    def time_insert(self, date):
        time_cur = self.mongo["Dim_Time"]
        date = date.strftime("%Y-%m-%d")
        raw = date.split("-")
        month = int(raw[1])
        year = raw[0]
        if month <= 3:
            quarter = 1
        if month <= 6 and month > 3:
            quarter = 2
        if month <= 9 and month > 6:
            quarter = 3
        if month > 9:
            quarter = 4
        try:
            time_cur.insert_one({"_id": date, "Month": month, "Quarter": quarter, "Year": year})
            return date
        except Exception as ex:
            pass

    # Cargar Ventas de Books y Electronics con id + b y e respectivamente
    def import_sales(self):
        book_cur = self.ms.cursor()
        electr_cur = self.sql.cursor()
        sales_cur = self.mongo["Fact_Sales"]

        book_cur.execute("SELECT Book_Order.OrderId, Ordering.BookId, Ordering.BookId, Customer.ZipCode, Book_Order.CustomerId, Book_Order.OrderDate, Ordering.Price FROM Book_Order INNER JOIN Ordering ON Book_Order.OrderId=Ordering.OrderId INNER JOIN Customer ON Book_Order.CustomerId=Customer.CustomerId;")
        electr_cur.execute("SELECT Orders.OrderId, Order_Details.OrderDetailId, Order_Details.ProductId, Customers.PostalCode, Orders.CustomerId, Orders.OrderDate, Order_Details.Quantity, Order_Details.UnitPrice, Order_Details.Discount FROM Orders INNER JOIN Order_Details ON Orders.OrderId=Order_Details.OrderId INNER JOIN Customers ON Orders.CustomerId=Customers.CustomerId;")

        for el in book_cur:
            date = self.time_insert(el[5])
            try:
                sales_cur.insert_one({"_id": f"{el[0]}b", "OrderDetailId": f"{el[1]}b", "ProductId": f"{el[1]}b", "PostalCode": el[3], "CustomerId": el[4], "Date": date, "Quantity": 1, "UnitPrice": el[6], "Discount": 0})
            except Exception as ex:
                pass

        for el in electr_cur:
            date = self.time_insert(el[5])
            try:
                sales_cur.insert_one({"_id": f"{el[0]}b", "OrderDetailId": f"{el[1]}e", "ProductId": f"{el[2]}e", "PostalCode": el[3], "CustomerId": el[4], "Date": date, "Quantity": el[6], "UnitPrice": el[7], "Discount": el[8]})
            except Exception as ex:
                pass
    
    def import_data(self):
        self.import_products()
        self.import_locations()
        self.import_sales()

if __name__ == "__main__":
    etl = Etl()
    etl.import_data()
import pyodbc
import mysql.connector
import pymongo
from config import *

class Etl():
    def __init__(self):
        self.ms = pyodbc.connect(winsql['string']+"DATABASE=BarnesNoble;")
        self.sql = conn = mysql.connector.connect(
                host=sql['host'],
                user=sql['user'],
                password=sql['password'],
                database='eluktronics'
            )
        self.mongo = pymongo.MongoClient("mongodb://localhost:27017/")["myetl"]
    
    def load_existing(self):
        products = self.mongo["dim_products"]
        num_products = products.find().count()
        locations = self.mongo["dim_location"]
        num_locations = locations.find().count()
        customers = self.mongo["dim_customer"]
        num_customers = customers.find().count()
    
    def import_data(self):
        book_cur = self.ms.cursor()
        electr_cur = self.sql.cursor()
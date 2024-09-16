# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import snowflake.connector
import pandas as pd

class BookCrawlerPipeline:
    def process_item(self, item, spider):
        return item

class SaveToSnowflakePipeline: 

    def  __init__(self):
        self.conn = snowflake.connector.connect(
            user='<your_username>',
            password='<your_password>',
            account='<your_account>.snowflakecomputing.com',
            warehouse='<your_warehouse>',
            database='<your_database>',
            schema='<your_schema>'
        )

        # Create a cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Create a new database (optional, you can use an existing one)
        # self.cur.execute("CREATE OR REPLACE DATABASE books_db")

        # Use the new database
        self.cur.execute("USE DATABASE books_db")

        # Create a new schema (optional)
        # self.cur.execute("CREATE OR REPLACE SCHEMA public")

        # Use the schema
        self.cur.execute("USE SCHEMA public")

        # Create master table shop table
        self.cur.execute('''
        CREATE OR REPLACE TABLE MASTER_TABLE (
            Bokus STRING NOT NULL,
            Adlibris STRING NOT NULL,
            Akademibokhandeln STRING NOT NULL
        )
        ''')

        # Create Bokus shop table
        self.cur.execute('''
        CREATE OR REPLACE TABLE BOKUS (
            title STRING NOT NULL,
            author STRING NOT NULL,
            price INTEGER,
            discount INTEGER,
            PRIMARY KEY (title)
        )
        ''')

        # Create Adlibris shop table
        self.cur.execute('''
        CREATE OR REPLACE TABLE ADLIBRIS (
            title STRING NOT NULL,
            author STRING NOT NULL,
            price INTEGER,
            discount INTEGER,
            category STRING,
            PRIMARY KEY (title)
        )
        ''')

        # Create Akademibokhandeln shop table
        self.cur.execute('''
        CREATE OR REPLACE TABLE AKADEMIBOKHANDELN (
            title STRING NOT NULL,
            author STRING NOT NULL,
            price INTEGER,
            discount INTEGER,
            category STRING,
            PRIMARY KEY (title)
        )
        ''')

    # Function to insert data into BOKUS table from a CSV
    def bokus_data_from_csv(self, csv_file):
        bokus_df = pd.read_csv(csv_file)
    
        for index, row in bokus_df.iterrows():
            self.cur.execute('''
                INSERT INTO BOKUS (title, author, price, discount)
                VALUES ( ?, ?, ?, ?)
            ''', (row['title'], row['author'], row['price'], row['discount']))

        # Commit the transaction
        self.conn.commit()

    # Close the connection
    def close_spider(self, spider):
        # Close cursor and connection
        self.cur.close()
        self.conn.close()

print("Database and tables created successfully in Snowflake!")
 

import pandas as pd
import datetime
import os
from time import time
import pymongo
import json


class Ingest:
    def __init__(self, **kwargs):
        self.utc_time = datetime.datetime.utcnow()
        self.today_date = self.utc_time.strftime("%Y%m%d")
        self.root_path = os.getcwd() + '/csv/'
        self.file_name = (
            self.today_date + 'bbc.csv'
        )
        self.filename = os.path.join(self.root_path, self.file_name)
        self.url = 'mongodb://localhost'
        self.port = 27017
        self.client = pymongo.MongoClient(self.url, self.port)
        self.DB = self.client['bbc']
        self.collection = self.DB['bbc_news']


    def timer_func(func):
        """This function shows the execution time of
        the function object passed"""
        def wrap_func(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
            return result
        return wrap_func

    def load_data(self):
        """load csv data from the directory"""
        try:
            df = pd.read_csv(self.filename)
            #print(df)
            return df
        except Exception as e:
            print(f"Error occurred while loading data\n{str(e)}")

    @timer_func
    def run(self):
        print(self.filename)
        data = self.load_data()
        data_json = json.loads(data.to_json(orient='records'))
        collecton = self.collection
        collecton.insert_many(data_json)
        print(collecton.estimated_document_count())
        collecton.create_index([("text", pymongo.TEXT)], name='text_index', default_language='english')

if __name__ == "__main__":
    Ingest().run()

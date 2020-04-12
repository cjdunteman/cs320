import zipfile
import io
from zipfile import ZipFile
import sqlite3
import os
import pandas as pd
import numpy as np

def open(name):
    c = Connection(name)
    return c

class Connection:
    def __init__(self, name):
        self.db = sqlite3.connect(name+".db")
        self.zf = zipfile.ZipFile(name+".zip")
#     def __init__(self, name):
#         # you need to set name as property because this value is used in multiple places
#         self._name = name
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
#         self.zf.close()

#     @property
#     def db(self):
#         return sqlite3.connect(self._name+".db")

#     @property
#     def zip(self):
#         return zipfile.ZipFile(self._name+".zip")

    def list_images(self):
        assert os.path.exists("images.db")
        c = sqlite3.connect("images.db")
        images_df = pd.read_sql("SELECT image FROM images", c)
        image_list = sorted(images_df['image'].tolist())
        return image_list
    
    def image_year(self, name):
        assert os.path.exists("images.db")
        c = sqlite3.connect("images.db")
        df = pd.read_sql("SELECT * FROM images", c)
        idx = df.loc[df['image'] == name].index.values.tolist()[0]
        year = int(df.iloc[idx]["year"])
        return year
    
    def image_name(self, name):
        assert os.path.exists("images.db")
        c = sqlite3.connect("images.db")
        images_df = pd.read_sql("SELECT * FROM images", c)
        places_df = pd.read_sql("SELECT * FROM places", c)
        row = images_df[images_df["image"] == name]
        place_id = row["place_id"].values.tolist()[0]
        name = places_df[places_df["place_id"] == place_id]["name"].values.tolist()[0]
        return name
    
    def image_load(self, name):
        with ZipFile("images.zip") as zf:
            with zf.open(name) as f:
                buf = io.BytesIO(f.read())
                place = np.load(buf)
        return place
    
    def lat_regression(self, use_code, ax):
        # GET DF of samp only places
        assert os.path.exists("images.db")
        c = sqlite3.connect("images.db")
        places_df = pd.read_sql("SELECT * FROM places", c)
        places_df = places_df["name"][0:100]

        # GET PERCENT
        with ZipFile("images.zip") as zf:
            count = 0
            total = 0
            for file in zf.namelist():
                with zf.open(file) as f:
                    buf = io.BytesIO(f.read())
                    place = np.load(buf)
                    count += np.count_nonzero(place == use_code)
                    total += np.size(place)
        percent = count / total
        return percent

    def close(self):
        self.db.close
        self.zf.close

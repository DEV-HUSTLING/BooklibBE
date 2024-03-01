from pymongo import MongoClient
import gridfs

def mongo_conn():
    try:
        conn = MongoClient(host = '127.0.0.1', port  = 27017)
        print("MongoDB connected", conn)
        return conn.grid_file
    except Exception as e:
        print("Error in mongo connection:", e)

db = mongo_conn()
name = "deeplearningwithpython.pdf"
file_location = "/Users/anushkareddy/Desktop/Books/"+name
file_data = open(file_location,"+rb")
data = file_data.read()
fs = gridfs.GridFS(db)
fs.put(data, filename = name)
print("upload complete")



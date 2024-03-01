from flask import Flask, request, jsonify,send_file
from gridfs import GridFS
import os
from bson import ObjectId
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
compress = Compress(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Books"
mongo = PyMongo(app)
db = mongo.db
fs = GridFS(db, collection='books')  # Specify the collection name as 'books' within the 'Books' database
CORS(app)  # Add this line to allow all origins

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        pdf_file = request.files['file']
        filename = pdf_file.filename
        file_data = pdf_file.read()

        # Insert the PDF file into GridFS
        fs.put(file_data, filename=filename)

        return jsonify({'message': 'PDF file uploaded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/files', methods=['GET'])
def list_files():
    try:
        files_info = []
        # Retrieve all file metadata from the GridFS collection
        for file_info in fs.find():
            files_info.append({
                'file_id': str(file_info._id),
                'filename': file_info.filename,
                'mimetype': 'application/pdf'
            })
        return jsonify({'files': files_info}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/files/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        # Retrieve the file from GridFS by its ObjectId
        file_object = fs.get(ObjectId(file_id))
        
        # Return the file as an attachment
        return send_file(file_object, mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "<p>Server is running</p>"

if __name__ == '__main__':
    app.run(debug=True)

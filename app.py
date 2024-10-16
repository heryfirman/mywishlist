from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

client = MongoClient(os.environ['MONGO_URI'])
db = getattr(client, os.environ['DB_NAME'])

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})


@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num = int(request.form["num"])
    db.bucket.delete_one({'num': num})
    return jsonify({'msg':'Delete done!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
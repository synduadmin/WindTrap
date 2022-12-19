# app.py
import os
import json
import logging
from flask import Flask, request
import uuid
import pymongo
from datetime import datetime
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/log', methods=['POST'])
def log():
    content = {}
    content['time'] = get_timestamp()
    content['status'] = 0
    content['id'] = str(uuid.uuid4())
    content['accept_charsets'] = request.accept_charsets
    content['accept_encodings'] = request.accept_encodings
    content['accept_languages'] = request.accept_languages
    content['accept_mimetypes'] = request.accept_mimetypes
    content['access_route'] = request.access_route
    content['accept_mimetypes'] = request.accept_mimetypes
    content['args'] = request.args
    content['authorization'] = request.authorization
    content['base_url'] = request.base_url
    content['blueprint'] = request.blueprint
    content['cache_control'] = request.cache_control
    content['content_length'] = request.content_length
    content['content_type'] = request.content_type
    content['cookies'] = request.cookies
    content['date'] = request.date
    
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        content['ip'] = request.environ['REMOTE_ADDR']
    else:
        content['ip'] = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    content['endpoint'] = request.endpoint
    content['files'] = request.files
    content['form'] = request.form
    content['full_path'] = request.full_path
    content['host'] = request.host
    content['host_url'] = request.host_url
    content['is_json'] = request.is_json
    content['is_secure'] = request.is_secure
    content['json'] = request.get_json()


    # write to logtrail
    app.logger.info(f"{content}")
    
    # log to databases

    # mongo db
    try:
        log_to_mongo(content)
    except Exception as e:
        app.logger.error(f"Failed to write to mongo: {e}")
    
    # postgres
    try: 
        log_to_postgres(content)
    except Exception as e:
        app.logger.error(f"Failed to write to pg: {e}")

    return '1'

def get_timestamp():
    format_str = "%A, %d %b %Y %H:%M:%S %p"
    result = datetime.now().strftime(format_str)
    return result

def log_to_mongo(content):
    load_dotenv()

    m_host = os.getenv("mongo_host")
    m_port = int(os.getenv("mongo_port"))
    m_user = os.getenv("mongo_user")
    m_pass = os.getenv("mongo_pass")
    m_db = os.getenv("mongo_db")
    m_collection = os.getenv("mongo_collection")

    client = pymongo.MongoClient(m_host, m_port, username=m_user, password=m_pass)
    mydb = client[m_db]
    mycol = mydb[m_collection]
    x = mycol.insert_one(content)
    return

def log_to_postgres(content):
    load_dotenv()
    
    pg_connection_dict = {
    'dbname': os.getenv("pg_db"),
    'user': os.getenv("pg_user"),
    'password': os.getenv("pg_pass"),
    'port': os.getenv("pg_port"),
    'host':os.getenv("pg_host")
    }

    conn = psycopg2.connect(**pg_connection_dict)
    cur = conn.cursor()
    cur.execute("INSERT INTO log (event_timestamp,  data, status) VALUES (now(), %s, 0)", [Json(content)])
    conn.commit()
    cur.close()
    conn.close()
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

import os
from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_pymongo import PyMongo
import uuid

app = Flask(__name__)
uri = 'mongodb://{}:{}@{}/{}'.format(os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'],os.environ['DB_NAME'])
mongo =  PyMongo(app, uri, tls=True, tlsCAFile='/etc/ca-clients/mongodb-ca-cert',tlsCertificateKeyFile='/etc/ca-clients/client-pem')

@app.route('/')
def tasks_list():
    tasks = mongo.db.tasks.find()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task =  {'content': content, 'done': False, 'id': str(uuid.uuid4())}
    mongo.db.tasks.insert_one(task)
    return redirect('/')


@app.route('/delete/<string:task_id>')
def delete_task(task_id):
    print('delete')
    mongo.db.tasks.delete_one({'id': task_id})
    return redirect('/')


@app.route('/done/<string:task_id>')
def resolve_task(task_id):
    task = mongo.db.tasks.find_one({'id': task_id})
    print(task)
    if not task:
        return redirect('/')
    if task['done']:
        done = False
    else:
        done = True

    mongo.db.tasks.update_one({'_id': task['_id']}, { '$set': { 'done': done } }  ,upsert=True)
    return redirect('/')


if __name__ == '__main__':
    debug = os.getenv('DEBUG') == "True"
    app.run(host='0.0.0.0', port='8080', debug=debug)
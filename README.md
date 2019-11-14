# Tasks_Python
Install virtualenv
pip install virtualenv

Make a directory
mkdir itflex

Open the directory created

Make a directory to stored the code in the lastest created directory
mkdir desafio_estagio_backend

Create the virtualenv in the directory
virtualenv .venv

Active the virtualenv
source .venv/bin/activate

#show
@api.route('/api/tasks', methods=['GET'])
def home():
    return jsonify(tasks), 200

#update
@api.route('/api/tasks', methods=['PUT'])
def change_done(id):
    for task in tasks:
        if task['id'] == id:
                task['done'] = request.get_json().get('done')
                return jsonify(tasks), 200
    return jsonify({'error': 'task not found'}), 404

#insert
@api.route('/api/tasks', methods=['POST'])
def save_task():
    data = request.get_json()
    tasks.append(data)
    return jsonify(tasks), 201

#delete
@api.route('/api/tasks', methods=['DELETE'])
def delete_task():
    index = id - 1
    del tasks[index]
    return jsonify({'message': 'Task removed'}), 204


from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

#instancia de flask
app = Flask(__name__)
#searla la base
app.config['MONGO_URI']='mongodb://localhost:27017/pythonreactdb'
#acceder a mongo
mongo = PyMongo(app)
CORS(app)
#acceder a modelo 
db = mongo.db.users
#ruta crear usuarios
@app.route('/users', methods=['POST'])
def createUser():
    #print(request.get_json(force=True))
    #insertar dato en mongodb
    id =  db.insert({
        "name": request.get_json(force=True)["name"],
        "email": request.get_json(force=True)["email"],
        "password": request.get_json(force=True)["password"]
    })
    return jsonify(str(ObjectId(id)))
   

#ruta recibir usuarios
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    #llenar arreglo con los datos de mongo
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'email':doc['email'],
            'password':doc['password']

        })
    
    return jsonify(users)

#ruta recibir usuario
@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    #buscar un dato en mongo
    user = db.find_one({'_id':ObjectId(id)})
    
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
        'name':user['name'],
        'email':user['email'],
        'password':user['password']
    })

#ruta Eliminar usuario
@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    #eliminar de mongo
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({'msg':'user delete'})

#ruta actualizar usuario
@app.route('/users/<id>',methods=['PUT'])
def updateUser(id):
    db.update_one({'_id':ObjectId(id)},{'$set':{
        'name': request.get_json(force=True)['name'],
        'email':request.get_json(force=True)['email'],
        'password':request.get_json(force=True)['password']
    }})
    return jsonify({'msg':'User updated'})

#iniciar
if __name__ == "__main__":
    app.run(debug=True)

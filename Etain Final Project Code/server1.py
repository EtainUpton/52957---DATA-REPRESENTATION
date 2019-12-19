from flask import Flask, jsonify, request, abort, render_template
from dogDAO import dogDAO
import mysql.connector

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
   return render_template('bookviewer.html')

#curl "http://127.0.0.1:5000/dogs"
@app.route('/dogs')
def getAll():
    results = dogDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/dogs/2"
@app.route('/dogs/<int:id>')
def findById(id):
    foundDog = dogDAO.findByID(id)

    return jsonify(foundDog)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Name\":\"Fluffy\",\"Owner\":\"John Doe\",\"Value\":10000}" http://127.0.0.1:5000/dogs
@app.route('/dogs', methods=['POST'])
def create():
    if not request.json:
        abort(400)
    # other checking 
    dog = {
        "Name": request.json['Name'],
        "Owner": request.json['Owner'],
        "Value": request.json['Value'],
    }
    values =(dog['Name'],dog['Owner'],dog['Value'])
    newId = dogDAO.create(values)
    dog['id'] = newId
    return jsonify(dog)     

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Name\":\"Fluffy\",\"Owner\":\"John Doe\",\"Value\":10000}" http://127.0.0.1:5000/dogs/1
@app.route('/dogs/<int:id>', methods=['PUT'])
def update(id):
    foundDog = dogDAO.findByID(id)
    if not foundDog:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Value' in reqJson and type(reqJson['Value']) is not int:
        abort(400)

    if 'Name' in reqJson:
        foundDog['Name'] = reqJson['Name']
    if 'Owner' in reqJson:
        foundDog['Owner'] = reqJson['Owner']
    if 'Value' in reqJson:
        foundDog['Value'] = reqJson['Value']
    values = (foundDog['Name'],foundDog['Owner'],foundDog['Value'],foundDog['id'])
    dogDAO.update(values)
    return jsonify(foundDog)


@app.route('/dogs/<int:id>', methods=['DELETE'])
def delete(id):
    dogDAO.delete(id)
    return jsonify({"done":True})

if __name__ == '__main__' :
    dogDAO.createTable()
    dogDAO.populateTable()
    app.run(debug= True)
        
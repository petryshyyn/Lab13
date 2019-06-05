from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dbsqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
database = SQLAlchemy(app)
# Init ma
marshmallow = Marshmallow(app)


# Event Class/Model
class StorageAccessories(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    material_of_bag = database.Column(database.String(100))
    price_by_toolbar = database.Column(database.Integer)
    type_of_folder = database.Column(database.String(100))

    def __init__(self, material_of_bag, price_by_toolbar,
                 type_of_folder):
        self.material_of_bag = material_of_bag
        self.price_by_toolbar = price_by_toolbar
        self.type_of_folder = type_of_folder


# Event Schema
class StorageAccessoriesSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'material_of_bag', 'price_by_toolbar', 'type_of_folder')


# Init schema
accessory_schema = StorageAccessoriesSchema(strict=True)
accessories_schema = StorageAccessoriesSchema(many=True, strict=True)


# Create a event
@app.route('/accessories', methods=['POST'])
def add_event():
    material_of_bag = request.json['material_of_bag']
    price_by_toolbar = request.json['price_by_toolbar']
    type_of_folder = request.json['type_of_folder']

    new_accessory = StorageAccessories(material_of_bag, price_by_toolbar, type_of_folder)

    database.session.add(new_accessory)
    database.session.commit()

    return accessory_schema.jsonify(new_accessory)


# Get all events
@app.route('/accessories', methods=['GET'])
def get_all_events():
    all_accessories = StorageAccessories.query.all()
    result = accessories_schema.dump(all_accessories)
    return jsonify(result.data)

# Get one event
@app.route('/accessories/<id>', methods=['GET'])
def get_event(id):
    accessories = StorageAccessories.query.get(id)
    return accessory_schema.jsonify(accessories)

# Uodate a event
@app.route('/accessories/<id>', methods=['PUT'])
def update_event(id):
    accessories = StorageAccessories.query.get(id)

    material_of_bag = request.json["material_of_bag"]
    price_by_toolbar = request.json["price_by_toolbar"]
    type_of_folder = request.json["type_of_folder"]

    accessories.material_of_bag = material_of_bag
    accessories.price_by_toolbar = price_by_toolbar
    accessories.type_of_folder = type_of_folder

    database.session.commit()

    return accessory_schema.jsonify(accessories)

# Delete event
@app.route('/accessories/<id>', methods=['DELETE'])
def delete_event(id):
    accessories = StorageAccessories.query.get(id)
    database.session.delete(accessories)
    database.session.commit()
    return accessory_schema.jsonify(accessories)


database.create_all()
# Run Server
if __name__ == '__main__':
    app.run(debug=True)

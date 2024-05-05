# app.py

from models import User, Product, Category
from flask import Flask, request, jsonify
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(email=data['email'], password=data['password'], name=data['name'], pincode=data['pincode'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    with app.app_context():
        user = User.query.filter_by(email=data['email'], password=data['password']).first()
        if user:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

# Define route for creating a product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')

    if not all([name, description, price, category_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_product = Product(name=name, description=description, price=price, category_id=category_id)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully', 'product_id': new_product.id}), 201

# Define route for creating a category
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Missing required fields'}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully', 'category_id': new_category.id}), 201

@app.route('/getproducts', methods=['GET'])
def get_all_products():
    with app.app_context():
        products = Product.query.all()
        output = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'category_id': product.category_id
            }
            output.append(product_data)
    return jsonify({'products': output})

# Define other CRUD endpoints for products and categories...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)

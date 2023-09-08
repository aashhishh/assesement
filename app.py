from flask import jsonify, request
from models import app,User,Product
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from models import db
import uuid
import re

otp_expiration= 10

session =  db.session

# Helper function to generate a unique product link
def generate_unique_product_link(user_id, product_id):
    unique_identifier = uuid.uuid4().hex
    product_link = f"/purchase/{user_id}/{product_id}/{unique_identifier}"
    return product_link

# API endpoint for advisor registration
@app.route('/advisor/signup', methods=['POST'])
def advisor_signup():
    if request.method == 'POST':
        try:
            data = request.get_json()
            mobile = str(data.get('mobile'))
            otp = str(data.get('otp'))
            if not re.match(r'^\d{10}$', mobile):
                return jsonify({'message': 'Invalid Phone number!'}), 400
            
            if not re.match(r'^\d{6}$', otp):
                return jsonify({'message': 'Invalid Otp format!'}), 400
            
            if otp !='123456':
                return jsonify({'error':'Invalid OTP!'}), 500

            existing_user = User.query.filter_by(mobile=mobile).first()
            if existing_user:
                advisor = existing_user
                advisor.mobile = mobile
                advisor.role = 'Advisor'
                db.session.add(advisor)
                db.session.commit()

                token = create_access_token({'sub': advisor.user_id, 'role': advisor.role})

                return jsonify({'message': 'Advisor already registered', 'user_id': advisor.user_id, 'access_token': token})

            advisor = User(mobile=mobile, role='Advisor')
            db.session.add(advisor)
            db.session.commit()

            token = create_access_token({'sub': advisor.user_id, 'role': advisor.role})

            return jsonify({'message': 'Advisor registered successfully', 'user_id': advisor.user_id, 'access_token': token})
        
        except KeyError as e:
            missing_field = str(e)
            return jsonify({'error': f"The field '{missing_field}' is required."}), 400
        except Exception as e:
            return jsonify({"error":str(e)})
        

# API endpoint for adding a client
@app.route('/advisor/add-client', methods=['POST'])
@jwt_required()
def add_client():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        advisor = User.query.get(user_id['sub'])
        print(advisor)
        # Check if the advisor exists and has the role 'Advisor'
        if advisor is None or advisor.role != 'Advisor':
            return jsonify({'message': 'Advisor not found'}), 404


        client_name = data.get('name')
        client_mobile = data.get('mobile')
        if not re.match(r'^\d{10}$', client_mobile):
                    return jsonify({'message': 'Invalid Client Phone number!'}), 400
        
        client = User(name=client_name, mobile=client_mobile, role='User', created_by= advisor.mobile)
        db.session.add(client)
        db.session.commit()
        
        return jsonify({'message': 'Client added successfully', 'name': client.name,'mobile':client.mobile})
    except IntegrityError as e:
        # Handle the duplicate mobile number error here
        db.session.rollback() 
        return jsonify({'message': 'Mobile number already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint for an advisor to view the list of all clients
@app.route('/advisor/clients', methods=['GET'])
@jwt_required()
def get_clients():
    try:
        advisor_id = get_jwt_identity()
        advisor = User.query.get(advisor_id['sub'])
        if advisor is None or advisor.role != 'Advisor':
            return jsonify({'message': 'Advisor not found'}), 404

        clients = User.query.filter_by(role='User').all()
        client_list = [{'user_id': client.user_id, 'name': client.name, 'mobile': client.mobile} for client in clients]
        
        return jsonify(client_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

# API endpoint for user signup
@app.route('/user/signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_mobile = str(data.get('mobile'))
            user_name = data.get('name')
            otp = str(data.get('otp'))
            if not re.match(r'^\d{10}$', user_mobile):
                return jsonify({'message': 'Invalid Phone number!'}), 400

            if not re.match(r'^\d{6}$', otp):
                return jsonify({'message': 'Invalid Otp format!'}), 400

            if otp !='123456':
                return jsonify({'error':'Invalid OTP!'}), 500

            existing_user = User.query.filter_by(mobile=user_mobile).first()
            if existing_user:
                user = existing_user
                user.mobile = user_mobile
                user.role = 'User'
                db.session.add(user)
                db.session.commit()
                return jsonify({'message': 'User already registered', 'user_id': user.user_id})

            user = User(name=user_name, mobile=user_mobile, role='User')
            db.session.add(user)
            db.session.commit()
        
            return jsonify({'message': 'User registered successfully', 'user_id': user.user_id})
        except KeyError as e:
            missing_field = str(e)
            return jsonify({'error': f"The field '{missing_field}' is required."}), 400
        except Exception as e:
                return jsonify({"error":str(e)})

# API endpoint for admin to add products
@app.route('/admin/add-product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        product_description = data.get('product_description')
        category = data.get('category')
        
        existing_category = Product.query.filter_by(category=category, product_name=product_name).first()
        if existing_category:return jsonify({'message': 'Product with same name and category already existed!'})

        new_product = Product(product_name=product_name, desc=product_description, category=category)
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({'message': 'Product added successfully', 'product_id': new_product.product_id, 'name': new_product.name, 'category': new_product.category})

    except KeyError as e:
            missing_field = str(e)
            return jsonify({'error': f"The field '{missing_field}' is required."}), 400
    except Exception as e:
            return jsonify({"error":str(e)})
    
@app.route('/advisor/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        advisor_id = get_jwt_identity()
        advisor = User.query.get(advisor_id['sub'])
        if advisor is None or advisor.role != 'Advisor':
            return jsonify({'message': 'Advisor not found'}), 404

        products = Product.query.all()
        product_list = [{'product_name': product.product_name, 'product_description': product.desc, 'category': product.category} for product in products]
        
        return jsonify(product_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

# API endpoint for an advisor to purchase products for users
@app.route('/advisor/purchase-product', methods=['POST'])
@jwt_required()
def purchase_product():
    try:
        data = request.get_json()
        advisor_id = get_jwt_identity()
        advisor = User.query.get(advisor_id['sub'])
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        
        if advisor is None or advisor.role != 'Advisor':
            return jsonify({'message': 'Advisor not found'}), 404

        # Generate a unique product link for the user and product
        unique_product_link = generate_unique_product_link(user_id, product_id)
        
        return jsonify({'product_link': unique_product_link})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True)



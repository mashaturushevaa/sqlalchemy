from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Налаштування для SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Налаштування для JWT
app.config["JWT_SECRET_KEY"] = "123456"

# Ініціалізація SQLAlchemy та JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Модель користувача
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Створення бази даних
with app.app_context():
    db.create_all()

# Головна сторінка
@app.route('/')
def index():
    return jsonify({'message': 'API is running. Try /register or /login.'})

# Реєстрація користувача
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if UserModel.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = UserModel(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Вхід користувача
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

# Захищений ендпоінт
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Отримуємо поточного користувача
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)




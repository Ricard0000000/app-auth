from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# MODELO USER
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# -------------------------
# ROTA HOME
# -------------------------
@app.route('/')
def home():
    return jsonify({"message": "API funcionando"})


# -------------------------
# CADASTRO
# -------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    # verifica email duplicado
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email já existe"}), 400

    # criptografa senha
    hashed_password = generate_password_hash(data['password'])

    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso"}), 201


# -------------------------
# LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login realizado com sucesso"}), 200

    return jsonify({"error": "Credenciais inválidas"}), 401


# -------------------------
# EXECUÇÃO
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
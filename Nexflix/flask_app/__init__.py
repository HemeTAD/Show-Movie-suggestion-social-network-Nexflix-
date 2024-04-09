from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "760662a40c62991bb02fd8d79f24777ed984201b236371f5d1efd844c0f5da10"

bcrypt = Bcrypt(app)  # we are creating an object called bcrypt,

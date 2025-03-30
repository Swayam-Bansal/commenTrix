# backend/main.py
from flask import Flask
from flask_cors import CORS
from routes.comments_routes import comments_bp
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}) # Allow only from your React app's origin

# Register Blueprints
app.register_blueprint(comments_bp)
app.register_blueprint(analysis_bp)

if __name__ == '__main__':
    app.run(debug=True)
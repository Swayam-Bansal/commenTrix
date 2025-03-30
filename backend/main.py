# backend/main.py
from flask import Flask
from routes.comments_routes import comments_bp
from routes.analysis_routes import analysis_bp
# Import other Blueprints if you have them

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(comments_bp)
app.register_blueprint(analysis_bp)
# Register other Blueprints

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify
from flask_cors import CORS
import logging, os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # # Load configuration from environment variables or a config file
    # app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mydatabase')
    # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Application initialized with configuration: %s", app.config)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "healthy"}), 200
    
    @app.get("/api/products")
    def products():
        demo = [
            {"id": "p1", "name": "Laptop Sleeve", "price": 29.99, "images": []},
            {"id": "p2", "name": "USB-C Hub", "price": 49.00, "images": []},
        ]
        return jsonify({"items": demo, "total": len(demo)})

    # @app.route('/health', methods=['GET'])
    # def health_check():
    #     return jsonify({"status": "healthy"}), 200

    return app
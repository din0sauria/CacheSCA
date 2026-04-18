from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.performance import performance_bp
from routes.evaluation import evaluation_bp
from routes.config import config_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(performance_bp, url_prefix='/api/performance')
app.register_blueprint(evaluation_bp, url_prefix='/api/evaluation')
app.register_blueprint(config_bp, url_prefix='/api/config')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'CacheSCA-Tool API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

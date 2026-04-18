import os
import sys
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.config_service import ConfigService

config_bp = Blueprint('config', __name__)
config_service = ConfigService()

@config_bp.route('/targets', methods=['GET'])
def get_targets():
    cipher = request.args.get('cipher', 'AES')
    targets = config_service.get_targets(cipher)
    return jsonify({'targets': targets})

@config_bp.route('/set-config', methods=['POST'])
def set_config():
    data = request.json
    result = config_service.set_config(data)
    return jsonify(result)

@config_bp.route('/get-config', methods=['GET'])
def get_config():
    config = config_service.get_config()
    return jsonify(config)

@config_bp.route('/upload-library', methods=['POST'])
def upload_library():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file and file.filename.endswith('.so'):
        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)
        result = config_service.upload_custom_library(temp_path)
        os.remove(temp_path)
        return jsonify(result)
    
    return jsonify({'success': False, 'message': 'Invalid file type. Only .so files are allowed'})

import os
import sys
from flask import Blueprint, request, jsonify

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.performance_service import PerformanceService

performance_bp = Blueprint('performance', __name__)
performance_service = PerformanceService()

@performance_bp.route('/test', methods=['POST'])
def run_performance_test():
    data = request.json
    result = performance_service.run_test(data)
    return jsonify(result)

@performance_bp.route('/compare', methods=['POST'])
def compare_results():
    files = request.json.get('files', [])
    result = performance_service.compare_results(files)
    return jsonify(result)

@performance_bp.route('/save', methods=['POST'])
def save_result():
    data = request.json
    result = performance_service.save_result(data)
    return jsonify(result)

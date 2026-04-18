import os
import sys
from flask import Blueprint, request, jsonify

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.evaluation_service import EvaluationService

evaluation_bp = Blueprint('evaluation', __name__)
evaluation_service = EvaluationService()

@evaluation_bp.route('/test', methods=['POST'])
def run_evaluation():
    data = request.json
    result = evaluation_service.run_evaluation(data)
    return jsonify(result)

@evaluation_bp.route('/analyze', methods=['POST'])
def analyze_result():
    filepath = request.json.get('filepath')
    result = evaluation_service.analyze_result(filepath)
    return jsonify(result)

@evaluation_bp.route('/heatmap', methods=['POST'])
def get_heatmap():
    data = request.json
    result = evaluation_service.get_heatmap(data)
    return jsonify(result)

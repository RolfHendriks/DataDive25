"""
Flask server for Global Digital Skills Gap Navigator
"""

from flask import Flask, render_template, send_from_directory, jsonify
from pathlib import Path
import json

app = Flask(__name__,
           template_folder='templates',
           static_folder='static')

# Base paths
BASE_DIR = Path(__file__).parent
VIZ_DATA_DIR = BASE_DIR / 'visualizations' / 'data'


@app.route('/')
def index():
    """Main dashboard page - seamless version"""
    return render_template('dashboard.html')

@app.route('/advanced')
def advanced():
    """Advanced dashboard with dark theme"""
    return render_template('index.html')


@app.route('/api/feature-importance')
def api_feature_importance():
    """Get feature importance data"""
    try:
        with open(VIZ_DATA_DIR / 'feature_importance.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Data not found. Please run the model training first.'}), 404


@app.route('/api/shape-functions')
def api_shape_functions():
    """Get shape functions data"""
    try:
        with open(VIZ_DATA_DIR / 'shape_functions.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Data not found. Please run the model training first.'}), 404


@app.route('/api/country-predictions')
def api_country_predictions():
    """Get country predictions and explanations"""
    try:
        with open(VIZ_DATA_DIR / 'country_predictions.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Data not found. Please run the model training first.'}), 404


@app.route('/api/model-metadata')
def api_model_metadata():
    """Get model metadata"""
    try:
        with open(VIZ_DATA_DIR / 'model_metadata.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Data not found. Please run the model training first.'}), 404


@app.route('/visualizations/data/<path:filename>')
def serve_viz_data(filename):
    """Serve visualization data files"""
    return send_from_directory(VIZ_DATA_DIR, filename)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    print("="*80)
    print("GLOBAL DIGITAL SKILLS GAP NAVIGATOR - WEB SERVER")
    print("="*80)
    print("\n✓ Starting server...")
    print(f"✓ Base directory: {BASE_DIR}")
    print(f"✓ Visualization data: {VIZ_DATA_DIR}")
    print("\n🌐 Open your browser to: http://localhost:5001")
    print("\nPress Ctrl+C to stop the server")
    print("="*80)

    app.run(debug=True, host='0.0.0.0', port=5001)

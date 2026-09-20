from flask import Flask, render_template, jsonify, request
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core import simulate, fmt_iec, sci

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    data = request.json
    branching = min(int(data.get('branching', 16)), 1000)
    level = min(int(data.get('level', 50)), 200)
    payload = min(int(data.get('payload', 43)), 10000)
    payload_type = data.get('payload_type', 'zeros')
    
    r = simulate(branching, level, payload, payload_type)
    
    return jsonify({
        'config': {
            'branching': r['branching'],
            'level': r['level'],
            'payload': r['payload'],
            'payload_type': r['payload_type'],
        },
        'results': {
            'total_files': r['total_files'],
            'total_files_sci': sci(r['total_files']),
            'total_files_digits': int(math.log10(r['total_files'])) + 1,
            'total_bytes': r['total_bytes'],
            'zip_size': r['zip_size'],
            'zip_size_human': fmt_iec(r['zip_size']),
            'ratio': r['ratio'],
            'ratio_sci': sci(r['ratio']),
        },
        'levels': [
            {
                'depth': l['depth'],
                'zip_size': l['zip_size'],
                'zip_size_human': fmt_iec(l['zip_size']),
                'files': l['files'],
                'files_sci': sci(l['files']),
                'uncompressed': l['uncompressed'],
                'ratio': l['ratio'],
                'ratio_sci': sci(l['ratio']),
            }
            for l in r['levels']
        ],
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

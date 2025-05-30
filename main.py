
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bypass', methods=['POST'])
def bypass_link():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Call the bypass API
        api_url = f"https://api.solar-x.top/free/bypass?url={url}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            result = response.text.strip()
            
            # Try to parse as JSON first
            try:
                import json
                parsed = json.loads(result)
                if isinstance(parsed, dict) and 'result' in parsed:
                    result = parsed['result']
                elif isinstance(parsed, dict) and 'url' in parsed:
                    result = parsed['url']
            except json.JSONDecodeError:
                # If not JSON, use the text as is
                pass
            
            return jsonify({'success': True, 'result': result})
        else:
            return jsonify({'error': f'API returned status code {response.status_code}'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

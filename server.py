import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# Helper functions

def call_model(prompt: str, context: str = "") -> str:
    payload = {
        "model": "devstral:24b",
        "prompt": prompt,
        "context": context
    }
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    if resp.ok:
        data = resp.json()
        return data.get("response", "")
    return ""


def read_project_context(project_path: str) -> str:
    contents = []
    for root, _dirs, files in os.walk(project_path):
        for fname in files:
            if fname.endswith(('.java', '.xml', '.properties', '.gradle', '.md', '.txt', '.sql')):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        contents.append(f"===== {fpath} =====\n" + f.read())
                except Exception as exc:
                    contents.append(f"Error reading {fpath}: {exc}\n")
    return "\n".join(contents)

# Endpoint definitions

@app.route('/create-file', methods=['POST'])
def create_file():
    data = request.json
    path = data.get('path')
    content = data.get('content', '')
    if not path:
        return jsonify({'error': 'path missing'}), 400
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'status': 'created', 'path': path})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@app.route('/modify-java-class', methods=['POST'])
def modify_java_class():
    data = request.json
    path = data.get('path')
    patch = data.get('patch', '')
    if not path:
        return jsonify({'error': 'path missing'}), 400
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines.append("\n" + patch + "\n")
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return jsonify({'status': 'modified', 'path': path})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@app.route('/project-context', methods=['GET'])
def project_context():
    project_path = request.args.get('path', '.')
    context = read_project_context(project_path)
    return jsonify({'context': context})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    context = data.get('context', '')
    result = call_model(prompt, context)
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

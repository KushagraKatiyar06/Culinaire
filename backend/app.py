import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
from transcript import getVideoID, getVideoMetadata
from recipe import generateRecipe

app = Flask(__name__)
CORS(app)

@app.route('/get-metadata', methods=['POST'])
def getMetadata():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "no url provided"}), 400
    
    try:
        videoID = getVideoID(url)
        if not videoID:
             return jsonify({"error": "invalid youtube url"}), 400
        
        metaData = getVideoMetadata(videoID)
        
        return jsonify(metaData), 200
    
    except Exception as e:
        print(f"metadata error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-recipe', methods=['POST'])
def getRecipe():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        recipe = generateRecipe(url)
        if recipe is None:
            return jsonify({"error": "Could not generate recipe"}), 500
        
        return jsonify(recipe.dict()), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def healthCheck():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("-" * 30)
    print(f"Server is starting!")
    print(f"Local URL for React Native: http://{local_ip}:5000")
    print("-" * 30)

    app.run(debug=True, host='0.0.0.0', port=5000)


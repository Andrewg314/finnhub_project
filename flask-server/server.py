from flask import Flask, jsonify
import finnhub
import API_KEY
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/api/quotes", methods=['GET'])
def quotes():
    key = API_KEY.apiKey
    finnhub_client = finnhub.Client(api_key=key)
    return jsonify(
        {
            "AMD": finnhub_client.quote('AMD'),
            "NVDA": finnhub_client.quote('NVDA')
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
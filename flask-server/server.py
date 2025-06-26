from flask import Flask, jsonify
import finnhub
import API_KEY

app = Flask(__name__)

@app.route("/api/quotes", methods=['GET'])
def quotes():
    api_key = API_KEY.apiKey
    finnhub_client = finnhub.Client(api_key="{api_key}")
    return jsonify(
        {
            "AAPL": finnhub_client.quote('AAPL')
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
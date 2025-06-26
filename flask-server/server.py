from flask import Flask, jsonify
import finnhub
import API_KEY

app = Flask(__name__)

@app.route("/api/quotes", methods=['GET'])
def quotes():
    key = API_KEY.apiKey
    finnhub_client = finnhub.Client(api_key=key)
    return jsonify(
        {
            "Apple": finnhub_client.quote('AAPL'),
            "NVDIA": finnhub_client.quote('NVDA'),
            "Amazon": finnhub_client.quote('AMZN'),
            "Tesla": finnhub_client.quote('TSLA')
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, jsonify
import finnhub
import API_KEY

app = Flask(__name__)

@app.route("/api/quotes", methods=['GET'])
def quotes():
    finnhub_client = finnhub.Client(api_key="{APIKEY}")
    return jsonify(
        {
            "AAPL": finnhub_client.quote('AAPL')
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
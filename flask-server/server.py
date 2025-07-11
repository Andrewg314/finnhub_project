import finnhub
from flask import Flask, jsonify
import login
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
cors = CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{login.dbPassword}@localhost/quotes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StockQuote(db.Model):
    __tablename__ = 'stock_quotes'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Numeric(12, 4), nullable=False)
    change = db.Column(db.Numeric(12, 4), nullable=False)
    percent_change = db.Column(db.Numeric(6, 4), nullable=False)
    high_price = db.Column(db.Numeric(12, 4), nullable=False)
    low_price = db.Column(db.Numeric(12, 4), nullable=False)
    open_price = db.Column(db.Numeric(12, 4), nullable=False)
    prev_close_price = db.Column(db.Numeric(12, 4), nullable=False)
    timestamp_unix = db.Column(db.BigInteger, nullable=False)

    __table_args__ = (db.UniqueConstraint('symbol', 'timestamp_unix'),)

def fetch_and_store_quotes():
    finnhub_client = finnhub.Client(api_key=login.apiKey)
    symbols = ['AMD', 'NVDA']

    for symbol in symbols:
        data = finnhub_client.quote(symbol)

        exists = StockQuote.query.filter_by(symbol=symbol, timestamp_unix=data['t']).first()
        if not exists:
            quote = StockQuote(
                symbol=symbol,
                price=data['c'],
                change=data['d'],
                percent_change=data['dp'],
                high_price=data['h'],
                low_price=data['l'],
                open_price=data['o'],
                prev_close_price=data['pc'],
                timestamp_unix=data['t']
            )
            db.session.add(quote)
            db.session.commit()

@app.route("/api/quotes", methods=['GET'])
def quotes():
    quotes = StockQuote.query.order_by(StockQuote.timestamp_unix.desc()).limit(10).all()
    results = [{
        "symbol": quote.symbol,
        "price": float(quote.price),
        "change": float(quote.change),
        "percent_change": float(quote.percent_change),
        "high_price": float(quote.high_price),
        "low_price": float(quote.low_price),
        "open_price": float(quote.open_price),
        "prev_close_price": float(quote.prev_close_price),
        "timestamp_unix": quote.timestamp_unix
    } for quote in quotes]
    return jsonify(results)

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_store_quotes, trigger="interval", minutes=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True, port=5000)

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
symbols = ['AMD', 'NVDA']

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
    with app.app_context():
        finnhub_client = finnhub.Client(api_key=login.apiKey)

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
    latest_quotes = []
    for symbol in symbols:
        latest_q = (
            StockQuote.query
            .filter_by(symbol=symbol)
            .order_by(StockQuote.timestamp_unix.desc())
            .first()
        )

        if latest_q:
            latest_quotes.append({
                "id": latest_q.id,
                "symbol": latest_q.symbol,
                "price": float(latest_q.price),
                "change": float(latest_q.change),
                "percent_change": float(latest_q.percent_change),
                "high_price": float(latest_q.high_price),
                "low_price": float(latest_q.low_price),
                "open_price": float(latest_q.open_price),
                "prev_close_price": float(latest_q.prev_close_price),
                "timestamp_unix": latest_q.timestamp_unix
            })
    return jsonify(latest_quotes)

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_store_quotes, trigger="interval", minutes=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
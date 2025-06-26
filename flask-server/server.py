from flask import Flask, jsonify
import finnhub

finnhub_client = finnhub.Client(api_key="d1atfdpr01qjhvtr9k00d1atfdpr01qjhvtr9k0g")

print(finnhub_client.quote('AAPL'))
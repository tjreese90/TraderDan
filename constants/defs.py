API_KEY = "48407535e759c72dc2cb45329f0cc6a8-4151784dcad97aaa0ada707761d3c560"
ACCOUNT_ID = "101-001-24345029-002"
URL = "https://api-fxpractice.oanda.com/v3/"


SECURE_HEADER = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type" : "application/json"
        }

SELL = -1
BUY = 1
NONE = 0

MONGO_CONN_STR="mongodb+srv://admin:Lowso900@cluster0.allolgl.mongodb.net/?retryWrites=true&w=majority"
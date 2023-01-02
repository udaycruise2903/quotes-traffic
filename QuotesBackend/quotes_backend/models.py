from SQLAlchemy import func
from quotes_backend.db import db 


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    text = db.Column(db.String(250))
    timestamp = db.Column(db.Datetime, server_default=func.now())
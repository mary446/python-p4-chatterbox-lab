# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.sql import func
# from sqlalchemy import DateTime
# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)

# class Message(db.Model, SerializerMixin):
#     __tablename__ = 'messages'

#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String)
#     username = db.Column(db.String)
#     created_at = db.Column(db.DateTime, default=func.now())
#     updated_at = db.Column(db.DateTime, onupdate = func.now())

    

#     def __repr__(self):
#         return f"Message(id={self.id}, body='{self.body}', username='{self.username}')"
     
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'<Message {self.body}, {self.username}>'
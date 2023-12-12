from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True # в столбик
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(20))
    phone = db.Column(db.String(20))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    adress = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.drop_all()
    db.create_all()

    def data_users():
        with open('user.txt', encoding='utf-8') as users:
            users_data = eval(users.read())
            return users_data

    for u in data_users():
        user = User(
            id=u['id'],
            first_name=u['first_name'],
            last_name=u['last_name'],
            age=u['age'],
            email=u['email'],
            role=u['role'],
            phone=u['phone']
        )
        db.session.add(user)

#============================================================

    def data_offer():
        with open('offer.txt', encoding='utf-8') as offer:
            offer_data = eval(offer.read())
            return offer_data

    for of in data_offer():
        offer = Offer(
            id=of['id'],
            order_id=of['order_id'],
            executor_id=of['executor_id'])

        db.session.add(offer)

# ============================================================

    def data_order():
        with open('order.txt', encoding='utf-8') as order:
            order_data = eval(order.read())
            return order_data


    for o in data_order():
        start_date = datetime.strptime(o['start_date'], '%m/%d/%Y').date()
        end_date = datetime.strptime(o['end_date'], '%m/%d/%Y').date()

        order = Order(
            id=o['id'],
            name=o['name'],
            description=o['description'],
            start_date=start_date,
            end_date=end_date,
            adress=o['adress'],
            price=o['price'],
            customer_id=o['customer_id'],
            executor_id=o['executor_id']
        )
        db.session.add(order)


        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка: {e}")
        finally:
            db.session.close()


from views import *

if __name__ == '__main__':
    app.run(debug=True)

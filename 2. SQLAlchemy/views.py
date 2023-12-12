from app import *

@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    user_response = []
    if request.method == 'GET':
        for user in User.query.all():
            user_response.append({
            'id':user.id,
            'first_name':user.first_name,
            'age':user.age,
            'role': user.role,
            })
        return jsonify(user_response)

    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            age=data['age']
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'first_name': new_user.first_name,
            'age': new_user.age
        })


@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def get_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        if not user:
            return 'User not found', 404

        user_response = {
            'id':user.id,
            'first_name':user.first_name,
            'age':user.age,
            'role': user.role,
        }
        return jsonify(user_response)

    elif request.method == 'PUT':
        if user:
            data = request.get_json()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.age = data['age']
            user.email = data['email']
            user.role = data['role']
            user.phone = data['phone']

            db.session.add(user)
            db.session.commit()

            return '', 203
        else:
            return 'Нет такого пользователя'

    elif request.method == 'PATCH':
        if user:
            data = request.get_json()
            user.first_name = data['first_name']

            db.session.add(user)
            db.session.commit()

            return '', 203
        else:
            return 'Нет такого пользователя'

    elif request.method == 'DELETE':
        if user:
            db.session.delete(user)
            db.session.commit()
            return ''
        else:
            return 'Нет такого пользователя'

#================================================================================================

@app.route('/offers')
def get_offers():
    offer_list = Offer.query.all()

    offer_response = []

    for offer in offer_list:
        offer_response.append({
        'id':offer.id,
        'order_id':offer.order_id,
        'executor_id':offer.executor_id,
        })
    return jsonify(offer_response)


@app.route('/offer/<int:offer_id>')
def get_offer(offer_id):
    offer = Offer.query.get(offer_id)

    if not offer:
        return 'Offer not found', 404

    offer_response = {
        'id':offer.id,
        'order_id':offer.order_id,
        'executor_id':offer.executor_id,
    }
    return jsonify(offer_response)
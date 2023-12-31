from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    # для аутентификации
    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.email == username).first()

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))

        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()

    def partial_update(self, user_d):
        user = self.get_one(user_d.get("id"))

        for key, value in user_d.items():
            setattr(user, key, value)
        self.session.commit()

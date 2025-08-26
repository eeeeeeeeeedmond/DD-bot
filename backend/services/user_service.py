import bcrypt
from sqlmodel import Session, select
from .. import models

class UserService():

    def __init__(self, session:Session):
        self.session = session

    # only parents and librarians register accounts
    def registerAccount(self, user_data: models.UserRegister) -> bool:

        # check if username or email exists in users tables first
        statement = select(models.Users).where(
            (models.Users.username == user_data.username) |
            (models.Users.email == user_data.email)
        )

        existing_user = self.session.exec(statement).first()

        # if exists return false
        if existing_user:
            return False
        
        # if not exists hash pw
        password_bytes = user_data.password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        # get role based on role type
        role_statement = select(models.Roles).where(models.Roles.name == user_data.usertype.value)
        role = self.session.exec(role_statement).one()

        # create the user
        new_parent = models.Users(
            username = user_data.username,
            email = user_data.email,
            password_hash = password_hashed,
            role_id = role.role_id
        )

        self.session.add(new_parent)
        self.session.commit()
        self.session.refresh(new_parent)


        return True
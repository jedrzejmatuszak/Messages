from crypto import password_hash, check_password


class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None
    table_name = "Users"

    def __init__(self, username, email):
        self.__id = -1
        self.username = username
        self.__hashed_password = ""
        self.email = email

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt=None):
        self.__hashed_password = password_hash(password, salt)

    def check_password(self, password):
        return check_password(password, self.__hashed_password)

    def save_to_database(self, cursor):
        if self.__id == -1:
            sql = f"""Insert into {User.table_name} (username, email, hashed_password)
                      values ('{self.username}', '{self.email}', '{self.hashed_password}') returning id;"""
            cursor.execute(sql)
            dane = cursor.fetchone()
            self.__id = dane[0]
            return True
        else:
            sql = f"""update users set 
                     username = '{self.username}',
                     email = '{self.email}',
                     hashed_password = '{self.hashed_password}'
                     where id = '{self.id}';
            """
            cursor.execute(sql)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = f"select id, email, username, hashed_password from users where id = {user_id};"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User(data[2], data[1])
            loaded_user.__id = data[0]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return False

    @staticmethod
    def load_user_by_username(cursor, user_name):
        sql = f"select id, email, username, hashed_password from users where username = '{user_name}';"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User(data[2], data[1])
            loaded_user.__id = data[0]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return False

    @staticmethod
    def load_all_user(cursor):
        sql = f"select id, email, username, hashed_password from users;"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User(str(row[2]), str(row[1]))
            loaded_user.__id = row[0]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        if self.__id != -1:
            sql = f"delete from users where id = {self.id};"
            cursor.execute(sql)
            self.__id = -1
            return True


class Message:
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None
    table_name = "message"

    def __init__(self, from_id, to_id, text):
        self.__id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_message_by_id(message_id, cursor):
        sql = f"select id, from_id, to_id, text, creation_date from {Message.table_name} where id = {message_id};"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_message = Message(data[1], data[2], data[3])
            loaded_message.__id = data[0]
            loaded_message.creation_date = data[4]
            return loaded_message

    @staticmethod
    def load_all_messages_to_user(to_id, cursor):
        sql = f"select id, from_id, to_id, text, creation_date from {Message.table_name} where to_id = {to_id};"
        cursor.execute(sql)
        ret = []
        for row in cursor.fetchall():
            loaded_message = Message(row[1], row[2], row[3])
            loaded_message.__id = row[0]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = f"select id, from_id, to_id, text, creation_date from {Message.table_name};"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message(row[1], row[2], row[3])
            loaded_message.__id = row[0]
            loaded_message.creation_date = row[4]
            ret.append(loaded_message)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = f"""Insert into {Message.table_name} (from_id, to_id, text, creation_date)
                      values ('{self.from_id}', '{self.to_id}', '{self.text}', current_timestamp) returning id;"""
            cursor.execute(sql)
            dane = cursor.fetchone()
            self.__id = dane[0]
            return True

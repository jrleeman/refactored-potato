MOCK_USERS = [{'email':'test@example.com',
               'salt': '8Fb23mMNHD5Zb8pr2qWA3PE9bH0=',
               'hashed': '102ee513873376ddab29e8e6bc0abb2768ca965f13ad3e953b69a500c2e3ec85eeddf4a5d6b5577e48eca3c7b59f1442c681947e952208ee1ea014122348c45e'}
               ]

class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None


    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({'email': email,
                           'salt': salt,
                           'hashed': hashed})

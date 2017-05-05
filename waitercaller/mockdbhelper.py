MOCK_USERS = [{'email':'test@example.com',
               'salt': 'E0XDvm/7wWwMMrU707ybm2SW0Y0=',
               'hashed': '58a76a944906787e13a2db88aa86f95b4b4ffb5aad95ea3a938dc0447384b46bf78a1cea5f37001f4a277420cb3c140526b501864a01512268154fcf81375b68'}
               ]

MOCK_TABLES = [{"_id": "1", "number": 1, "owner": "test@example.com", "url": "mockurl"}]

class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None


    def add_user(self, email, salt, hashed):
        print(email, salt, hashed)
        MOCK_USERS.append({'email': email,
                           'salt': salt,
                           'hashed': hashed})


    def add_table(self, number, owner):
        MOCK_TABLES.append({"_id":number, "number":number, "owner":owner})
        return number


    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get("_id") == _id:
                table["url"] = url
                break


    def get_tables(self, owner_id):
        return MOCK_TABLES


    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get('_id') == table_id:
                del MOCK_TABLES[i]
                break

import json
import uuid

from models import Blacklist, db


class TestCreateUser:

    def setup_method(self):
        self.token = "some_token"
        self.blacklistOne = Blacklist(
                            email="email@gmail.com", 
                            app_uuid=uuid.UUID("a3fa2036-67f9-4e3b-9e5f-fd175600e4b7"),
                            blocked_reason="some reason",
                            ip_address="192.168.0.1"
                            )
        
        self.blacklist_data = {
            "email" : "email@gmail.com",
            "app_uuid" : "a3fa2036-67f9-4e3b-9e5f-fd175600e4b7",
            "blocked_reason": "some blocked reason"
        }

        self.blacklist_data_without_email = {
            "app_uuid" : "a3fa2036-67f9-4e3b-9e5f-fd175600e4b7",
            "blocked_reason": "some blocked reason"
        }

    def teardown_method(self):
        db.session.rollback()
        Blacklist.query.delete()

    def sendRequest(self, client, headers, data: dict = None):
        json_request_data = data or self.blacklist_data
        json_data = json.dumps(json_request_data)
        self.response = client.post('/blacklists', data=json_data, headers=headers)
        self.json_response = self.response.json

    def test_blacklist_item_created_successful_in_db(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        self.sendRequest(client=client, headers=headers)
        blacklist_created_db = Blacklist.query.all()
        assert len(blacklist_created_db) == 1
        assert self.response.status_code == 201
    
    def test_blacklist_item_not_created_in_db_because_token_not_was_passed(self, client):
        headers = {'Content-Type': 'application/json'}
        self.sendRequest(client=client, headers=headers)
        user_created_db = Blacklist.query.all()
        assert len(user_created_db) == 0
        assert self.json_response["message"] == 'The token is required'
        assert self.response.status_code == 403
    
    def test_blacklist_item_not_created_in_db_because_token_is_bad(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {"bad_token"}'}
        self.sendRequest(client=client, headers=headers)
        user_created_db = Blacklist.query.all()
        assert len(user_created_db) == 0
        assert self.json_response["message"] == 'The token is invalid'
        assert self.response.status_code == 401
    
    def test_blacklist_item_not_created_in_db_because_email_was_not_sent(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        self.sendRequest(client=client, headers=headers, data=self.blacklist_data_without_email)
        user_created_db = Blacklist.query.all()
        assert len(user_created_db) == 0
        assert self.response.status_code == 400
    
    def test_blacklist_not_created_in_db_because_email_already_exists(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        db.session.add(self.blacklistOne)
        db.session.commit()
        self.sendRequest(client=client, headers=headers)
        user_created_db = Blacklist.query.all()
        assert len(user_created_db) == 1
        assert self.json_response["message"] == 'Email or app_uuid already exists, the account could not be created'
        assert self.response.status_code == 412
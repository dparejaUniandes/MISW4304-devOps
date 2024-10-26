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

        self.blacklist_data_without_email = {
            "app_uuid" : "a3fa2036-67f9-4e3b-9e5f-fd175600e4b7",
            "blocked_reason": "some blocked reason"
        }

    def teardown_method(self):
        db.session.rollback()
        Blacklist.query.delete()

    def sendRequest(self, client, headers, email):
        self.response = client.get(f'/blacklists/{email}', headers=headers)
        self.json_response = self.response.json

    def test_blacklist_item_get_successful_in_db(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        db.session.add(self.blacklistOne)
        db.session.commit()
        self.sendRequest(client=client, headers=headers, email="email@gmail.com")
        assert self.json_response["is_email_present"] == True
        assert self.response.status_code == 200
    
    def test_blacklist_item_get_error_token_not_sent(self, client):
        headers = {'Content-Type': 'application/json'}
        db.session.add(self.blacklistOne)
        db.session.commit()
        self.sendRequest(client=client, headers=headers, email="email@gmail.com")
        assert self.response.status_code == 403
    
    def test_blacklist_item_get_token_invalid(self, client):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {"bad token"}'}
        db.session.add(self.blacklistOne)
        db.session.commit()
        self.sendRequest(client=client, headers=headers, email="email@gmail.com")
        assert self.response.status_code == 401
import sys

from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from models import *

blacklistSchema = BlacklistSchema()
token = "some_token"

class BlacklistsView(Resource):
    def post(self):
        try:
            headersRequest = request.headers
            bearer = headersRequest.get('Authorization')
            if bearer is None:
                return {"message": "The token is required"}, 403
            tokenRequest = bearer.split()[1]
            if token != tokenRequest:
                return {"message": "The token is invalid"}, 401
            blacklist = blacklistSchema.load(request.json, session=db.session)
            email=blacklist.email
            app_uuid=blacklist.app_uuid
            blocked_reason=blacklist.blocked_reason
            if not(email and app_uuid and blocked_reason):
                return {"message": 'All fields are needed'}, 400
            ip_address = request.remote_addr
            
            newItemBlacklist = Blacklist(
                            email=email,
                            app_uuid=app_uuid, 
                            blocked_reason=blocked_reason,
                            ip_address=ip_address
                        )
            db.session.add(newItemBlacklist)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return {"message": 'Email or app_uuid already exists, the account could not be created'}, 412
        except ValidationError as me:
            return {"message": '{}'.format(me)}, 400
        except:
            db.session.rollback()
            print("Internal Error:  " , sys.exc_info())
            return {"message": 'Internal server error, the account could not be created', "error": sys.exc_info()}, 500
        return {"message": "The account could be created successfully"}, 201

class BlacklistView(Resource):
    def get(self, email):
        headersRequest = request.headers
        bearer = headersRequest.get('Authorization')
        if bearer is None:
            return {"message": "The token is required"}, 403
        tokenRequest = bearer.split()[1]
        if token != tokenRequest:
            return {"message": "The token is invalid"}, 401
        blacklist = Blacklist.query.filter(Blacklist.email == email).first()
        if not blacklist:
            return {"is_email_present": False}, 404
        return {"is_email_present": True, "reason": blacklist.blocked_reason}, 200
__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'

import planit_appcodes
from neoapi import application_codes
import planit_error
from flask import Flask, request
from constants import AuthenticationLevels
from neomodel import (StringProperty, AliasProperty, RelationshipTo, Relationship, ZeroOrOne,
                      FloatProperty, ZeroOrMore, OneOrMore, IntegerProperty, RelationshipFrom, DoesNotExist)
from user import User, UserRoles
from event import Event
from category import Category
import json
from datetime import datetime

app = Flask(__name__)


# API CHECK#############################################################################################################


@app.route('/', methods=['GET'])
@app.route('/v1', methods=['GET'])
def index():
    """ Call this method for basic version info or to ensure the api is running. """
    return 'This is version 1 of the PlanIt API.  The API is running.'


# AUTHENTICATION########################################################################################################


def authenticate(level=AuthenticationLevels.ANY, user_id=None):
    def authenticate_decorator(func):
        def func_wrapper(*args, **kwargs):
            response = None
            with app.app_context():  # change the context in order to allow for use of request
                try:  # fetch the user by id
                    token = request.headers['Authorization']
                    the_user = User.nodes.get(id=token)  # fetch the user by id
                    if level == AuthenticationLevels.ANY:
                        pass
                    if level == AuthenticationLevels.USER and the_user.id != user_id:
                        raise planit_error.WrongUserError()
                    if level == AuthenticationLevels.EVENT_CREATOR and the_user.role not in [
                            UserRoles.EVENT_CREATOR_ROLE, UserRoles.ADMIN_ROLE]:
                        raise planit_error.Forbidden()
                    if level == AuthenticationLevels.ADMIN and the_user.role != UserRoles.ADMIN_ROLE:
                        raise planit_error.Forbidden()
                    response = func(*args, **kwargs)

                except DoesNotExist:  # return an error message if token is bad
                    response = application_codes.error_response([application_codes.BAD_AUTHENTICATION])
                except KeyError:  # return an error message if authentication not provided
                    response = application_codes.error_response([application_codes.NO_AUTHENTICATION])
                except planit_error.WrongUserError:
                    response = application_codes.error_response([planit_appcodes.WRONG_USER])
                except planit_error.Forbidden:
                    response = application_codes.error_response([application_codes.FORBIDDEN_VIOLATION])

            return response

        return func_wrapper
    return authenticate_decorator


# USER METHODS##########################################################################################################


@app.route('/v1/users/<id>', methods=['GET', 'PATCH', 'DELETE'])
@app.route('/v1/users', defaults={'id': None}, methods=['POST', 'GET'])
def user_wrapper(id):
    """Methods related to the user resource"""
    response = None

    def post_user():
        return User.create_resource(eval(request.data))

    @authenticate(AuthenticationLevels.USER, id)
    def patch_user():
        return User.update_resource(eval(request.data), id)

    @authenticate(AuthenticationLevels.USER, id)
    def delete_user():
        return User.deactivate_resource(id)

    @authenticate()
    def get_user():
        return User.get_resource(request.args, id)

    @authenticate()
    def get_user_collection():
        return User.get_collection(request.args)

    # pick method to execute
    if request.method == 'POST':  # no auth required
        response = post_user()
    elif request.method == 'PATCH':  # must be user
        response = patch_user()
    elif request.method == 'DELETE':  # must be user
        response = delete_user()
    elif request.method == 'GET' and id:  # must be user
        response = get_user()
    elif request.method == 'GET':  # must be administrator
        response = get_user_collection()
    return response


@app.route('/v1/users/<id>/relationships/<related_collection_name>', methods=['POST', 'PATCH', 'DELETE', 'GET'])
def user_relationships_wrapper(id, related_collection_name):
    """Methods related to user relationships"""

    @authenticate(AuthenticationLevels.USER, id)  # All methods require user perform the action on themselves
    def user_relationships():
        response = None
        if request.method == 'POST':
            response = User.create_relationships(id, related_collection_name, eval(request.data))
        elif request.method == 'PATCH':
            response = User.update_relationship(id, related_collection_name, json.loads(request.data))
        elif request.method == 'DELETE':
            response = User.disconnect_relationship(id, related_collection_name, eval(request.data))
        elif request.method == 'GET':
            response = User.get_relationship(request.args, id, related_collection_name)
        return response
    return user_relationships()


# EVENT METHODS#########################################################################################################


@app.route('/v1/events/<id>', methods=['GET', 'PATCH', 'DELETE'])
@app.route('/v1/events', defaults={'id': None}, methods=['POST', 'GET'])
def event_wrapper(id):
    """Methods related to the event resource"""
    response = None

    try:
        event_creator = Event.nodes.get(id=id).owner.single().id
    except DoesNotExist:
        event_creator = None

    @authenticate(AuthenticationLevels.EVENT_CREATOR)
    def post_event():
        req_data = eval(request.data)
        try:  # convert dates to datetime format
            st = req_data['data']['attributes'].get('start_time')
            et = req_data['data']['attributes'].get('end_time')
            # set the owner
            req_data['data']['relationships']['owner'] = dict()
            req_data['data']['relationships']['owner']['data'] = {'id': request.headers['Authorization'], 'type': 'users'}
            if st:
                req_data['data']['attributes']['start_time'] = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
            if et:
                req_data['data']['attributes']['end_time'] = datetime.strptime(et, '%Y-%m-%d %H:%M:%S')

        except KeyError:
            return application_codes.error_response([application_codes.BAD_FORMAT_VIOLATION])

        # set the owner

        return Event.create_resource(req_data)

    @authenticate(AuthenticationLevels.USER, event_creator)  # user who created the event only one allowed to update it
    def patch_event():
        req_data = eval(request.data)
        try:  # convert dates to datetime format
            st = req_data['data']['attributes'].get('start_time')
            et = req_data['data']['attributes'].get('end_time')
            if st:
                req_data['data']['attributes']['start_time'] = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
            if et:
                req_data['data']['attributes']['start_time'] = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
        except KeyError:
            pass
        return Event.update_resource(req_data, id)

    @authenticate(AuthenticationLevels.USER, event_creator)
    def delete_event():
        return Event.deactivate_resource(id)

    @authenticate()
    def get_event():
        resp = Event.get_resource(request.args, id)
        return resp

    @authenticate()
    def get_event_collection():
        "Hacky ass endpoint.  This will incorporated into get_resource the get_event endpoint"
        resp =  Event.get_collection(request.args)
        cat_list = request.args.get('category_list', '[]')
        cat_list = eval(cat_list)  # expects type list
        resp_data = json.loads(resp.get_data())
        resp_data_temp = resp_data
        for i, event in enumerate(resp_data_temp['data']):
            remove_event = True
            for category in event['relationships']['categories']['data']:
                if category['id'] in cat_list:
                    remove_event = False
                    print "do not remove"
            if remove_event:
                print "i am here"
                print resp_data['data'][i]
                del resp_data['data'][i]

        resp.set_data(json.dumps(resp_data))

        return resp

    # pick method to execute
    if request.method == 'POST':  # no auth required
        response = post_event()
    elif request.method == 'PATCH':  # must be user
        response = patch_event()
    elif request.method == 'DELETE':  # must be user
        response = delete_event()
    elif request.method == 'GET' and id:  # must be user
        response = get_event()
    elif request.method == 'GET':  # must be administrator
        response = get_event_collection()
    return response


@app.route('/v1/event/<id>/relationships/<related_collection_name>', methods=['POST', 'PATCH', 'DELETE', 'GET'])
def event_relationships_wrapper(id, related_collection_name):
    """Methods related to event relationships"""

    try:
        event_creator = Event.nodes.get(id=id).single().user.id
    except DoesNotExist:
        event_creator = None

    @authenticate(AuthenticationLevels.USER, event_creator)  # All methods require user perform the action on themselves
    def event_relationships():
        response = None
        if request.method == 'POST':
            response = Event.create_relationships(id, related_collection_name, eval(request.data))
        elif request.method == 'PATCH':
            response = Event.update_relationship(id, related_collection_name, json.loads(request.data))
        elif request.method == 'DELETE':
            response = Event.disconnect_relationship(id, related_collection_name, eval(request.data))
        elif request.method == 'GET':
            response = Event.get_relationship(request.args, id, related_collection_name)
        return response
    return event_relationships()


# CATEGORY METHODS######################################################################################################


@app.route('/v1/categories/<id>', methods=['GET', 'PATCH', 'DELETE'])
@app.route('/v1/categories', defaults={'id': None}, methods=['POST', 'GET'])
def category_wrapper(id):
    """Methods related to the user resource"""
    response = None

    @authenticate(AuthenticationLevels.ADMIN)
    def post_category():
        return Category.create_resource(eval(request.data))

    @authenticate(AuthenticationLevels.ADMIN)
    def patch_category():
        return Category.update_resource(eval(request.data), id)

    @authenticate(AuthenticationLevels.ADMIN)
    def delete_category():
        return Category.deactivate_resource(id)

    @authenticate()
    def get_category():
        return Category.get_resource(request.args, id)

    @authenticate()
    def get_category_collection():
        return Category.get_collection(request.args)

    # pick method to execute
    if request.method == 'POST':  # no auth required
        response = post_category()
    elif request.method == 'PATCH':  # must be user
        response = patch_category()
    elif request.method == 'DELETE':  # must be user
        response = delete_category()
    elif request.method == 'GET' and id:  # must be user
        response = get_category()
    elif request.method == 'GET':  # must be administrator
        response = get_category_collection()
    return response


@app.route('/v1/categories/<id>/relationships/<related_collection_name>', methods=['POST', 'PATCH', 'DELETE', 'GET'])
def category_relationships_wrapper(id, related_collection_name):
    """Methods related to user relationships"""

    @authenticate(AuthenticationLevels.ADMIN)  # All methods require user perform the action on themselves
    def category_relationships():
        response = None
        if request.method == 'POST':
            response = Category.create_relationships(id, related_collection_name, eval(request.data))
        elif request.method == 'PATCH':
            response = Category.update_relationship(id, related_collection_name, json.loads(request.data))
        elif request.method == 'DELETE':
            response = Category.disconnect_relationship(id, related_collection_name, eval(request.data))
        elif request.method == 'GET':
            response = Category.get_relationship(request.args, id, related_collection_name)
        return response
    return category_relationships()


# ERROR HANDLING########################################################################################################


@app.errorhandler(404)
def not_found(error):
    return application_codes.error_response([application_codes.RESOURCE_NOT_FOUND])


@app.errorhandler(405)
def method_not_allowed(error):
    return application_codes.error_response([application_codes.METHOD_NOT_ALLOWED])


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10200, debug=True)

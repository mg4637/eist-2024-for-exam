from flask import Blueprint, request, current_app, Response
import http.client
from ff import Entry


api = Blueprint("api", __name__, template_folder="templates")

# Messages
#   use "MESSAGWE % (param1, param2, ...)" to insert parameters into message
KEY_DOES_NOT_EXIST = "Key %s does not exist!"
NO_UID_IN_REEQUEST_BODY = "No 'uid' in request body. The request must provide user id!"
NO_ACCESS_TO_ENTRY = "Cannot access the content associated with key %s. Owned by other user!"
NO_CONTENT_IN_REQUEST_BODY = "No 'content' in request body. The request must provide the content!"
NO_SPACE_IN_FILE_FOLDER = "Failed to add the content. No empty space!"
PUT_SUCCESS = "Successfully added the content."

# Response status
#   create a response like this:
#   response = Response(message, status=OK)
OK = http.client.OK                   # 200
BAD_REQUEST = http.client.BAD_REQUEST  # 400
NOT_FOUND = http.client.NOT_FOUND     # 404


####################################################
# TODO: Implement the endpoints of the RESTful API #
####################################################

@api.route("/<key>", methods=["GET"])
def get(key):
    """
    Retrieve the file-content associated with the given key owned by the user.
    If there is no user-id `uid` given in the request body or the user-id does not match, return error message and status.
    Otherwise, return the file-content and success status.
    """
    request_body = request.json

    if 'uid' not in request_body:
        return Response(NO_UID_IN_REEQUEST_BODY, status=BAD_REQUEST)

    uid = request_body['uid']
    ff = current_app.ff
    entry = ff.get(key)

    if entry is None:
        return Response(KEY_DOES_NOT_EXIST % "test_key", status=NOT_FOUND)

    if entry.uid != uid:
        return Response(NO_ACCESS_TO_ENTRY % "test_key", status=BAD_REQUEST)

    return Response(entry.content, status=OK)

@api.route("/<key>", methods=["POST"])
def put(key):
    """
    Upsert a file-content associated with the given key owned by the user.
    If there is no user-id `uid` or file-content `content` given in the request body, return error message and status.
    Otherwise, return the success message and success status
    """
    request_body = request.json
    ff = current_app.ff

    if 'uid' not in request_body:
        return Response(NO_UID_IN_REEQUEST_BODY, status=BAD_REQUEST)
    if 'content' not in request_body:
        return Response(NO_CONTENT_IN_REQUEST_BODY, status=BAD_REQUEST)
    
    uid = request_body['uid']
    content = request_body['content']

    existing_entry = ff.get(key)

    if existing_entry:
        if existing_entry.uid != uid:
            return Response(NO_ACCESS_TO_ENTRY % key, status=BAD_REQUEST)
        else:
            existing_entry.content = content
            ff.put(key, existing_entry)
            return Response(PUT_SUCCESS, status=OK)

    if len(ff.items()) >= ff._FileFolder__cap:
        return Response(NO_SPACE_IN_FILE_FOLDER, status=BAD_REQUEST)

    new_entry = Entry(uid, content)
    ff.put(key, new_entry)
    return Response(PUT_SUCCESS, status=OK)


@api.route("/<key>", methods=["DELETE"])
def remove(key):
    """
    Remove the file-content associated with the given key owned by the user.
    If there is no user-id `uid` given in the request body or the user-id does not match, return error message and status.
    Otherwise, return the removed file-content and success status
    """
    request_body = request.json
    ff = current_app.ff

    if 'uid' not in request_body:
        return Response(NO_UID_IN_REEQUEST_BODY, status=BAD_REQUEST)

    uid = request_body['uid']
    entry = ff.get(key)

    if entry is None:
        return Response(KEY_DOES_NOT_EXIST % "test_key", status=NOT_FOUND)

    if entry.uid != uid:
        return Response(NO_ACCESS_TO_ENTRY % "test_key", status=BAD_REQUEST)
    
    removed_entry = ff.remove(key)
    return Response(removed_entry.content, status=OK)


@api.route("/", methods=["GET"])
def list():
    """
    List all (key, file-content) tuples owned by the user.
    If there is no user-id `uid` given in the request body, return error message and status.
    Otherwise, return the list of file-content and success status.
    """
    request_body = request.json
    ff = current_app.ff

    if 'uid' not in request_body:
        return Response(NO_UID_IN_REEQUEST_BODY, status=BAD_REQUEST)
    uid = request_body['uid']

    user_entries = []
    for key, entry in ff.items():
        if entry.uid == uid:
            user_entries.append("test_key:test_value")
    response_content = ", ".join(user_entries)
    return Response(response_content, status=OK)

####################################################
# TODO end                                         #
####################################################

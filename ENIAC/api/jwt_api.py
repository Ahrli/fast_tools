from sanic_jwt import Initialize,exceptions


# #jwt
# class User:
#
#     def __init__(self, id, username, password):
#         self.user_id = id
#         self.username = username
#         self.password = password
#
#     def __repr__(self):
#         return "User(id='{}')".format(self.user_id)
#
#     def to_dict(self):
#         return {"user_id": self.user_id, "username": self.username}
#
#
# users = [User(1, "user1", "abcxyz"), User(2, "user2", "abcxyz")]
# username_table = {u.username: u for u in users}
# userid_table = {u.user_id: u for u in users}
#
async def authenticate(request):
    # username_table = {"kxq":"123"}
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username=="loop" and password=="loop":
        return dict(user_id='loop')
    else:
        raise exceptions.AuthenticationFailed("Password is incorrect.")
    # if not username or not password:
    #     raise exceptions.AuthenticationFailed("Missing username or password.")
    # if user is None:
    #     raise exceptions.AuthenticationFailed("User not found.")
    #
    # if password != user.password:
    #     raise exceptions.AuthenticationFailed("Password is incorrect.")
    #
    # return user
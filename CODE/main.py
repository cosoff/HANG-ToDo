from flask import Flask, jsonify, request
from userAPI import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['JSON_AS_ASCII'] = False  # 禁止中文转义
USER_API = User_API()


@app.route("/user/signup", methods=["POST"])
def user_signup():
    # 用户注册
    data = request.get_json()
    userName = data.get("userName")
    password = data.get("password")
    return USER_API.signup(userName, password)


@app.route("/user/login", methods=["POST"])
def user_login():
    # 用户登录
    data = request.get_json()
    userName = data.get("userName")
    password = data.get("password")
    return USER_API.login(userName, password)


@app.route("/user/info", methods=["GET", "POST"])
def user_info():
    # 获取当前用户信息
    token = request.get_json().get("token")
    return USER_API.info(token)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

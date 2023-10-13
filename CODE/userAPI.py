import json
import time
import random
from flask import Flask, jsonify, request


def json_save(dict_data, file_name):
    with open(file_name, 'w') as f:
        json.dump(dict_data, f, indent=4)


class User_API:
    def __init__(self):
        # 载入数据
        self.user_login_data = json.loads(open('./data/user.json', 'r').read())
        self.token_data = json.loads(open('./data/token.json', 'r').read())
        # 清理过期token
        for it in list(self.token_data.keys()):
            if time.time() - self.token_data[it]['time'] > 60 * 60 * 24:
                del self.token_data[it]
        json_save(self.token_data, './data/token.json')

    # 用户注册
    def signup(self, userName, password):
        # 判断用户是否存在
        if userName in self.user_login_data:
            return jsonify({"code": 1, "msg": "用户已存在"})
        else:
            self.user_login_data[userName] = {
                "password": password,
                "id": len(self.user_login_data) + 1,
                "Name": userName,
                "userType": 1
            }
            json_save(self.user_login_data, './data/user.json')
            return jsonify({"code": 0, "msg": "注册成功"})

    def login(self, userName, password):
        # 判断用户是否存在
        if type(userName) != str or type(password) != str:
            return jsonify({"code": -2, "msg": "数据格式异常"})
        if userName == "" or password == "":
            return jsonify({"code": -2, "msg": "数据为空"})
        if userName in self.user_login_data:
            # 判断密码是否正确
            if password == self.user_login_data[userName].get("password"):
                # 登陆成功, 生成token
                token = random.randint(0, 10 ** 16)
                self.token_data[token] = {
                    "time": time.time(),  # token时间
                    "id": self.user_login_data[userName].get("id"),
                    "userName": userName,
                }
                json_save(self.token_data, './data/token.json')
                return jsonify({
                    "code": 0,
                    "data": {
                        "id": self.token_data[token].get("id"),
                        "token": token
                    },
                    "msg": "登录成功"
                })
            else:
                # 登录失败
                return jsonify({"code": 1, "msg": "用户名或密码错误"})
        else:
            # 登录失败
            return jsonify({"code": -1, "msg": "用户不存在"})

    def info(self, token):
        if token in self.token_data:
            return jsonify({
                "code": 0,
                "data": {
                    "id": self.token_data[token].get("id"),
                    "userName": self.token_data[token].get("userName"),
                    "Name": self.user_login_data[self.token_data[token].get("userName")].get("Name"),
                    "userType": self.user_login_data[self.token_data[token].get("userName")].get("userType"),
                }
            })
        else:
            return jsonify({
                "code": 999999,
                "msg": "token不存在或已过期"
            })

    def data(self, token):
        if token in self.token_data:
            id = self.token_data[token].get("id")
        else:
            return jsonify({
                "code": 999999,
                "msg": "token不存在或已过期"
            })

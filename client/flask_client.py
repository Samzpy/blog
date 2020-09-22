# -*- coding:utf-8 -*-
 ######################################################
#        > File Name: flask_client.py
#      > Author: GuoXiaoNao
 #     > Mail: 250919354@qq.com 
 #     > Created Time: Mon 20 May 2019 11:52:00 AM CST
 ######################################################

from flask import Flask, send_file

app = Flask(__name__)
#127.0.0.1:5000/index  u
@app.route('/index')
def index():
    #首页
    return send_file('templates/index.html')
#127.0.0.1:5000/login  u
@app.route('/login')
def login(): 
    #登录
    return send_file('templates/login.html')
#127.0.0.1:5000/register  u
@app.route('/register')
def register():
    #注册
    return send_file('templates/register.html')
#127.0.0.1:5000/sam/info u
@app.route('/<username>/info')
def info(username):
    #个人信息
    return send_file('templates/about.html')
#127.0.0.1:5000/sam/change_info u
@app.route('/<username>/change_info')
def change_info(username):
    #修改个人信息
    return send_file('templates/change_info.html')

#u
@app.route('/<username>/topic/release')
def topic_release(username):
    #发表博客
    return send_file('templates/release.html')

#u
@app.route('/<username>/topics')
def topics(username):
    #个人博客列表
    return send_file('templates/list.html')
#u
@app.route('/<username>/topics/detail/<t_id>')
def topics_detail(username, t_id):
    #博客内容详情
    return send_file('templates/detail.html')

@app.route('/<username>/content/detail/<t_id>')
# http://127.0.0.1:5000/qq/content/detail/7
def content(username,t_id):
    #博客内容详情
    return send_file('templates/content.html')

@app.route('/<username>/topics/modify/<t_id>')
#http://127.0.0.1:5000/qqqqqq/topics/modify/18
def modify(username,t_id):
    #博客内容详情
    return send_file('templates/modify.html')

if __name__ == '__main__':
    app.run(debug=True)


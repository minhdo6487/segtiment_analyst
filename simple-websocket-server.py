#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError

# tất cả clients đang connect tới server
clients = []

def send_to_all_clients(message):
    """ gửi message tới tất cả các clients """

    global clients

    # những clients vẫn còn giữ kết nối
    alive_clients = []
    
    # duyệt qua các clients
    # giữ lại những client vẫn còn kết nối
    # gửi message tới những client này
    for client in clients:
        if not client.closed:
            alive_clients.append(client)
            client.send(message)

    # cập nhật lại danh sách clients còn giữ kết nối
    clients = alive_clients


def request_handle(env, response):
    """ xử lý yêu cầu từ websocket client """

    # websocket được chứa trong env (làm một dict)
    # với key là 'wsgi.websocket'
    websocket = env['wsgi.websocket']

    # lưu client mới kết nối này vào danh sách clients
    clients
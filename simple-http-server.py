#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent.pywsgi import WSGIServer

def request_handle(env, response):
    """ xử lý HTTP request từ người dùng/web browser """

    # chuẩn bị thông điệp 200 gửi lại trang HTML cho người dùng
    response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    
    # nội dung của trang HTML (tạo UI và javascript tạo websocket)
    yield """
        <!doctype html>
        <html>
        <head>
            <title>Websocket chatroom đơn giản</title>
            <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
            <script type="text/javascript">

                var random_color = function() {
                    return "#" + (0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
                };

                $(function() {
                    
                    var user = '<span style="color:' + random_color() + '">' + prompt("Bạn tên là gì?", "pythonvietnam") + '</span>';

                    var websocket = new WebSocket("ws://localhost:8000/");

                    websocket.onmessage = function(e) {
                        $("body").append("<p>" + e.data + "</p>");
                    };

                    websocket.onopen = function(e) {
                        $("#status").html(user + ": Connected");
                    };

                    var send = function() {
                        var message = $("input[name=message]").val();
                        if (message != "") {
                            websocket.send(user + ": " + message);
                        }
                        $("input[name=message]").val("");
                    };

                    $("input[name=message]").keydown(function(e) {
                        if (e.which == 13) {
                            e.preventDefault();
                            send();
                        }
                    });

                    $("#send-btn").click(function() {
                        send();
                    });

                });
            </script>
        </head>
        <body>
            <h1>PythonVietnam Chatroom</h1>
            <p id="status"></p>
            <input type="text" name="message" /><button id="send-btn">Gửi</button>
        </body>
        </html>
    """

if __name__ == '__main__':
    # bắt đầu lắng nghe tại cổng 8080
    WSGIServer(('', 8000), request_handle).serve_forever()
from tornado.options import options, define, parse_command_line
from tornado.web import RequestHandler, Application, removeslash, UIModule, asynchronous
from tornado.gen import coroutine, Task, engine
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient

# other libraries
import os
import json

define("port", default=8000,
       help='run on the given port',
       type=int)


class ApiHandler(RequestHandler):

    @asynchronous
    @engine
    def get(self):
        client = AsyncHTTPClient()
        response = yield Task(client.fetch,"https://radiant-harbor-42641.herokuapp.com/leaderboard")
        body = json.loads(response.body)

        if body["status"] == 200:
            leaderboard = body["payload"]
            users_key = sorted(leaderboard,key=lambda p:leaderboard[p])
            users = []
            for members in users_key:
                users.append([members,leaderboard[members]])
            self.render('leaderboard.html',users=users)
        else:
            self.write_error(666)
        self.finish()

    def write_error(self, status_code, **kwargs):
        self.write("sorry! crow error "+str(status_code))

settings = dict(
    debug=True
)

app = Application(
    handlers=[(r'/', ApiHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    **settings)

if __name__ == "__main__":
    parse_command_line()
    HTTPServer(app).listen(options.port)
    IOLoop.current().start()

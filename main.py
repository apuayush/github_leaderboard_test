from tornado.options import options,define,parse_command_line
import tornado.web
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import json
import os.path
define("port",default=9999,help='run on the given port',type=int)

#call the database

class Module_handler(tornado.web.UIModule):
    def render(self):
        return self.render_string("module1.html",list_elements=list_elements)

class MainHandler(tornado.web.RequestHandler):
    @coroutine
    @tornado.web.removeslash
    def get(self):
        members_list=requests.get('https://api.github.com/orgs/GDGVIT/members').json()
        for members in members_list:
            score=member['login']
            #update the score of the people who have logged in on the database
        new_array=sorted(member_list,key=lambda p:score(p[2])[::-1]
        self.render('index.html',new_array=new_array)

if __name__=="__main__":
    parse_command_line()
    app=tornado.web.Application(handlers=[(r'/leaderboard',MainHandler)],
                                template_path=os.path.join(os.path.dirname(__file__),'template'),
                                static_path=os.path.join(os.path.dirname(__file__),"static"),
                                ui_modules={"list":Module_handler},
                                debug=True)
    HTTPServer(app).listen(options.port)
    IOLoop.instance().start()

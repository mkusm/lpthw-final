# -*- coding:utf-8 -*-

import web
import sqlite3
from gothonweb import map
from web import form


urls = (
    '/game', 'GameEngine',
    '/', 'Index',
    '/login', 'Login',
    '/signup', 'SignUp',
)

app = web.application(urls, globals())

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store, initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout")

login_form = form.Form(
    form.Textbox('username'),
    form.Password('password'),
    form.Button('Login'),
)

signup_form = form.Form(
    form.Textbox('username', description="Username"),
    form.Password('password', description="Password"),
    form.Password('repeat_password', description="Repeat Password"),
    form.Button("Sign Up", type="submit"),
    validators = [form.Validator("Passwords didn't match.",
                                 lambda i: i.password == i.repeat_password)]
)

#def signup():
#    conn = sqlite3.connect('users.db')
#    c = conn.cursor()
#    if c.execute
#    c.execute("""
#    CREATE TABLE user (
#        user_id         INT NOT NULL AUTO_INCREMENT PRIMARY_KEY,
#        user_login      VARCHAR(64) NOT NULL,
#        user_password   VARCHAR(255) NOT NULL,
#        user_status     VARCHAR(16) NOT NULL DEFAULT 'active',
#        user_map        TEXT
#    """)

#def form_test():
#    pass
#
#class Test(object):
#    def GET(self):
#        pass
#        #return

class Index(object):

    def GET(self):
        # this is used to "setup" the session with starting values
        session.room = map.START
        web.seeother("/game")


class Login(object):

    def GET(self):
        login_form_temp = login_form()
        return render.login_page(form=login_form_temp)

    def POST(self):
        login_form_temp = login_form()
        return login_form_temp.password


class SignUp(object):

    def GET(self):
        signup_form_temp = signup_form()
        return render.signup_page(signup_form_temp)

    def POST(self):
        signup_form_temp = signup_form()
        if not signup_form_temp.validates():
            return render.signup_page(signup_form_temp)
        else:
            web.seeother("/login")


class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)
        else:
            return render.you_died()

    def POST(self):
        form = web.input(action=None)

        # there is a bug here, can you fix it?
        if session.room and form.action:
            session.room = session.room.go(form.action)

        web.seeother("/game")

if __name__ == "__main__":
    app.run()

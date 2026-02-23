import argparse

from flask import Flask, render_template, make_response, send_file
from werkzeug.exceptions import HTTPException
import numpy as np
from werkzeug.middleware.proxy_fix import ProxyFix

ERR = [
    {"code": 400,"text": ["Bad request!"]},
    {"code": 403,"text": ["You have been blocked!"]},
    {"code": 404,"text": ["Page not found!"]},
    {"code": 411,"text": ["Length required!"]},
    {"code": 413,"text": ["Too large!"]},
    {"code": 418,"text": ["I'm a teapot!"]},
    {"code": 500,"text": ["An internal error has occured!"]},
    {"code": 501,"text": ["This page has not been implemented!"]},
    {"code": 507,"text": ["The server has not found sufficient storage for your request!"]}
]

app = Flask(__name__)

@app.route('/')
def route_index():
    return render_template('index.html')

@app.route('/style')
@app.route('/style.css')
def route_style():
    return send_file('style.css')

@app.route('/about')
@app.route('/about.html')
def route_about():
    return render_template('about.html')

@app.route('/sitemap.xml')
def route_sitemap():
    return send_file('robots/sitemap.xml')

@app.route('/sitemap-index.xml')
def route_sitemap_index():
    return send_file('robots/sitemap-index.xml')

@app.route('/robots.txt')
def route_robots():
    return send_file('robots/robots.txt')

@app.errorhandler(HTTPException)
def route_exception(e):
    a = [a for a in ERR if a['code'] == e.code]
    msg = a[0]['text'] if a else ["An Error has occurred!"]
    return make_response(render_template(
        'error.html',
        code=e.code,
        msg=np.random.choice(msg, p=np.arange(len(msg), 0, -1)/np.arange(len(msg), 0, -1).sum())
    ), e.code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--Debug", action="store_true", help="Activate debug mode")
    args = parser.parse_args()
    # set proper wsgi for app if not debug
    if not args.Debug:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    app.run(port=5000, debut=args.Debug)
from flask import Flask, request, url_for, redirect, json, Response, jsonify
from flask_sqlalchemy  import SQLAlchemy
from flask.helpers import flash
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user
from models import *


app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'


login_manager = LoginManager(app)



@app.route('/create-news', methods = ['POST'])
def create_article():
    values = request.json
    disc = values['disc']
    theme = values['theme']
    text = values['text'] 
    if values['author']:
        article = Article(disc = disc, theme = theme, text = text, user_name = values['author'])
    else :
        article = Article(disc = disc, theme = theme, text = text)
    try:
         db.session.add(article)
         db.session.commit()
    except:
        response = Response(json.dumps({'success':False}), status=502)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response 
    last_sample = Article.query.filter_by(disc=disc, theme=theme, text=text).first()
    response = Response(json.dumps({'success':True,'last_news_id':last_sample.id, 'last_news_date':last_sample.date}), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response 


@app.route('/get-news', methods = ['GET'])
def get_news():
    start_id = int(request.args.get('start_id', None))
    end_id = int(request.args.get('end_id', None))
    atricle = Article.query.order_by(Article.id.desc()).offset(start_id).limit(end_id+1 - start_id).all()
    out = db_sample_to_json(atricle)
    response = Response(json.dumps(out), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/get-news-by-tag', methods = ['GET'])
def get_news_tag():
    start_id = int(request.args.get('start_id', None))
    end_id = int(request.args.get('end_id', None))
    username = str(request.args.get('username', None))
    atricle = Article.query.filter_by(user_name = username).offset(start_id).limit(end_id+1 - start_id).all()
    out = db_sample_to_json(atricle)
    response = Response(json.dumps(out), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/get-new', methods = ['GET'])
def get_new():
    article_id = int(request.args.get('newsId', None))
    atricle = Article.query.get(article_id)
    out = db_sample_to_json_text(atricle)
    response = Response(json.dumps(out), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/registration', methods = ['POST', 'GET'])
def reg():
    try:
        user = User(username = request.json['login'])
        user.set_password(password = request.json['password'])
    except:
        out = {'resultCode': 0}
        response = Response(json.dumps(out), status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        db.session.add(user)
        db.session.commit()
    except:
        out = {'resultCode': 0}
        response = Response(json.dumps(out), status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    out = {'resultCode': 1}
    response = Response(json.dumps(out), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.set_cookie('foo', 'bar', max_age=60*60*24*365*2, domain='127.0.0.1:3000')
    return response



@app.route('/login', methods = ['POST', 'GET'])
def login():
    user = db.session.query(User).filter(User.username == request.json['login']).first()
    if user and user.check_password(request.json['password']):
        # login_user(user, remember=request.json['remember'])
        out = {'resultCode': 1, 'id': user.id, 'login': user.username}
        response = Response(json.dumps(out), status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        # response.set_cookie('foo', 'bar', max_age=60*60*24*365*2, domain='127.0.0.1:3000')
        return response

    out = {'resultCode': 0}
    response = Response(json.dumps(out), status=200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    return response


def db_sample_to_json(data_sample_list):
    out_json = []
    for sample in data_sample_list:
        out_json.append(
            {
                'id': sample.id,
                'disc': sample.disc,
                'theme': sample.theme,
                # 'text': sample.text,
                'date':sample.date,
                'username': sample.user_name 
            }
        )
    return out_json

def db_sample_to_json_text(sample):
    out_json = []
    
    out_json.append(
        {
            'id': sample.id,
            'disc': sample.disc,
            'theme': sample.theme,
            'text': sample.text,
            'date':sample.date,
            'username': sample.user_name 
        }
    )
    return out_json

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)#debugging
    
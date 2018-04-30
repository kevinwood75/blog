from flask import Flask, render_template, session
from flask import request
from app.models.baseball import Baseball
from app.models.blog import Blog
from app.models.roster import Roster
from app.models.util import check_null

from app.common.database import Database
from app.models.user import User

app = Flask(__name__)
app.secret_key = "woodez"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('resgister.html')

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        data = User.get_by_email(email)
        return render_template("profile.html", email=session['email'], player=data.player, age=data.age, sport=data.sport, team=data.team)
    else:
        session['email'] = None
        return render_template("login.html", email=session['email'])


@app.route('/auth/register', methods=['GET', 'POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    player = request.form['player']
    age = request.form['age']
    sport = request.form.get('sport')
    team = request.form['team']
    User.register(email, password, player, age, sport, team)
    return render_template("profile.html", email=session['email'], player=player, age=age, sport=sport, team=team)


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/roster/add', methods=['POST'])
def add_player():
    data = request.json
    existing_id = Roster.get_by_number(data['number'])
    if existing_id is not None:
       data.update({"_id": existing_id['_id']})
       Roster.input(**data)
    else:
       Roster.input(**data)


@app.route('/stats')
def stats_template():
    user_id = session.get('email')
    if user_id is not None:
        return render_template('gamedayinput.html')
    else:
        return render_template('login.html')


@app.route('/input/stats', methods=['POST'])
def stats_input():
    email = session.get('email')
    if email is not None:
        date = request.form['when']
        hits = check_null(request.form['hits'])
        ab = check_null(request.form['ab'])
        runs = check_null(request.form['runs'])
        second = check_null(request.form['2b'])
        third = check_null(request.form['3b'])
        hr = check_null(request.form['hr'])
        rbi = check_null(request.form['rbi'])
        so = check_null(request.form['so'])
        if Baseball.get_by_user(date, email) is None :
            Baseball.input(email, date, hits, ab, runs, second, third, hr, rbi, so)
            return render_template("statsinput.html", email=session['email'], date=date, hits=hits, ab=ab, runs=runs, second=second, third=third, hr=hr, rbi=rbi, so=so)
        else:
            return render_template("gamedayinput.html")
    else:
        return render_template('login.html')


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html', posts=posts, blog_title=blog.title)

if __name__ == '__main__':
    app.run(port=4000, debug=True)
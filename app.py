import flask
import flask_login
from config import Config
import datetime
import bcrypt
import ssl
from model.model import User, UserProfiles, UserRoles, Roles, Permissions, db, Session
from model.google import init_google_oauth

# SSL 검증 비활성화
if getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

app = flask.Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 초기화
db.init_app(app)

# 로그인 매니저 초기화
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# 구글 로그인 설정
google = init_google_oauth(
    app.config.get('GOOGLE_OAUTH2_CLIENT_ID'),
    app.config.get('GOOGLE_OAUTH2_CLIENT_SECRET')
)

@login_manager.user_loader
def load_user(id):
    session = Session()
    user = session.query(User).filter_by(ID=id).first()
    session.close()
    return user

#-------------------------------------------------로그인 관련-------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        id = flask.request.form.get("id")
        password = flask.request.form.get("password")

        user = User.query.filter_by(ID=id).first()

        if user:
            # 데이터베이스에 저장된 해시된 비밀번호와 입력된 비밀번호 비교
            if bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
                flask_login.login_user(user)
                return flask.redirect(flask.url_for("home"))
            else:
                flask.flash('Login failed. Please check your username and password.', 'error')
                return flask.redirect(flask.url_for('login'))
        else:
            flask.flash('Login failed. Please check your username and password.', 'error')
            return flask.redirect(flask.url_for('login'))

    return flask.render_template('login.html')

@app.route("/google/login")
def google_login():
    return google.authorize(callback=flask.url_for('google_callback', _external=True))

# 구글 OAuth 콜백 처리
@app.route('/google/callback')
def google_callback():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s' % (
            flask.request.args['error_reason'],
            flask.request.args['error_description']
        )
    flask.session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo').data

    email = user_info['email']
    name = user_info.get('name', '')

    session = Session()
    user = session.query(User).filter_by(Email=email).first()

    if user is None:
        new_user = User(
            ID=email,  
            Username=name,
            Password='', 
            Email=email,
            Phone='',
            DateOfBirth=None,
            DateJoined=datetime.datetime.now(),
            Status='active'
        )
        session.add(new_user)
        session.commit()

        new_user_profile = UserProfiles(
            UserID=new_user.UserID,
            ID=email,
            Username=name,
            FirstName='새로운',
            LastName='뉴비',
            Address=''
        )
        session.add(new_user_profile)
        session.commit()

        default_role = session.query(Roles).filter_by(RoleName='Basic User').first()
        default_permission = session.query(Permissions).filter_by(PermissionName='User').first()

        new_user_role = UserRoles(
            UserID=new_user.UserID,
            RoleID=default_role.RoleID,
            PermissionID=default_permission.PermissionID
        )
        session.add(new_user_role)
        session.commit()

        user = new_user

    session.close()
    flask_login.login_user(user)
    return flask.redirect(flask.url_for('home'))

@google.tokengetter
def get_google_oauth_token():
    return flask.session.get('google_token')

# 회원가입
@app.route('/register', methods=['POST'])
def register():
    name = flask.request.form.get('name')
    join_id = flask.request.form.get('join_id')
    join_pwd = flask.request.form.get('join_pwd')
    birth = flask.request.form.get('birth')
    phone = flask.request.form.get('phone')
    email = flask.request.form.get('email')
    address = flask.request.form.get('address')
    address2 = flask.request.form.get('address2')
    address3 = flask.request.form.get('address3')

    # 비밀번호 암호화
    hashed_pwd = bcrypt.hashpw(join_pwd.encode('utf-8'), bcrypt.gensalt())
    full_address = f"{address}, {address2}, {address3}"
    
    session = Session()
    
    # 데이터베이스 저장
    new_user = User(
        ID=join_id,
        Username=name,
        Password=hashed_pwd,
        Email=email,
        Phone=phone,
        DateOfBirth=birth,
        DateJoined= datetime.datetime.now(),
        Status='active'
    )
    session.add(new_user)
    session.commit()

    new_user_profile = UserProfiles(
        UserID=new_user.UserID, 
        ID=join_id, 
        Username=name,
        FirstName="새로운",
        LastName="뉴비",
        Address=full_address
    )
    db.session.add(new_user_profile)
    db.session.commit()

    default_role = session.query(Roles).filter_by(RoleName='Basic User').first()
    default_permission = session.query(Permissions).filter_by(PermissionName='User').first()

    new_user_role = UserRoles(
        UserID=new_user.UserID,
        RoleID=default_role.RoleID,
        PermissionID=default_permission.PermissionID
    )
    session.add(new_user_role)
    session.commit()
    session.close()

    flask.flash('Account created successfully!', 'success')
    return flask.redirect(flask.url_for('login'))

# 개인정보 동의 문서 읽어오기
@app.route('/get_terms_of_use')
def get_terms_of_use():
    with open('TermsofUse/TermsofUse.txt', 'r', encoding='utf-8') as file:
        terms_of_use = file.read()
    return terms_of_use
@app.route('/get_personal_information')
def get_personal_information():
    with open('TermsofUse/PersonalInformation.txt', 'r', encoding='utf-8') as file:
        personal_information = file.read()
    return personal_information

#로그아웃
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"

#아이디 중복 확인
@app.route('/check_id', methods=['GET'])
def check_id():
    join_id = flask.request.args.get('join_id')
    user = User.query.filter_by(ID=join_id).first()
    return flask.jsonify({'exists': user is not None})

@app.context_processor
def inject_flask_login():
    return dict(flask_login=flask_login)
#-----------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    if flask_login.current_user.is_authenticated:
        return flask.render_template('home.html')
    else:
        return flask.redirect(flask.url_for('login'))

@app.route('/account')
def account():
    return flask.render_template('account.html')

@app.route('/error')
def error():
    return flask.render_template('error.html')

@app.route('/donotdisturb')
def donotdisturb():
    return flask.render_template('donotdisturb.html')

@app.route('/introdeveloper')
def introdeveloper():
    return flask.render_template('introdeveloper.html')

@app.route('/introservice')
def introservice():
    return flask.render_template('introservice.html')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

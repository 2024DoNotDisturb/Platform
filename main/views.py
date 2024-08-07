from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
import base64

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    if current_user.is_authenticated:
        user_profile = current_user.user_profile[0]
        profile_picture = user_profile.ProfilePicture
        encoded_profile_picture = None
        if profile_picture:
            encoded_profile_picture = base64.b64encode(profile_picture).decode('utf-8')

        return render_template('home.html', encoded_profile_picture=encoded_profile_picture)
    else:
        return redirect(url_for('auth.login'))

@views_bp.route('/account')
def account():
    if current_user.is_authenticated:
        user_profile = current_user.user_profile[0]
        profile_picture = user_profile.ProfilePicture
        encoded_profile_picture = None
        if profile_picture:
            encoded_profile_picture = base64.b64encode(profile_picture).decode('utf-8')

        return render_template('account.html', encoded_profile_picture=encoded_profile_picture)
    else:
        return redirect(url_for('auth.login'))

@views_bp.route('/error')
def error():
    return render_template('error.html')

@views_bp.route('/donotdisturb')
def donotdisturb():
    return render_template('donotdisturb.html')

@views_bp.route('/introdeveloper')
def introdeveloper():
    return render_template('introdeveloper.html')

@views_bp.route('/introservice')
def introservice():
    return render_template('introservice.html')

@views_bp.route('/Dashboard')
def dashboard_page():
    return render_template('dashboard.html')
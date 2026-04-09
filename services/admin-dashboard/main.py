from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from src.models.authorization_model import AuthorizationORM
from src.models.user_profile_model import UserORM
from src.models.application_model import ApplicationORM
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True

admin = Admin(
    app, 
    name='Blood Donation Admin Dashboard', 
    template_mode='bootstrap3',
    index_view=CustomAdminIndexView()
)

auth_engine = create_engine(
    Config.AUTHORIZATION_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)
auth_session = scoped_session(sessionmaker(bind=auth_engine, autocommit=False, autoflush=False))

user_engine = create_engine(
    Config.USER_PROFILE_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)
user_session = scoped_session(sessionmaker(bind=user_engine, autocommit=False, autoflush=False))


app_engine = create_engine(
    Config.APPLICATION_MANAGEMENT_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)
app_session = scoped_session(sessionmaker(bind=app_engine, autocommit=False, autoflush=False))

class AuthorizationView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 50
    column_list = ['id', 'email', 'name','created_at', 'updated_at']
    column_searchable_list = ['email', 'name']
    column_filters = ['created_at', 'updated_at']
    column_labels = {
        'id': 'ID',
        'email': 'Email',
        'name': 'Name',
        'password_hash': 'Password Hash',
        'created_at': 'Created At',
        'updated_at': 'Updated At'
    }
    form_excluded_columns = ['password_hash']  

class UserProfileView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 50
    column_list = ['id', 'email', 'name', 'phone', 'birth_date', 'blood_type', 'is_verified', 'is_active', 'is_banned', 'total_donations', 'created_at']
    column_searchable_list = ['email', 'name', 'phone']
    column_filters = ['is_verified', 'is_active', 'is_banned', 'blood_type', 'created_at']
    column_labels = {
        'id': 'ID',
        'email': 'Email',
        'name': 'Name',
        'phone': 'Phone',
        'birth_date': 'Birth Date',
        'blood_type': 'Blood Type',
        'is_verified': 'Verified',
        'is_active': 'Active',
        'is_banned': 'Banned',
        'total_donations': 'Total Donations',
        'last_donation_at': 'Last Donation',
        'roles': 'Roles',
        'created_at': 'Created At',
        'updated_at': 'Updated At',
        'password_hash': 'Password Hash'
    }
    form_excluded_columns = ['password_hash']  

class ApplicationView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 50
    column_list = ['id', 'user_id', 'blood_type', 'status', 'application_time', 'application_day', 'location_id', 'created_at']
    column_searchable_list = ['user_id', 'blood_type', 'status', 'location_id']
    column_filters = ['status', 'blood_type', 'application_time', 'created_at']
    column_labels = {
        'id': 'ID',
        'user_id': 'User ID',
        'blood_type': 'Blood Type',
        'application_time': 'Application Time',
        'application_day': 'Application Day',
        'location_id': 'Location ID',
        'status': 'Status',
        'description': 'Description',
        'created_at': 'Created At',
        'updated_at': 'Updated At'
    }


admin.add_view(AuthorizationView(AuthorizationORM, auth_session, name='Authorizations', category='Authorization'))
admin.add_view(UserProfileView(UserORM, user_session, name='User Profiles', category='User Profile'))
admin.add_view(ApplicationView(ApplicationORM, app_session, name='Applications', category='Applications'))

@app.route('/')
def index():
    return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    auth_session.remove()
    user_session.remove()
    app_session.remove()

if __name__ == '__main__':
    print("Starting Admin Dashboard on http://0.0.0.0:5000")
    print("Access admin panel at: http://localhost:5000/admin/")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

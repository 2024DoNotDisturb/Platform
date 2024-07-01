from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum, ForeignKey, Text, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import flask_login
from config import Config

# Flask SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

# 데이터베이스 엔진 생성
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Session 클래스 생성
Session = sessionmaker(bind=engine)

# 유저 테이블
class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    ID = Column(String(255), unique=True, nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Phone = Column(String(20))
    DateOfBirth = Column(Date)
    DateJoined = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    LastLogin = Column(TIMESTAMP)
    Status = Column(Enum('active', 'inactive', 'banned', name='user_status'), default='active')

    # User와 UserProfiles 간의 관계 설정
    user_profile = relationship('UserProfiles', back_populates='user', primaryjoin="User.UserID == UserProfiles.UserID", lazy='joined')

    def get_id(self):
        return self.ID

# 유저 프로필 테이블
class UserProfiles(db.Model):
    __tablename__ = 'UserProfiles'
    UserProfileID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    ID = Column(String(255), nullable=False)  # 외래 키가 아닌 경우에도 nullable=False로 설정
    Username = Column(String(255), nullable=False)  # 외래 키가 아닌 경우에도 nullable=False로 설정
    FirstName = Column(String(255))
    LastName = Column(String(255))
    Address = Column(String(255))
    ProfilePicture = Column(String(255))

    # User와의 관계 설정
    user = relationship('User', back_populates='user_profile', foreign_keys=[UserID, ID, Username], lazy='joined', innerjoin=True)

# AI 서비스 테이블
class AIServices(db.Model):
    __tablename__ = 'AIServices'
    ServiceID = Column(Integer, primary_key=True, autoincrement=True)
    ServiceName = Column(String(255), unique=True, nullable=False)
    Description = Column(Text)
    Endpoint = Column(String(255), nullable=False)

# 유저 서비스 테이블
class UserServices(db.Model):
    __tablename__ = 'UserServices'
    UserServiceID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    ServiceID = Column(Integer, ForeignKey('AIServices.ServiceID'), nullable=False)
    SubscriptionDate = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    Status = Column(Enum('active', 'inactive', 'canceled', name='subscription_status'), default='active')

# 서비스 사용 테이블
class ServiceUsage(db.Model):
    __tablename__ = 'ServiceUsage'
    UsageID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    ServiceID = Column(Integer, ForeignKey('AIServices.ServiceID'), nullable=False)
    UsageDate = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    UsageDetail = Column(Text)
    UsageAmount = Column(Integer)

# 알림 테이블
class Notifications(db.Model):
    __tablename__ = 'Notifications'
    NotificationID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    Message = Column(Text, nullable=False)
    DateSent = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    IsRead = Column(Boolean, default=False)

# 역할 테이블
class Roles(db.Model):
    __tablename__ = 'Roles'
    RoleID = Column(Integer, primary_key=True, autoincrement=True)
    RoleName = Column(String(255), unique=True, nullable=False)

# 권한 테이블
class Permissions(db.Model):
    __tablename__ = 'Permissions'
    PermissionID = Column(Integer, primary_key=True, autoincrement=True)
    PermissionName = Column(String(255), unique=True, nullable=False)

# 유저 역할 테이블
class UserRoles(db.Model):
    __tablename__ = 'UserRoles'
    UserRoleID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    RoleID = Column(Integer, ForeignKey('Roles.RoleID'), nullable=False)
    PermissionID = Column(Integer, ForeignKey('Permissions.PermissionID'), nullable=False)

# 로그 테이블
class Logs(db.Model):
    __tablename__ = 'Logs'
    LogID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'), nullable=False)
    Action = Column(String(255), nullable=False)
    Timestamp = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    Details = Column(Text)

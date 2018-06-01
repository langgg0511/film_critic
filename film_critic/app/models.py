import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 用户对电影评价表
class UsersMoviesEvaluates(db.Model):
    __tablename__ = 'users_movies_evaluates'
    # 用户ID
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 电影ID
    movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    # 用户评分 0,2,4,6,8,10
    evaluate = db.Column('evaluate', db.Integer, default=0)
    # 评分时间
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    #是否为最近评分
    is_this_week = db.Column(db.Boolean, default=True)


# 用户对评论评价表
class UsersCommentsEvaluates(db.Model):
    __tablename__ = 'users_comments_evaluates'
    # 用户ID
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # 评论ID
    comment_id = db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    # 有用
    useful = db.Column('useful', db.Boolean)
    # 无用
    useless = db.Column('useless', db.Boolean)


class Message(db.Model):
    """
    留言板
    """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(), index=True)


# todo 邮箱认证
class User(UserMixin, db.Model):
    """
    用户信息表
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    description = db.Column(db.Text)
    is_administrator = db.Column(db.Boolean, default=False)

    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    # 写过的留言信息
    wrote_messages = db.relationship('Message', foreign_keys=[Message.writer_id],
                                      backref=db.backref('writer', lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')
    # 留言接受信息
    received_messages = db.relationship('Message', foreign_keys=[Message.receiver_id],
                                        backref=db.backref('receiver', lazy='joined'),
                                        lazy='dynamic',
                                        cascade='all, delete-orphan')

    movies_evaluates = db.relationship('UsersMoviesEvaluates', foreign_keys=[UsersMoviesEvaluates.user_id],
                                       backref=db.backref('user', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')

    comments_evaluates = db.relationship('UsersCommentsEvaluates', foreign_keys=[UsersCommentsEvaluates.user_id],
                                         backref=db.backref('user', lazy='joined'),
                                         lazy='dynamic',
                                         cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError("It's not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(),
                     password=forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def get_new_messages(self):
        return self.received_messages.order_by(Message.timestamp.desc()).limit(5)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), default='')
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


movies_tags = db.Table('movies_tags',
                       db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Movie(db.Model):
    """
    电影信息表
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    # 英文名
    # eg_name = db.Column(db.String(32))
    # 正在热映
    is_playing = db.Column(db.Boolean, default=False)
    actor = db.Column(db.String(128))
    director = db.Column(db.String(32))
    language = db.Column(db.String(16))
    release_year = db.Column(db.Date, index=True)
    # 用户评分 0 <= x <= 10.0
    evaluate = db.Column(db.Float, default=0)
    evaluate_count = db.Column(db.Integer, default=0)
    evaluate_week = db.Column(db.Float, default=0)
    evaluate_count_week = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    country = db.Column(db.String(16))
    # URI
    picture = db.Column(db.String(32))

    # 别名
    other_name = db.Column(db.String(32))
    # 时长
    runtime = db.Column(db.String(16))
    # 编剧
    scriptwriter = db.Column(db.String(32))

    comments = db.relationship('Comment', backref='movie', lazy='dynamic')

    tags = db.relationship('Tag', secondary=movies_tags,
                           backref=db.backref('movies', lazy='dynamic'), lazy='dynamic')

    users_evaluates = db.relationship('UsersMoviesEvaluates', foreign_keys=[UsersMoviesEvaluates.movie_id],
                                       backref=db.backref('movie', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')

    @staticmethod
    def generate_fake(count=100):
        """
        生成虚拟数据 todo
        :param count:
        :return:
        """
        from random import seed, randint
        import forgery_py
        seed()
        movie_count = Movie.query.count()

    def get_evaluates(self):
        return self.evaluate

    def get_tags_name(self):
        """
        获取标签名列表
        :return:
        """
        return list(map(lambda tags: tags.name, self.tags))

    def get_most_useful_comment(self):
        """
        获取最多赞评论
        :return:
        """
        return self.comments.order_by(Comment.useful_count.desc()).first()

    def add_tags_by_name(self, name_list):
        """
        通过标签名添加 Tag
        :param name_list: 标签名列表
        :return:
        """
        self.tags.append(list(map(lambda name: Tag.query.filter_by(name=name).first(), name_list)))


class Tag(db.Model):
    """
    电影类型标签表
    """
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True)


class Comment(db.Model):
    """
    评论表
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), default='')
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    disabled = db.Column(db.Boolean, default=False)
    useful_count = db.Column(db.Integer, default=0)
    useless_count = db.Column(db.Integer, default=0)

    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    users_evaluates = db.relationship('UsersCommentsEvaluates', foreign_keys=[UsersCommentsEvaluates.comment_id],
                                         backref=db.backref('comment', lazy='joined'),
                                         lazy='dynamic',
                                         cascade='all, delete-orphan')


class Feedback(db.Model):
    """
    信息反馈表
    """
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Cancel(db.Model):
    """
    用户注销请求表
    """
    __tablename__ = 'cancels'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

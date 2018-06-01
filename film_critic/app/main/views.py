import datetime
import json
import re

from flask import render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.utils.decorators import admin_required
from . import main
from app.models import (
    Movie,
    Tag,
    User,
    Comment,
    UsersMoviesEvaluates,
    UsersCommentsEvaluates,
    Message,
)

from .forms import WriteComment


@main.route("/")
def index():
    """
    主页
    :return:
    """
    tags = Tag.query.all()

    # 热映电影
    playing_movies = Movie.query.filter_by(is_playing=True).all()
    playing_slide_index_max = int(len(playing_movies) / 6) + 1
    per_page_playing_movies = []
    for i in range(0, playing_slide_index_max):
        per_page_playing_movies.append(playing_movies[i * 5: i * 5 + 5])
    if len(per_page_playing_movies[playing_slide_index_max - 1]) < 5:
        for i in range(
                0, 5 - len(per_page_playing_movies[playing_slide_index_max - 1])
        ):
            per_page_playing_movies[playing_slide_index_max - 1].append("empty")

    # 最近热门电影
    per_page_hot_movies = []
    for i in range(0, 5):
        per_page_hot_movies.append(
            Movie.query.order_by(Movie.release_year.desc()).limit(50)[
            i * 10: i * 10 + 10
            ]
        )
    # 热门影评
    time_now = datetime.datetime.now()
    hot_reviews = (
        Comment.query.filter(Comment.timestamp >= time_now - datetime.timedelta(days=5))
            .order_by(Comment.useful_count.desc())
            .limit(5)
    )
    # 本周口碑榜
    week_evaluate = UsersMoviesEvaluates.query.filter(
        (UsersMoviesEvaluates.timestamp < time_now - datetime.timedelta(days=5))
        & (UsersMoviesEvaluates.timestamp >= time_now - datetime.timedelta(days=6))
    ).all()
    if week_evaluate:
        for i in week_evaluate:
            if i.is_this_week is True:
                movie = Movie.query.filter_by(id=i.movie_id).first()
                movie.evaluate_week = (
                                          float(movie.evaluate_week) * movie.evaluate_count_week
                                          - float(i.evaluate)
                                      ) / float(movie.evaluate_count_week - 1)
                movie.evaluate_count_week = movie.evaluate_count_week - 1
                db.session.add(movie)
                db.session.commit()
                i.is_this_week = False
                db.session.add(i)
                db.session.commit()
    hot_movie = Movie.query.filter().order_by(Movie.evaluate_week.desc()).limit(10)
    num_list = range(0, 10)
    return render_template(
        "index.html",
        tags=tags,
        playing_slide_index_max=playing_slide_index_max,
        per_page_playing_movies=per_page_playing_movies,
        per_page_hot_movies=per_page_hot_movies,
        hot_reviews=hot_reviews,
        hot_movie=hot_movie,
        num_list=num_list,
    )


@main.route("/users/<username>")
@login_required
def user_info(username):
    """
    用户信息页
    :param username:
    :return:
    """
    # 查询用户
    user = User.query.filter_by(username=username).first_or_404()
    user_comments = user.comments.limit(5)
    user_received_messages = user.received_messages.order_by(
        Message.timestamp.desc()
    ).limit(10)
    return render_template(
        "user_info.html",
        user_comments=user_comments,
        user=user,
        user_received_messages=user_received_messages,
    )


@main.route("/users/<username>", methods=["POST", "GET"])
@login_required
def post_message(username):
    """
    提交留言
    :param username:
    :return:
    """
    message_text = request.values.get("message_text", "", str)
    receiver = User.query.filter_by(username=username).first()
    if message_text != "":
        db.session.add(
            Message(writer=current_user, receiver=receiver, body=message_text)
        )
        db.session.commit()
    print("ddebug")

    # 提交签名
    user_description = request.values.get("user_description", "", str)
    if user_description and username == current_user.username:
        current_user.description = user_description
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for("main.user_info", username=username))


@main.route("/users/<username>/message", methods=["POST", "GET"])
@login_required
def all_message(username):
    """
    用户所有留言
    :param username:
    :return:
    """
    if username == current_user.username:
        pass
        user = User.query.filter_by(username=username).first()
        received_messages = user.received_messages.all()
        return render_template(
            "all_message.html", username=username, received_messages=received_messages
        )
    else:
        return redirect(url_for("main.user_info", username=username))


@main.route("/users/<username>/message/delete/<message_id>", methods=["POST", "GET"])
@login_required
def message_delete(message_id, username):
    if username == current_user.username:
        message = Message.query.filter_by(id=message_id).first()
        db.session.delete(message)
        db.session.commit()
        return redirect(url_for("main.all_message", username=username))
    else:
        return redirect(url_for("main.user_info", username=username))


@main.route("/user_comments/<username>")
@login_required
def user_comments(username):
    """
    显示用户的所有评论
    :param username:
    :return:
    """
    page = request.values.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first()
    pagination = user.comments.paginate(
        page, per_page=current_app.config["COMMENT_PER_PAGE"], error_out=False
    )
    comments = pagination.items
    return render_template(
        "user_comments.html", user=user, pagination=pagination, comments=comments
    )


@main.route("/movies/tag/<tag_name>", methods=["GET"])
def movie_by_tag(tag_name):
    """
    根据tag_name返回分类页
    :param tag_name:
    :return:
    """
    tags = Tag.query.all()

    page = request.args.get("page", 1, type=int)

    sort_id = request.args.get("sort_id", 1, type=int)

    pagination = ""

    if not sort_id or sort_id == 1:
        # 根据tag_name(标签)分页查询 按热门程度
        pagination = (
            Tag.query.filter_by(name=tag_name)
                .first()
                .movies.order_by(Movie.evaluate_count.desc())
                .paginate(
                page, per_page=current_app.config["MOVIES_PER_PAGE"], error_out=False
            )
        )
    elif sort_id == 2:
        # 按时间
        pagination = (
            Tag.query.filter_by(name=tag_name)
                .first()
                .movies.order_by(Movie.release_year.desc())
                .paginate(
                page, per_page=current_app.config["MOVIES_PER_PAGE"], error_out=False
            )
        )
    else:
        # 按评价
        pagination = (
            Tag.query.filter_by(name=tag_name)
                .first()
                .movies.order_by(Movie.evaluate.desc())
                .paginate(
                page, per_page=current_app.config["MOVIES_PER_PAGE"], error_out=False
            )
        )
    # 某一类的电影列表
    movies = pagination.items
    return render_template(
        "movies_list_by_tag.html",
        tags=tags,
        tag_name=tag_name,
        movies=movies,
        pagination=pagination,
        tab_index=sort_id,
    )


@main.route("/images/<name>", methods=["GET", "POST"])
def images_server(name):
    """
    图片上传下载
    :param name:
    :return:
    """
    pass


@main.route("/movies/id/<int:movie_id>", methods=["GET", "POST"])
def movie_by_id(movie_id):
    """
    电影信息页
    :param movie_id:
    :return:
    """
    # 查询电影

    movie = Movie.query.get(int(movie_id))
    page = request.args.get("page", 1, type=int)
    # 评论分页
    comment_pagination = Comment.query.filter_by(movie_id=movie_id).paginate(
        page, per_page=current_app.config["COMMENT_PER_PAGE"], error_out=False
    )
    comments = comment_pagination.items
    # 电影类型
    tag = ""
    tag_list = movie.tags.all()
    for i in range(0, len(tag_list)):
        tags = Tag.query.get(tag_list[i].id).name
        if i == 0 or i == len(tag_list):
            tag = tags
        else:
            tag = tags + "/" + tag
    star = round(movie.evaluate / 2)
    # 点击事件--添加评论
    form = WriteComment()
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
    else:
        user = ""
    if form.validate_on_submit():
        comment = Comment(
            body=form.content.data,
            timestamp=datetime.datetime.now(),
            movie_id=movie_id,
            writer_id=user.id,
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("main.movie_by_id", movie_id=movie_id))
    return render_template(
        "movies.html",
        movie=movie,
        comment_pagination=comment_pagination,
        comments=comments,
        tag=tag,
        star=star,
        form=form,
        user=user,
    )


@main.route("/movie_evaluate/movie_id", methods=["GET"])
def users_movies_evaluate():
    """
    评分响应
    :return:
    """
    movie_id_web = request.args.get("movie_id", "")
    pattern = re.compile(r"\d+")
    movie_id = pattern.findall(movie_id_web)
    evaluate = request.args.get("evaluate", "")
    # user_id = request.args.get("user_id", "")
    # 判断是否登录账户
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        movie_evaluate = UsersMoviesEvaluates.query.filter_by(
            user_id=int(user.id), movie_id=int(movie_id[0])
        ).count()
        # 判断是否评分
        if movie_evaluate == 1:
            data = dict(ok=0)
            return json.dumps(data)
        # 添加评分信息
        if movie_evaluate == 0:
            evaluates = UsersMoviesEvaluates(
                user_id=int(user.id), movie_id=int(movie_id[0]), evaluate=int(evaluate)
            )
            movie = Movie.query.filter_by(id=int(movie_id[0])).first()
            # 修改评分
            evaluate_ = (
                            float(movie.evaluate) * movie.evaluate_count + float(evaluate)
                        ) / float(movie.evaluate_count + 1)
            movie.evaluate_count = movie.evaluate_count + 1
            movie.evaluate = round(evaluate_, 1)
            # 修改近期评分
            movie.evaluate_week = (
                                      float(movie.evaluate_week) * movie.evaluate_count_week + float(evaluate)
                                  ) / float(movie.evaluate_count_week + 1)
            movie.evaluate_count_week = movie.evaluate_count_week + 1

            db.session.add(movie)
            db.session.commit()
            db.session.add(evaluates)
            db.session.commit()
            data = dict(ok=1)
            return json.dumps(data)
    else:
        data = dict(ok=2)
    return json.dumps(data)


@main.route("/comment_evbaluate", methods=["GET"])
def comment_evaluate():
    """
    评论赞/踩响应
    :return:
    """
    movie_id_web = request.args.get("movie_id", "")
    comment_id_web = request.args.get("comment_id", "")
    useful_useless = request.args.get("useful_useless", "")

    pattern = re.compile(r"\d+")
    movie_id = pattern.findall(movie_id_web)
    comment_id = pattern.findall(comment_id_web)
    # print(movie_id_web,comment_id_web,useful_useless,movie_id,comment_id)

    # 判断是否登录账户
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        uce = UsersCommentsEvaluates.query.filter_by(
            user_id=int(user.id), comment_id=int(comment_id[0])
        )
        count = uce.count()
        uces = uce.first()
        # 判断是否评分
        if count == 1:
            if uces.useful is True:
                data = dict(ok=0)
                return json.dumps(data)
            else:
                data = dict(ok=3)
                return json.dumps(data)
        # 添加评论评分信息
        if count == 0:
            if useful_useless == "useful":
                evaluates = UsersCommentsEvaluates(
                    user_id=int(user.id), comment_id=int(comment_id[0]), useful=True
                )
                comment = Comment.query.filter_by(id=int(comment_id[0])).first()
                comment.useful_count = comment.useful_count + 1
                db.session.add(comment)
                db.session.commit()

                db.session.add(evaluates)
                db.session.commit()
                data = dict(ok=1)
                return json.dumps(data)
            else:
                evaluates = UsersCommentsEvaluates(
                    user_id=int(user.id), comment_id=int(comment_id[0]), useless=True
                )
                comment = Comment.query.filter_by(id=int(comment_id[0])).first()
                comment.useless_count = comment.useless_count + 1
                db.session.add(comment)
                db.session.commit()

                db.session.add(evaluates)
                db.session.commit()
                data = dict(ok=4)
                return json.dumps(data)
    else:
        data = dict(ok=2)
    return json.dumps(data)


# todo 搜索功能
@main.route("/search", methods=["GET", "POST"])
def search():
    page = request.args.get("page", 1, type=int)

    q = request.args.get("q", 1, type=str)

    tags = Tag.query.all()

    pagination = Movie.query.filter(Movie.name.like("%" + q + "%")).paginate(
        page, per_page=current_app.config["MOVIES_PER_PAGE"], error_out=False
    )
    movies = pagination.items
    return render_template(
        "search.html", movies=movies, pagination=pagination, tags=tags
    )

from app import db
from . import admin
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, MovieInfo, ModifyInfo, ModifyInfo2, \
    DeleteInfo, DeleteInfo2, UserInfo, DeleteUser
from app.models import User, Movie, Tag
from app.utils.decorators import admin_required


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    管理员登陆
    :return: 登陆页
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@login_required
@admin_required
def logout():
    """
    用户退出
    :return: 重定向到主页
    """
    logout_user()
    flash('you have been logged out.')
    return redirect(url_for('main.index'))


@admin.route('/movie/add', methods=['GET', 'POST'])
@login_required
@admin_required
def movie_add():
    """
    添加电影信息
    :return:
    """
    form = MovieInfo()
    if form.validate_on_submit():
        tag = Tag.query.filter_by(name=form.tag.data).first()
        tags = Tag.query.get(tag.id)
        movie = Movie(name=form.name.data,
                      actor=form.actor.data,
                      director=form.director.data,
                      language=form.language.data,
                      release_year=form.release_year.data,
                      evaluate=form.evaluate.data,
                      description=form.description.data,
                      country=form.country.data,
                      picture=form.picture.data,
                      tags=[tags]
                      )

        db.session.add(movie)
        db.session.commit()

    return render_template('admin/movie.html', form=form)


@admin.route('/movie/modify', methods=['GET', 'POST'])
@login_required
@admin_required
def movie_modify():
    form = ModifyInfo()
    form2 = ModifyInfo2()
    if form.validate_on_submit():
        movie = Movie.query.filter_by(name=form.find_name.data).first()
        form2.name.data = movie.name
        form2.actor.data = movie.actor
        form2.director.data = movie.director
        form2.language.data = movie.language
        form2.release_year.data = movie.release_year
        form2.evaluate.data = movie.evaluate
        form2.description.data = movie.description
        form2.country.data = movie.country
        form2.picture.data = movie.picture
        movies = Movie.query.get(movie.id)
        tag_list = movies.tags.all()
        # tags = Tag.query.get(tag_list[1].id).name
        tags = ''
        for i in range(0, len(tag_list)):
            tag = Tag.query.get(tag_list[i].id).name
            tags = tag + ' ' + tags
        form2.tag.data = tags

    if form2.validate_on_submit():
        # for i in form2.tag.data:

        movie = Movie.query.filter_by(name=form2.name.data).first()
        movie.name = form2.name.data
        movie.actor = form2.actor.data
        movie.director = form2.director.data
        movie.language = form2.language.data
        movie.release_year = form2.release_year.data
        movie.evaluate = form2.evaluate.data
        movie.description = form2.description.data
        movie.country = form2.country.data
        movie.picture = form2.picture.data
        tag = Tag.query.filter_by(name=(form2.tag.data).strip()).first()
        tags = Tag.query.get(tag.id)
        movie.tags = [tags]

        db.session.add(movie)
        db.session.commit()

    return render_template('admin/modify.html', form=form, form2=form2)


@admin.route('/movie/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def movie_delete():
    form = DeleteInfo()
    form2 = DeleteInfo2()
    if form.validate_on_submit():
        movie = Movie.query.filter_by(name=form.find_name.data).first()
        form2.name.data = movie.name
        form2.actor.data = movie.actor
        form2.director.data = movie.director
        form2.language.data = movie.language
        form2.release_year.data = movie.release_year
        form2.evaluate.data = movie.evaluate
        form2.description.data = movie.description
        form2.country.data = movie.country
        form2.picture.data = movie.picture
        movies = Movie.query.get(movie.id)
        tag_list = movies.tags.all()
        # tags = Tag.query.get(tag_list[1].id).name
        tags = ''
        for i in range(0, len(tag_list)):
            tag = Tag.query.get(tag_list[i].id).name
            tags = tag + ' ' + tags
        form2.tag.data = tags

        if form2.validate_on_submit():
            # for i in form2.tag.data:

            movie = Movie.query.filter_by(name=form2.name.data).first()
            form2.name.data = ''
            form2.actor.data = ''
            form2.director.data = ''
            form2.language.data = ''
            form2.release_year.data = ''
            form2.evaluate.data = ''
            form2.description.data = ''
            form2.country.data = ''
            form2.picture.data = ''
            form2.tag.data = ''

            db.session.delete(movie)
            db.session.commit()

    return render_template('admin/delete.html', form=form, form2=form2)


@admin.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users_info():
    form = UserInfo()
    form2 = DeleteUser()
    user_list = User.query.all()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.find_name.data).first()

    elif form2.validate_on_submit():
        users = User.query.filter_by(username=form2.delete_name.data).first()
        db.session.delete(users)
        db.session.commit()
        user = None
    else:
        user = None
    return render_template('admin/users.html', user_list=user_list, form=form, user=user, form2=form2)

from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return 'В базе данных записей нет.'
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    # Тут подключаем шаблон opinion.html:
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    # Вот тут создаётся новый экземпляр формы:
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь...
        if Opinion.query.filter_by(text=text).first() is not None:
            # ...вызвать функцию flash и передать соответствующее сообщение:
            flash('Такое мнение уже было оставлено ранее!')
            # Вернуть пользователя на страницу «Добавить новое мнение»:
            return render_template('add_opinion.html', form=form)
        # ...то нужно создать новый экземпляр класса Opinion:
        opinion = Opinion(
            # И передать в него данные, полученные из формы:
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        # Затем добавить его в сессию работы с базой данных:
        db.session.add(opinion)
        # И зафиксировать изменения:
        db.session.commit()
        # Затем переадресовать пользователя на страницу добавленного мнения:
        return redirect(url_for('opinion_view', id=opinion.id))
    # Если валидация не пройдена — просто отрисовать страницу с формой:
    # Объект формы передаётся в шаблон add_opinion.html:
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
# Параметром указывается имя переменной:
def opinion_view(id):
    quantity = Opinion.query.count()
    if not quantity:
        # Если в базе пусто, при запросе к главной странице
        # пользователь увидит ошибку 500:
        abort(500)
    offset_value = randrange(quantity)
    # Теперь можно запросить нужный объект по id...
    opinion = Opinion.query.offset(offset_value).first()
    # ...и передать его в шаблон (шаблон тот же, что и для главной страницы):
    return render_template('opinion.html', opinion=opinion)

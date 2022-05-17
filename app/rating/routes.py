import pickle
from ast import literal_eval
from datetime import datetime

from flask import Blueprint , session
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import Rates, Group, Question, Rank,Temp_text
from app.rating.forms import RateForm, Compare2, ChangeText

rating = Blueprint('rating', __name__)


@rating.route('/exp')
@login_required
def exp_page():
    items = [item.number for item in Group.query.filter_by(professor=current_user.professor_name)]

    submited_data = db.session.query(Rates).filter(
        Rates.username == current_user.username).all()
    submited_groups = [int(x.group) for x in submited_data]

    items.sort()
    submited_groups.sort()

    return render_template('exp2.html', items=items, submited_groups=submited_groups)


@rating.route('/grouprate/<groupnum>', methods=['GET', 'POST'])
@login_required
def rate_page(groupnum):
    groups_rated_by_users = Rates.query.filter_by(username=current_user.username).all()
    groups_rated_by_users = [item.group for item in groups_rated_by_users]

    if groupnum in groups_rated_by_users:  # if user inserted rate close page
        return render_template('Access.html')

    form = RateForm()

    if form.validate_on_submit():
        print(form.data)
        username = current_user.username
        ans_q1 = form.q1.data

        rate = int(form.rate.data)

        rate_to_create = Rates(username=username, group=groupnum, q1=ans_q1, rate=rate)

        same_rate = db.session.query(Rates).filter(
            Rates.username == current_user.username).filter(Rates.rate == rate).filter(Rates.group != groupnum).all()

        exs_rank = Rank.query.filter_by(username=current_user.username, date=datetime.today().date()).first()

        # is experiment group or not
        check_exp = Rank.query.filter_by(username=username).filter_by(
            date=datetime.today().date()).first()
        exp = False
        if check_exp:
            if check_exp.experiment_group == 1:
                exp = True

        if same_rate and exp:
            rate_to_create = repr(pickle.dumps(rate_to_create))
            same_rate_groups = [x for x in literal_eval(exs_rank.list_rank) if int(x[1]) == rate]

            try:
                temp_text = Temp_text.query.filter_by(username=current_user.username).first()
                db.session.delete(temp_text)
                db.commit()
            except:
                pass

            temp_data = Temp_text(username=current_user.username, pickle=rate_to_create)
            db.session.add(temp_data)
            db.session.commit()



            return redirect(
                url_for('rating.compare_page', same_rate_groups=repr(same_rate_groups)))
            # return redirect(
            #     url_for('rating.compare_page', rate_to_create=rate_to_create, same_rate_groups=repr(same_rate_groups)))

        flash(f'submited evalutation for group {groupnum}', category='info')

        if exs_rank:
            t = literal_eval(exs_rank.list_rank)  # t-temp list
        else:
            t = []

        flag = True
        if t == []:
            t.append((int(groupnum), rate))
            flag = False

        if flag:
            tcopy = t.copy()
            for index, elem in enumerate(tcopy):
                if int(elem[1]) < rate:
                    t.insert(index, ((int(groupnum), rate)))
                    flag = False
                    break

        if flag:
            t.insert(len(t), (int(groupnum), rate))

        # save changes to db
        if exs_rank:
            exs_rank.list_rank = repr(t)
            db.session.commit()
        else:
            rank = Rank(username=current_user.username, date=datetime.today().date(), list_rank=repr(t))
            db.session.add(rank)
            db.session.commit()

        db.session.add(rate_to_create)
        db.session.commit()

        return redirect(url_for('rating.exp_page'))
    else:
        if form.errors != {}:  # if there are no errors from validations
            for err_msg in form.errors.values():
                flash(f'Error found: {err_msg}', category='danger')

    date = datetime.today().date()
    time = datetime.now().strftime("%H:%M:%S")

    questions = Question.query.filter_by(professor_name=current_user.professor_name).all()
    groupname = Group.query.filter_by(number=groupnum).first().name

    return render_template('groupRate.html', group=groupnum, date=date, time=time, questions=questions, form=form,
                           groupname=groupname)


@rating.route('/compare_page', methods=['GET', 'POST'])
@login_required
def compare_page():
    #rate_to_create = request.args.get('rate_to_create')

    temp_text = Temp_text.query.filter_by(username=current_user.username).first()


    #rate_to_create = session.pop('rate_to_create',None)

    rate_to_create = pickle.loads(literal_eval(temp_text.pickle))
    groupnum = int(rate_to_create.group)
    same_rates = literal_eval(request.args.get('same_rate_groups'))
    form = Compare2()

    exs_rank = Rank.query.filter_by(username=current_user.username, date=datetime.today().date()).first()

    # add to prevent bugs
    rank_list = literal_eval(exs_rank.list_rank)
    if int(rate_to_create.group) in [int(item[0]) for item in rank_list]:
        return render_template('Access.html')

    if same_rates == []:

        rank_list = literal_eval(exs_rank.list_rank)
        index = len(rank_list)  # if not bigger then any element insert to end of list
        for i, item in enumerate(rank_list):

            if int(item[1]) < int(rate_to_create.rate):
                index = i
                break

        rank_list.insert(index, (groupnum, rate_to_create.rate))
        exs_rank.list_rank = repr(rank_list)
        db.session.commit()
        db.session.add(rate_to_create)
        db.session.commit()
        return redirect(url_for('rating.exp_page'))

    if request.method == 'POST' and form.select.data:

        exs_rank.number_questions += 1
        db.session.commit()

        pref = form.select.data
        if int(pref) == int(rate_to_create.group):

            rank_list = literal_eval(exs_rank.list_rank)
            index = None
            for i, item in enumerate(rank_list):

                if item[0] == same_rates[0][0]:
                    index = i
                    break

            rank_list.insert(index, (groupnum, rate_to_create.rate))
            exs_rank.list_rank = repr(rank_list)
            db.session.commit()
            db.session.add(rate_to_create)
            db.session.delete(temp_text)
            db.session.commit()
            return redirect(url_for('rating.exp_page'))
        else:

            same_rates = same_rates[1:]

            rate_to_create = repr(pickle.dumps(rate_to_create))

            # return redirect(
            #     url_for('rating.compare_page', rate_to_create=rate_to_create, same_rate_groups=repr(same_rates)))
            return redirect(
                url_for('rating.compare_page', same_rate_groups=repr(same_rates)))

    for r in same_rates:

        if int(r[1]) == int(rate_to_create.rate):
            compare_group = r[0]
            form.select.choices = [(groupnum), (compare_group)]

            compare_name = Group.query.filter_by(number=compare_group).first().name
            group_name = Group.query.filter_by(number=groupnum).first().name

            return render_template('compare2groups.html', groupnum=groupnum, compare_group=compare_group, form=form,
                                   compare_name=compare_name, group_name=group_name)


@rating.route('/change_text/<groupnum>', methods=['GET', 'POST'])
@login_required
def change_text(groupnum):
    old_rate = Rates.query.filter_by(username=current_user.username).filter_by(group=groupnum).first()

    form = ChangeText()

    if form.validate_on_submit():
        username = current_user.username
        ans_q1 = form.q1.data

        old_rate.q1 = ans_q1




        db.session.commit()
        flash("changes have been saved!", category="info")
        return redirect(url_for('rating.exp_page'))

    form.q1.data = old_rate.q1



    questions = Question.query.filter_by(professor_name=current_user.professor_name).all()
    groupname = Group.query.filter_by(number=groupnum).first().name
    return render_template('change_text.html', group=groupnum, questions=questions, form=form, groupname=groupname)

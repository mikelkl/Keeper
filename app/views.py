# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .models import User, Treatment, ECG
from datetime import datetime
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 若用户已登录，重定向到index
    if g.user is not None and g.user.is_authenticated:
        flash('请勿重复登录！')
        # return redirect(url_for('index'))

    # 若用户未登录，重定向到index
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form.get('email'), password=request.form.get('password')).first()

        if user is None:
            flash('用户名或密码错误！请重新输入！')
            return redirect(url_for('login'))

        remember_me = False
        if request.form.get('remember_me'):
            # print request.form.get('remember_me')
            remember_me = True
        login_user(user, remember=remember_me)
        return redirect(url_for('patient'))

    return render_template('login.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/first_aid')
@login_required
def first_aid():
    return render_template('first_aid.html', jd=103.593302, wd=30.332618)


@app.route('/record/<file_name>')
@login_required
def record(file_name):
    ecgs = ECG.query.all()
    print ecgs
    print file_name
    if not file_name:
        return render_template('record.html', ecgs=ecgs)
    data = []
    with open('app/static/uploads/data/' + file_name, 'r') as f:
        for point in f.readlines():
            data.append(int(point.strip()))
    # print data
    date = 0
    time = 0
    # if num == '1':
    #     date = '2016-1-22 10:38'
    #     time = '30'
    # elif num == '2':
    #     date = '2016-1-22 10:38'
    #     time = '3'
    # elif num == '3':
    #     date = '2016-1-22 10:38'
    #     time = '18'
    return render_template('record.html',ecgs=ecgs, data=data, date=date, time=time)
    # with open('app/static/uploads/data/' + file_name, 'r') as f:
    #     for point in f.readlines():
    #         data.append(int(point.strip()))
    # # print data
    # date = 0
    # time = 0
    # if num == '1':
    #     date = '2016-1-22 10:38'
    #     time = '30'
    # elif num == '2':
    #     date = '2016-1-22 10:38'
    #     time = '3'
    # elif num == '3':
    #     date = '2016-1-22 10:38'
    #     time = '18'
    # return render_template('record.html', data=data, id=num, date=date, time=time)


@app.route('/doctor')
@login_required
def doctor():
    if g.user == None:
        flash('User ' + g.nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('doctor.html',
                           user=g.user)


@app.route('/patient')
@login_required
def patient():
    if g.user == None:
        flash('User ' + g.nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('patient.html',
                           user=g.user)


@app.route('/treatment_record/<int:num>')
@login_required
def treatment_record(num):
    if g.user == None:
        flash('User ' + g.nickname + ' not found.')
        return redirect(url_for('index'))
    user = User.query.filter_by(id=2).first()
    treatments = []
    treatments.append(Treatment('陈钊医生', '儿科', '主治医师', '2015-11-24','四川大学华西医院','莫绪旻','以胸闷、心慌2天来诊，自诉前几天曾熬夜，工作较忙而发病，并觉乏力、纳差。查体：脉搏90次/分，脉率不齐，即查心电图提示：窦性心律不齐，心率88次/分，st-t轻度改变。询问病史，既往体健。考虑：劳累所致心律失常，心肌供血不足。建议患者注意休息，避免劳累，多食富含维生素、蛋白质及微量元素的瓜果蔬菜，如有不适，及时就诊，以免发生严重的心脏疾患。'))
    treatments.append(Treatment('莫亚宁医生', '内科', '主任医师', '2015-11-19','桂林医学院','莫绪旻','感冒数日后觉心慌、乏力，活动后气促来诊，查体：T38度，脉搏110次/分，有停顿。即查心电图：窦性心动过速并不齐，心率112次/分，偶发房性早搏，st段改变。考虑有急性心肌炎可能，建议住院观察。'))
    treatments.append(Treatment('陆光飞医生', '外科', '副主任医师', '2015-11-15','桂林医学院','莫绪旻','因心前区疼痛6年，加重伴呼吸困难10小时来诊。6年反复感心前区疼痛，系膨胀性或压迫感，多于劳累、饭后发作，每次持续3～5分钟，休息后减轻。入院前2月，痛渐频繁，且休息时也发作，入院前10小时，于睡眠中突感心前区剧痛，并向左肩部、臂部放射，且伴大汗、呼吸困难，咳出少量粉红色泡沫状痰液，自含消心痛无缓解。'))
    treatments.append(Treatment('王鹏医生', '内科', '主治医师', '2015-11-11','四川大学华西医院','莫绪旻','经常活动后气急，1小时前上体育课时觉胸闷，气急，头晕，乏力，老师送来就诊，查见：面唇发绀，汗出肢冷，心脏听诊：心率120次/分，二尖瓣区可闻收缩期吹风样杂音，查心电图：窦性心动过速，st—t改变，考虑先天性心脏病，建议入院进一步诊治。'))
    treatments.append(Treatment('莫亚宁医生', '内科', '主治医师', '2015-11-6','桂林医学院','莫绪旻','因反复喘息40余年，咳嗽、咯痰20余年，心慌气急3年，复发并加重半天，在当地诊所予抗炎、止咳、扩张血管等治疗无好转来诊，体格检查： T 37.7℃，P 134次/分，R 27次/分，BP 112/72mmHg。口唇发绀，颈静脉怒张，胸廓呈桶状，颜面及双下肢水肿，心电图：右心室肥大，右束支传导阻滞。考虑慢性肺源性心脏病，建议住院治疗。'))
    treatments.append(Treatment('王鹏医生', '内科', '主治医师', '2015-11-8','四川大学华西医院','莫绪旻','反复喘促14年，双下肢水肿9年，腹胀1年，加重2天来诊，查见：P:111次/分，R:24次/分。端坐呼吸，二尖瓣面容。口唇紫绀，桶状胸，叩诊呈过清音，双肺呼吸音粗糙。心率125次/分，律不齐，心音强弱不等，二尖瓣膜听诊区可闻及隆隆样杂音。腹部膨隆，右侧肝区压痛明显。心电图：心房纤颤；轻度的ST-T异常。考虑风湿性心脏病，心房纤颤，二尖瓣关闭不全 ，心功能Ⅳ级。收住心内科治疗。'))
    # print treatments[0] 
    return render_template('treatment_record.html', user=user, treatment=treatments[num], num=num)


@app.route('/follow_up_info')
@login_required
def follow_up_info():
    if g.user == None:
        flash('User ' + g.nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('follow_up_info.html')


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        if request.form.get('nickname'):
            g.user.nickname = request.form.get('nickname')
        if request.form.get('about_me'):
            g.user.about_me = request.form.get('about_me')
        avatar = request.files.get('avatar')
        if avatar and allowed_file(avatar.filename):
            avatar_name = unicode(
                g.user.id) + '.' + avatar.filename.rsplit('.', 1)[1]
            # avatar_url = os.path.join(UPLOAD_FOLDER, avatar_name)
            avatar.save(UPLOAD_FOLDER + '/' + avatar_name)
            g.user.avatar = avatar_name

        db.session.add(g.user)
        db.session.commit()
        flash('您的修改已保存！')
        return redirect(url_for('edit'))

    return render_template('edit.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=['POST'])
def upload():
    # print data + '\n' + file_name
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        if file_name:
            print 'success!!!!!!!!!!'
            # print request.form.get('data')
            with open('app/static/uploads/data/' + file_name, 'w') as f:
                data = request.form.get('data')
                ecg = ECG(file_name=file_name)
                f.write(data)
                db.session.add(ecg)
                db.session.commit()
                    # print request.form.get('file_name')
        else:
            print 'fail!!!!!!!!!!'
    return 'sz'
        # if file:
        #     file.save( 'app/static/uploads/data/' + file.filename)
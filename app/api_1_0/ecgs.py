from app.api_1_0 import api
from flask import jsonify
from .decorators import allow_cross_domain

import time

# @login_required
@api.route('/record/<file_name>/<num>')
def record(file_name="", num=""):
    # ecgs = ECG.query.all()
    # if not file_name:
    #     return render_template('record.html', ecgs=ecgs)
    data = []
    with open('app/static/uploads/data/' + file_name, 'r') as f:
        for point in f.readlines():
            data.append(int(point.strip()))

    time.sleep(1)
    # print data
    # date = 0
    # time = 0
    # ecg = ECG.query.filter_by(id=num).first()
    # return render_template('record.html', ecgs=ecgs, id=num, data=data, date=ecg.date, time=ecg.time)
    return jsonify({'data': data})

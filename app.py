import urllib

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO

app = Flask(__name__, template_folder='./')

# 配置 MySQL 数据库
password = "Vision123!@#"
encoded_password = urllib.parse.quote_plus(password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://vision:{encoded_password}@123.57.1.100:33063/vision'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 定义数据库模型
class Estate(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    update_date = db.Column(db.DateTime)
    img_url = db.Column(db.String(255))
    source_url = db.Column(db.String(255))
    price = db.Column(db.Float)
    source = db.Column(db.String(50))
    estate_name = db.Column(db.String(255))
    rent_type = db.Column(db.String(50))
    few_room = db.Column(db.Integer)
    room_name = db.Column(db.String(255))
    area = db.Column(db.Float)
    floor = db.Column(db.Integer)
    total_floor = db.Column(db.Integer)
    orientation = db.Column(db.String(50))
    district_name = db.Column(db.String(255))
    business_circle_name = db.Column(db.String(255))
    subway_station_name = db.Column(db.String(255))
    subway_line_name = db.Column(db.String(255))
    walk_distance = db.Column(db.Integer)
    house_tags = db.Column(db.String(255))


# 首页展示表格
@app.route('/')
def index():
    query = Estate.query

    # 处理过滤条件
    filters = request.args.to_dict()
    for key, value in filters.items():
        if hasattr(Estate, key) and value:
            column = getattr(Estate, key)
            query = query.filter(column.like(f"%{value}%"))

    # 处理排序
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    if sort_by and hasattr(Estate, sort_by):
        column = getattr(Estate, sort_by)
        if order == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    data = query.all()

    return render_template('index.html', data=data)


# 导出为 Excel
@app.route('/export')
def export():
    query = Estate.query.all()
    data = [{
        'title': item.title,
        'update_date': item.update_date,
        'img_url': item.img_url,
        'source_url': item.source_url,
        'price': item.price,
        'source': item.source,
        'estate_name': item.estate_name,
        'rent_type': item.rent_type,
        'few_room': item.few_room,
        'room_name': item.room_name,
        'area': item.area,
        'floor': item.floor,
        'total_floor': item.total_floor,
        'orientation': item.orientation,
        'district_name': item.district_name,
        'business_circle_name': item.business_circle_name,
        'subway_station_name': item.subway_station_name,
        'subway_line_name': item.subway_line_name,
        'walk_distance': item.walk_distance,
        'house_tags': item.house_tags,
    } for item in query]

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output, download_name='租房数据（自用）.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7666)

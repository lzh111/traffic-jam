# coding: utf-8
# Author: 刘子豪
# Date: 2020/12/7 8:48
import requests

from pyecharts.charts import Geo
from pyecharts import options as opts
from flask import Flask, render_template


def get_data():
    '''
    获取拥堵指数
    '''
    # 获取各城市的拥堵指数
    url = 'https://jiaotong.baidu.com/trafficindex/city/list'  # 接口api
    res = requests.get(url)
    data = res.json()

    # 提取数据
    citys = [i['cityname'] for i in data['data']['list']]  # 提取城市
    indexs = [float(i['index']) for i in data['data']['list']]  # 提取对应的指数

    # 返回数据
    return zip(citys, indexs)


def get_geo():
    '''
    获取地图
    '''
    # 获取各城市的拥堵指数
    data = get_data()

    # 绘制散点分布图
    geo = Geo()
    geo.add_schema(maptype='china')  # 加入中国地图
    geo.add('各城市拥堵指数 by kimol', data, type_='effectScatter')  # 设置地图类型及数据
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 设置是否显示标签
    geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(
        # max_ = 2.5, # 用于连续表示
        is_piecewise=True,  # 是否分段
        pieces=[{'min': 1.0, 'max': 1.5, 'label': '畅通', 'color': '#16CE95'},
                {'min': 1.5, 'max': 1.8, 'label': '缓行', 'color': '#F79D06'},
                {'min': 1.8, 'max': 2.0, 'label': '拥堵', 'color': '#D80304'},
                {'min': 2.0, 'max': 2.5, 'label': '严重拥堵', 'color': '#8F0921'}]))  # 设置图例显示

    # 返回地图
    return geo


# 定义app
app = Flask(__name__)


# 定义主界面
@app.route("/")
def hello():
    geo = get_geo()
    return render_template('geo.html',
                           mygeo=geo.render_embed())


if __name__ == "__main__":
    # 运行项目
    app.run()

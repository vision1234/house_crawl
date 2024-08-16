# coding=utf-8
import json

import requests
from lxml import etree


def get_woaiwojia_data(base_url, page=1):
    # if zufang_data_list is None:
    zufang_data_list = []
    url = base_url.format(page)
    print(url)
    DEFAULT_REQUEST_HEADERS = {

        "Host": "www.1zu.com",

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }

    res = requests.get(url, headers=DEFAULT_REQUEST_HEADERS).text
    # print(res)
    html = etree.HTML(res)
    data_list_ = html.xpath("//script[@id='__NEXT_DATA__']/text()")[0]
    data_list = json.loads(data_list_)["props"]["pageProps"]["houseList"]
    print(len(data_list))
    # for d in data_list:
    #     print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))

    for d in data_list:
        # print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))
        zufang_data_list.append({
            "img_url": d["coverPicUrl"],
            "source_url": 'https://www.1zu.com/view/' + str(d["id"]),
            "title": "{}·{} {}居室{}{}".format("合租" if d["rentType"] == 2 else "整租", d["estateName"], d["fewRoom"],
                                               "-" if d["roomName"] != "" else "", d["roomName"]),
            "price": d["rentPrice"],
            "source": "相寓",
            "estate_name": d["estateName"],  # 小区
            "rent_type": "合租" if d["rentType"] == 2 else "整租",
            "few_room": d["fewRoom"],  # 居室
            "room_name": d["roomName"],  # 主卧次卧
            "area": d["area"],  # 面积
            "floor": d["floor"],  # 楼层
            "total_floor": d["totalFloor"],  # 总楼层
            "orientation": d["orientation"],  # 朝向
            "district_name": d["districtName"],  # 区
            "business_circle_name": d["businessCircle"]["businessCircleName"],  # 商圈
            "subway_station_name": d["subways"][0]["subwayStationName"] if len(d["subways"]) > 0 else "",  # 地铁站
            "subway_line_name": d["subways"][0]["subwayLineName"] if len(d["subways"]) > 0 else "",  # 地铁线
            "walk_distance": d["subways"][0]["walkDistance"] if len(d["subways"]) > 0 else "",  # 步行距离
            "house_tags": " ".join([h["tagValue"] for h in d["houseTags"]])  # 标签
        })
    total = json.loads(data_list_)["props"]["pageProps"]["total"]
    if total > page * 20:
        print("next!!!!!!!!")
        page += 1
        zufang_data_list += get_woaiwojia_data(base_url, page)
    return zufang_data_list

    # print(get_lianjia_data())
    # print(res.status_code)
    # print(res.text)


if __name__ == '__main__':
    print(json.dumps(
        get_woaiwojia_data("https://www.1zu.com/newHouse/bj/type2/pg{}?kw=%E4%BA%8C%E9%87%8C%E6%B2%9F&isAms=1")))

# coding=utf-8
import json

import requests
from lxml import etree


def get_beike_data(url):
    next_url_path = '//*[@id="content"]//div[@class="content__pg"]/a/@href'
    url_base = url + 'pg{}'

    headers = {
        "Host": "bj.zu.ke.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    i = 1
    zufang_data_list = []
    while True:
        print(url_base.format(i))
        res = requests.get(url_base.format(i), headers=headers).text
        html = etree.HTML(res)
        data_list = html.xpath('//*[@id="content"]//div[@class="content__list--item"]')

        for d in data_list:
            title = d.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]//text()')
            desc = "".join(d.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]//text()')).replace(" ",
                                                                                                                   "").replace(
                "精选/", "")
            zufang_data_list.append({
                "img_url": d.xpath('./a[@class="content__list--item--aside"]/img/@data-src')[0],
                "source_url": 'https://bj.zu.ke.com/' + d.xpath('./a[@class="content__list--item--aside"]/@href')[0],
                "title": ''.join(
                    title).replace(
                    " ",
                    "").replace(
                    "\n", ""),
                "price": int(
                    d.xpath(
                        './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()')[0]),
                "source": "贝壳",
                "estate_name": title[0].strip()[3:title[0].strip().find(" ")],  # 小区
                "rent_type": title[0].strip()[:2],
                "few_room": title[0].strip()[title[0].strip().find(" ") + 1:title[0].strip().find(" ") + 2],  # 居室
                "room_name": title[0].strip()[title[0].strip().rfind(" "):],  # 主卧次卧
                "area": float(desc.split("/")[1].replace("㎡", "")),  # 面积
                "floor": None,  # 楼层
                "total_floor": None,  # 总楼层
                "orientation": desc.split("/")[2],  # 朝向
                "district_name": desc.split("/")[0].split("-")[0].strip(),  # 区
                "business_circle_name": desc.split("/")[0].split("-")[1],  # 商圈
                "subway_station_name": "",  # 地铁站
                "subway_line_name": "",  # 地铁线
                "walk_distance": None,  # 步行距离
                "house_tags": " ".join(d.xpath(
                    './div[@class="content__list--item--main"]/p[@class="content__list--item--bottom oneline"]/i/text()')).replace(
                    "\n", "")  # 标签
            })
        next_tag = ",".join(html.xpath(next_url_path))
        print(next_tag)
        if url_base.format(i + 1) in next_tag:
            i += 1
        else:
            break
    return zufang_data_list


if __name__ == '__main__':
    print(json.dumps(get_beike_data('https://bj.zu.ke.com/ditiezufang/li46107350s1120076969779357/rt200600000002/')))

# print(res.status_code)
# print(res.text)

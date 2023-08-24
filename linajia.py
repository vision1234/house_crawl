# coding=utf-8
import requests
from lxml import etree


def get_lianjia_data():
    url = 'https://bj.lianjia.com/ditiezufang/li656s43137676/rt200600000001l1l2ra2ra3ra4brp4000erp7300/'

    headers = {
        "Host": "bj.lianjia.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    res = requests.get(url, headers=headers).text
    html = etree.HTML(res)
    data_list = html.xpath('//*[@id="content"]//div[@class="content__list--item"]')
    zufang_data_list = []
    for d in data_list:
        zufang_data_list.append({
            "img_url": d.xpath('./a[@class="content__list--item--aside"]/img/@data-src')[0],
            "source_url": 'https://bj.lianjia.com/' + d.xpath('./a[@class="content__list--item--aside"]/@href')[0],
            "title": ''.join(
                d.xpath(
                    './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]//text()')).replace(
                " ",
                "").replace(
                "\n", ""),
            "price": ''.join(
                d.xpath('./div[@class="content__list--item--main"]/span[@class="content__list--item-price"]//text()')),
            "source": "链家"

        })
    return zufang_data_list
    # print(res.status_code)
    # print(res.text)

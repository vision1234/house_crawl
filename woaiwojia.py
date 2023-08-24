# coding=utf-8
import requests
from lxml import etree


def get_lianjia_data(page=1):
    # if zufang_data_list is None:
    zufang_data_list = []
    if page == 1:
        url = "https://bj.5i5j.com/zufang/subway/ss2159/b4000e7300h110l70r2r3t1u1/"
    else:
        url = "https://bj.5i5j.com/zufang/subway/ss2159/b4000e7300h110l70r2r3t1u1n{}/".format(page)
    print(url)
    DEFAULT_REQUEST_HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "bj.5i5j.com",
        "Referer": "https://bj.5i5j.com/map/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }

    res = requests.get(url, headers=DEFAULT_REQUEST_HEADERS).text
    # print(res)
    html = etree.HTML(res)
    data_list = html.xpath('/html/body//ul[@class="pList rentList"]/li')
    # for d in data_list:
    #     print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))

    for d in data_list:
        # print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))
        zufang_data_list.append({
            "img_url": d.xpath('./div[@class="listImg"]/a/img/@src')[0] if (len(
                d.xpath('./div[@class="listImg"]/a/img/@src'))) > 0 else
            d.xpath('./div[@class="listImg"]/a/img/@data-src')[0],
            "source_url": 'https://bj.5i5j.com' + d.xpath('./div[@class="listImg"]/a/@href')[0],
            "title": ''.join(
                d.xpath(
                    './div[@class="listCon"]/div[@class="listX"]/p[1]//text()') + d.xpath(
                    './div[@class="listCon"]/div[@class="listX"]/p[2]//text()')).replace(
                " ",
                "").replace(
                "\n", ""),
            "price": ''.join(
                d.xpath(
                    './div[@class="listCon"]/div[@class="listX"]/div[@class="jia"]/p[@class="redC"]//text()')).replace(
                " ",
                "").replace(
                "\n", ""),
            "source": "我爱我家"

        })
    if (len(html.xpath('/html/body//div[@class="pageSty rf"]/a')) > 0 and
            html.xpath('/html/body//div[@class="pageSty rf"]/a[1]/text()')[0] == '下一页'):
        print("next!!!!!!!!")
        zufang_data_list += get_lianjia_data(page + 1)
    return zufang_data_list

# print(get_lianjia_data())
# print(res.status_code)
# print(res.text)

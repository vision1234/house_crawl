# coding=utf-8
import requests
from lxml import etree


def get_woaiwojia_data(url):
    # if zufang_data_list is None:
    zufang_data_list = []
    # url = "{}n{}/".format(base_url, page)
    print(url)
    DEFAULT_REQUEST_HEADERS = {

        "Host": "www.1zu.com",

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }

    res = requests.get(url, headers=DEFAULT_REQUEST_HEADERS).text
    print(res)
    html = etree.HTML(res)
    data_list = html.xpath("/html/body//div[contains(@class, 'List_list')]/div/a")
    # for d in data_list:
    #     print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))

    for d in data_list:
        # print(d.xpath('./div[@class="listImg"]/a/img/@data-src'))
        zufang_data_list.append({
            "img_url": None,#d.xpath("./div/div[contains(@class, 'ListItem_img')]/img/@src")[0],
            "source_url": 'https://www.1zu.com' + d.xpath('./@href')[0],
            "title": ''.join(
                d.xpath(
                    "./div/div[contains(@class, 'ListItem_content')]/div[contains(@class, 'ListItem_title')]//text()") + d.xpath(
                    "./div/div[contains(@class, 'ListItem_content')]/div[contains(@class, 'ListItem_desc')]//text()")).replace(
                "\n", ""),
            "price": ''.join(
                d.xpath(
                    "./div/div[contains(@class, 'ListItem_price')]//text()")).replace(
                " ",
                "").replace(
                "\n", ""),
            "source": "相寓"

        })
    if len(html.xpath(
            "/html/body//div[contains(@class, 'List_list')]//a[contains(@class, 'Pagination_nextTrigger')]/@href")) > 0:
        print("next!!!!!!!!")
        zufang_data_list += get_woaiwojia_data("https://www.1zu.com" + html.xpath(
            "/html/body//div[contains(@class, 'List_list')]//a[contains(@class, 'Pagination_nextTrigger')]/@href")[
            0])
        return zufang_data_list

    # print(get_lianjia_data())
    # print(res.status_code)
    # print(res.text)


if __name__ == '__main__':
    print(get_woaiwojia_data("https://www.1zu.com/newHouse/bj/type2/pg1?kw=%E4%BA%8C%E9%87%8C%E6%B2%9F&isAms=1"))

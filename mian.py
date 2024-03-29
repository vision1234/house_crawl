import linajia
import woaiwojia
import send_mail
import pymysql
import config

connection = pymysql.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.database
)

# 創建一個游標對象
cursor = connection.cursor()


def get_yesterday_data_one(source_url):
    # 執行SELECT查詢
    sql = "SELECT count(1) FROM houses where update_date=DATE_ADD(CURDATE(),INTERVAL -1 DAY) and source_url=%s"
    cursor.execute(sql, source_url)

    results = cursor.fetchone()

    return list(results)


def get_yesterday_data_all():
    # 執行SELECT查詢
    sql = "SELECT * FROM houses where update_date=DATE_ADD(CURDATE(),INTERVAL -1 DAY)"
    cursor.execute(sql)

    # 獲取所有結果行
    results_list = []
    results = cursor.fetchall()
    for r in results:
        results_list.append({
            "title": r[1],
            "img_url": r[3],
            "source_url": r[4],
            "price": r[5],
            "source": r[6]
        })
    return results_list


def insert_today_data(data):
    # 執行INSERT語句
    insert_sql = "insert into houses (title,update_date,img_url,source_url,price,source) VALUES(%s,CURDATE(),%s,%s,%s,%s)"
    for d in data:
        data_to_insert = (d["title"], d["img_url"], d["source_url"], d["price"], d["source"])

        cursor.execute(insert_sql, data_to_insert)

        # 提交事務
        connection.commit()


def get_source_from_data(zf_data):
    res = []
    for d in zf_data:
        res.append(d["source_url"])
    return res


if __name__ == '__main__':
    # print(get_yesterday_data_all())
    new_data = []
    old_data = []
    down_data = []
    data_list = linajia.get_lianjia_data() + woaiwojia.get_lianjia_data()
    for data in data_list:
        if not get_yesterday_data_one(data["source_url"])[0]:
            new_data.append(data)
        else:
            old_data.append(data)
    source_urls = get_source_from_data(data_list)
    yesterday_data = get_yesterday_data_all()
    for t in yesterday_data:
        if t["source_url"] not in source_urls:
            down_data.append(t)

    mail_data = send_mail.get_html(new_data, down_data, old_data)
    send_mail.mail(config.to_mail, mail_data)
    insert_today_data(data_list)

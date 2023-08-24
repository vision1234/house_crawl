#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import logging
import arrow
import config

# 第三方 SMTP 服务

my_sender = config.my_sender  # 发件人邮箱账号
my_pass = config.my_pass  # 口令
from_name = config.from_name
to_name = config.to_name


def mail(u, datas):
    ret = True
    # for u in my_user:
    try:
        mes_str = datas
        msg = MIMEText(mes_str, _subtype="html", _charset='utf-8')
        msg['From'] = formataddr([from_name, my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_name, u])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "租房推送"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [u, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(e)
        logging.exception(e)
        ret = False
    return ret


def get_html(new_data, down_data, old_data):
    mail_module = ""
    news = ""
    downs = ""
    items = ""
    with open("zufang.html", "r", encoding='utf-8') as f:
        mail_module = f.read()
    # print(mail_module)
    item_module = """
         <div class="listing-item">
                <div class="image-container">
                    <img src="{img_url}" alt="Property 1">
                </div>
                <div class="listing-details">
                    <h3><a href='{source_url}';>{title}</a></h3>
                    <p><span>价格：{price}     </span> 来源：{source}</p>
                </div>
            </div>
    """
    for row in new_data:
        new = item_module.format(img_url=row["img_url"], source_url=row["source_url"], title=row["title"],
                                  price=row["price"],
                                  source=row["source"])
        news += new
    # print(items)
    to_day = arrow.now().format("YYYY-MM-DD")
    mail_text = mail_module.replace("{news}", news).replace("{date}", to_day).replace("{new_num}", str(len(new_data)))
    for row in down_data:
        down = item_module.format(img_url=row["img_url"], source_url=row["source_url"], title=row["title"],
                                  price=row["price"],
                                  source=row["source"])
        downs += down
    # print(items)
    mail_text = mail_text.replace("{downs}", downs).replace("{down_num}", str(len(down_data)))

    for row in old_data:
        old = item_module.format(img_url=row["img_url"], source_url=row["source_url"], title=row["title"],
                                  price=row["price"],
                                  source=row["source"])
        items += old
    # print(items)
    mail_text = mail_text.replace("{items}", items).replace("{num}", str(len(old_data)))
    return mail_text

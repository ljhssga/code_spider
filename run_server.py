# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import uuid

from db.DbClient import DBClient

headers = {
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Host": "ss.cods.org.cn"
}

index_url = "https://www.cods.org.cn/"
myDb = DBClient()


def info(soup, data):
    result = soup.select('body > div.container > div.content.clearfix > div.main > div.result.result-2 > div')
    for res in result:
        # 机构名称
        name = res.select("div.tit > a > h3")[0].get_text()
        # 经营状态
        status = res.select("div.tit > a > em")
        statusStr = ""
        if status is not None and len(status) > 0:
            statusStr = status[0].string
        # 信用代码
        code = res.select("div.info >p")[0].string
        # 成立日期
        dateOfesta = res.select("div.info >p")[1].string
        # 登记号
        registrCode = res.select("div.info >p")[2].string
        # 注册地址
        registrAddr = res.select("div.info")[1].select('p')[0].string
        # 经营期限
        operatingPeriod = res.select("div.info")[1].select('p')[1].string
        id = uuid.uuid1()
        sql_temp = "INSERT INTO `organization` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"
        sql = sql_temp % (
            id, name, '', dateOfesta, '', code, '', '', operatingPeriod,registrCode ,'' , '', '', registrAddr)
        myDb._exeCute(sql)


def start(cookie, current_url):
    setCookies(cookie=cookie)
    res = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(str(res.text), 'lxml')
    empty = soup.select('div[class=each-empty]')
    if len(empty) < 1:
        # 总条数
        count = soup.select(
            'body > div.container > div.content.clearfix > div.main > div.position.position2 > p > strong:nth-child(1)')[
            0].string
        allPage = 1
        if int(count) > 10:
            # 下一页的标签
            pageNext = soup.select('a[class=next]')[0]
            # 总页数
            allPage = pageNext.find_previous_sibling('a').string
        data = []
        for i in range(1, int(allPage) + 1):
            if i == 1:
                info(soup=soup, data=data)
            else:
                next_url = current_url.replace('currentPage=1', 'currentPage=' + str(i))
                res = requests.get(next_url, headers=headers)
                soup = BeautifulSoup(str(res.text), 'lxml')
                info(soup=soup, data=data)
        return data
    else:
        print('-----无数据-----')


def setCookies(cookie, current_url):
    cookieStr = ""
    for c in cookie:
        cookieStr += c['name'] + "=" + c['value'] + ";"
    headers['Cookie'] = cookieStr
    return current_url

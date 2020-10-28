# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
from urllib import parse
import pymysql
import requests
from login.chaojiying import Chaojiying_Client
from login.connecting import conn
from login.config import table,cookie_table
from taskmanage.settings import logger

num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.headers1 = self.r_headers1()
        self.headers2 = self.r_headers2()
        self.url = self.r_url()
        self.url2 = self.r_url2()
        self.url3 = self.r_url3()
        self.proxies = self.r_proxies()

    def r_session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def r_headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Length':'87',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_headers1(self):
        headers1 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
        }
        return headers1

    def r_headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
            'X - Requested - With':'XMLHttpRequest'
        }
        return headers2

    def r_url(self):
        url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/'
        return url

    def r_url2(self):
        url2 = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/misc.php?mod=seccode&action=update&idhash=cSA&0.3610130124744941&modid=member::logging'
        return url2

    def r_url3(self):
        url3 = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        return url3

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Lfwpm'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http': proxie}
        return proxies

    def suff(self):
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(res.status_code)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        data = {
            'fastloginfield': 'username',
            'username': username,
            'password': password,
            'quickforward': 'yes',
            'handlekey': 'ls'
        }
        logger.info(data)
        resp = self.session.post(self.url3, headers=self.headers, proxies=self.proxies,data=data)
        logger.info(resp.status_code)
        time.sleep(2)
        login_url = re.findall("'login',.'(.*?)referer=", resp.text)[0]
        login_url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/{}referer=http%3A%2F%2Flfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion%2F&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'.format(login_url)
        login_url = parse.unquote(login_url)
        #logger.info(login_url)
        auth = re.findall("auth=(.*?)&referer",resp.text)[0]
        auth = parse.unquote(auth)
        #logger.info(auth)
        g_data = {
            'mod': 'logging',
            'action': 'login',
            'auth': auth,
            'referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'infloat': 'yes',
            'handlekey': 'login',
            'inajax': '1',
            'ajaxtarget': 'fwin_content_login',
        }
        logger.info(g_data)
        respon = self.session.post(login_url, headers=self.headers2, proxies=self.proxies, data=g_data)
        logger.info(respon.status_code)
        #logger.info(respon.text)
        time.sleep(2)
        response = self.session.get(self.url2, headers=self.headers1, proxies=self.proxies)
        logger.info(response.status_code)
        #logger.info(response.text)
        time.sleep(2)
        url_code = re.findall('src="(.*?)" class="vm"',response.text)[1]
        #logger.info(url_code)
        url_code = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/{}'.format(url_code)
        code_response = self.session.get(url_code, headers=self.headers2, proxies=self.proxies)
        logger.info(code_response.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/img/lfwpm.png".format(path), 'wb').write(code_response.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/lfwpm.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        logger.info(result)
        post_code = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=cSA&secverify={}'.format(result)
        #logger.info(post_code)
        code_data = {
            'mod': 'seccode',
            'action': 'check',
            'inajax': '1',
            'modid': 'member::logging',
            'idhash': 'cSA',
            'secverify': result,
        }
        logger.info(code_data)
        formhash = re.findall('name="formhash" value="(.*?)" />',respon.text)[0]
        #logger.info(formhash)
        loginhash = re.findall('loginhash=(.*?)">',respon.text)[0]
        #logger.info(loginhash)
        last_url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={}&inajax=1'.format(loginhash)
        #logger.info(last_url)
        last_data = {
            'formhash': formhash,
            'referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'auth': auth,
            'seccodehash': 'cSA',
            'seccodemodid': 'member::logging',
            'seccodeverify': result,
        }
        logger.info(last_data)
        time.sleep(2)
        last_response = self.session.post(last_url, headers=self.headers, proxies=self.proxies,data=last_data)
        logger.info(last_response.status_code)
        logger.info(last_response.text)

        post_code_response = self.session.post(post_code, headers=self.headers2, proxies=self.proxies,data=code_data)
        logger.info(post_code_response.status_code)
        #logger.info(post_code_response.text)

        if '欢迎您回来' in last_response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
            # cursor = conn.cursor()  # 创建游标对象
            # sql = "insert into lfwpm(cookies) values (%s);"
            # #"update bjhgd_tor_info SET cookie=%s WHERE project_name='Apollo'"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()  # 提交
            # cursor.close()
            # conn.close()
        else :
            if len(num) <= 3:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies


    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        logger.info(im_id)

    def main(self):
        num.append(1)
        username,jsonCookies =self.suff()
        return username,jsonCookies



if __name__ == '__main__':
    l = Login()
    l.main()
import os
import re
import sys
import time
from datetime import datetime

import requests
import whois

from predeldomain.utils.enum import Mode

"""
Provider 提供者
"""


class Provider:
    data = []

    whois_tencent_url = 'https://dnspod.cloud.tencent.com/cgi/capi?action=DescribeWhoisInfoSpecial&csrfCode=&innerCapiMark=1'

    def __init__(
        self,
        length=3,
        mode=Mode.ALPHABETIC.value,  # noqa: F821
        whois='',
        delay=3,
        ouput=False,
    ):
        self.length = length
        self.mode = mode
        self.whois = whois
        self.delay = delay
        self.ouput = ouput

    def entry(self):  # noqa: B027
        """
        主函数
        """
        pass

    def data_all(self):
        """
        获取所有数据
        """
        return self.data

    def data_early(self):
        """
        获取昨日数据
        """
        return self.data[0] if len(self.data) > 0 else []

    def data_today(self):
        """
        获取今日数据
        """
        return self.data[1] if len(self.data) > 1 else []

    def data_tomorrow(self):
        """
        获取明日数据
        """
        return self.data[2] if len(self.data) > 2 else []

    def data_future(self):
        """
        获取未来数据
        """
        return self.data[3:] if len(self.data) > 3 else []

    def match_mode(self, data):
        """
        匹配模式
        """
        if self.mode == Mode.ALPHANUMERIC.value and not re.match(
            r'^[a-zA-Z0-9]+$', data
        ):
            return False
        if self.mode == Mode.NUMERIC.value and not re.match(r'^[0-9]+$', data):
            return False
        if self.mode == Mode.ALPHABETIC.value and not re.match(r'^[a-zA-Z]+$', data):
            return False
        return True

    def remove_file(self, file_name: str):
        """
        删除文件
        """
        if os.path.isfile(file_name):
            os.remove(file_name)

    def should_download_file(self, file_name: str):
        """
        检查是否需要下载文件
        """
        if not os.path.isfile(file_name):
            return True
        file_time = datetime.fromtimestamp(os.path.getmtime(file_name))
        return file_time.date() != datetime.now().date()

    def print_data(self, domain, is_available=False):
        """
        打印数据
        """
        if self.ouput:
            print(f'{domain} is available: {is_available}')

    def is_domain_available(self, domain):
        """
        判断是否可注册
        """

        if self.whois == 'nic':  # nic.top
            if '.top' in domain:
                is_available = self.nic_top_available(domain)
                self.print_data(domain, is_available)
                return is_available
            else:
                return False

        time.sleep(self.delay)

        is_available = False
        if self.whois == 'isp':
            is_available = self.isp_available(domain)
        elif self.whois == 'whois':
            is_available = self.whois_available(domain)
        else:
            return True

        self.print_data(domain, is_available)
        return is_available

    def nic_top_available(self, domain):
        """
        通过 nic.top 判断是否可注册
        """
        params = {'domainName': domain}
        response = requests.post('https://www.nic.top/cn/whoischeck.asp', data=params)
        return 'is available' in response.text

    def whois_available(self, domain):
        """
        通过 Whois 判断是否可注册
        """
        try:
            w = whois.query(domain)
            # return True if w.available else False
            if w is None:
                return True
            else:
                return False
        except Exception as e:
            print(f'Error: {domain}, {e}', file=sys.stderr)
            return False

    def isp_available(self, domain):
        """
        通过 ISP 判断是否可注册
        """

        data = {
            'Version': '2018-08-08',
            'serviceType': 'domain',
            'api': 'DescribeWhoisInfoSpecial',
            'DomainName': domain,
            'dpNodeCustomClientIPField': 'RealClientIp',
        }

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '149',
            'content-type': 'application/json; charset=UTF-8',
            # 'cookie': '__root_domain_v=.tencent.com; _qddaz=QD.725133824044670; hy_user=a_98e5efef527597446e27dcffc370ae58; hy_token=R4Fso9Hx4m6w7zCdXsxx0cMFpR5yqUGgMw/q9ioxg1Vcrpd46wehlnDrLKYPWyfwn0yPhOrq1LckTgoLv0p7dA==; hy_source=web; qcloud_uid=oJv0qdK_ZSks; language=zh; qcstats_seo_keywords=%E5%93%81%E7%89%8C%E8%AF%8D-%E5%93%81%E7%89%8C%E8%AF%8D-%E7%99%BB%E5%BD%95; _ga=GA1.2.261890131.1733898849; _gcl_au=1.1.1975438295.1733898849; loginType=wx; sid=b8b508544870b6d77b724ffb9ccad6cc; trafficParams=***%24%3Btimestamp%3D1733987618427%3Bfrom_type%3Dserver%3Btrack%3Da49c89bc-d795-4377-a9ef-098cdcc67e3d%3B%24***; qcloud_visitId=22dcaec137f7d8ed64f5a131576e916e; _gat=1; qcmainCSRFToken=SkzN-My9N1g; intl=; qcloud_outsite_refer=https://whois.cloud.tencent.com;  qcloud_from=qcloud.inside.whois-1734107656341; dp.sess=b80f551d2e83e8aad0505b61e27b85a22e69538b29716c4a4a',
            'origin': 'https://whois.cloud.tencent.com',
            'priority': 'u=1, i',
            'referer': 'https://whois.cloud.tencent.com/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        response = requests.post(self.whois_tencent_url, json=data, headers=headers)

        try:
            if response.status_code != 200:
                raise ValueError(f'status code {response.status_code}')

            resp = response.json()
            if 'message' in resp and '未注册' in resp['message']:
                return True
            else:
                return False

        except Exception as e:
            print(f'Error: find domain: {domain}, err:{e}')
        return False

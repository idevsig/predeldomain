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
    proxy_url = ''

    whois_tencent_url = 'https://dnspod.cloud.tencent.com/cgi/capi?action=DescribeWhoisInfoSpecial&csrfCode=&innerCapiMark=1'
    whois_zzzzy_url = 'https://www.zzidc.com/domain/checkDomain'

    whois_westxyz_url_f = (
        'https://www.west.xyz/web/whois/whoisinfo?domain={}&server=&refresh=0'
    )

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

        self.proxy_url = os.environ.get('PROXY', '')

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

        # 未传入 whois 参数时，直接返回 True
        if not self.whois:
            return True

        if self.whois == 'nic':  # nic.top
            if '.top' in domain:
                is_available = self.nic_top_available(domain)
                self.print_data(domain, is_available)
                return is_available
            else:
                return False

        time.sleep(self.delay)

        is_available = False
        if self.whois == 'qcloud':
            is_available = self.qcloud_available(domain)
        elif self.whois == 'whois':
            is_available = self.whois_available(domain)
        elif self.whois == 'westxyz':
            is_available = self.westxyz_available(domain)
        elif self.whois == 'zzidc':
            is_available = self.zzidc_available(domain)
        else:
            return False

        self.print_data(domain, is_available)
        # exit()
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

    def qcloud_available(self, domain):
        """
        通过腾讯云判断是否可注册
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
            'cookie': '__root_domain_v=.tencent.com; _qddaz=QD.725133824044670; hy_user=a_98e5efef527597446e27dcffc370ae58; hy_token=R4Fso9Hx4m6w7zCdXsxx0cMFpR5yqUGgMw/q9ioxg1Vcrpd46wehlnDrLKYPWyfwn0yPhOrq1LckTgoLv0p7dA==; hy_source=web; qcloud_uid=oJv0qdK_ZSks; language=zh; qcstats_seo_keywords=%E5%93%81%E7%89%8C%E8%AF%8D-%E5%93%81%E7%89%8C%E8%AF%8D-%E7%99%BB%E5%BD%95; _ga=GA1.2.261890131.1733898849; _gcl_au=1.1.1975438295.1733898849; loginType=wx; sid=b8b508544870b6d77b724ffb9ccad6cc; trafficParams=***%24%3Btimestamp%3D1733987618427%3Bfrom_type%3Dserver%3Btrack%3Da49c89bc-d795-4377-a9ef-098cdcc67e3d%3B%24***; qcloud_visitId=22dcaec137f7d8ed64f5a131576e916e; _gat=1; qcmainCSRFToken=SkzN-My9N1g; intl=; qcloud_outsite_refer=https://whois.cloud.tencent.com;  qcloud_from=qcloud.inside.whois-1734107656341; dp.sess=b80f551d2e83e8aad0505b61e27b85a22e69538b29716c4a4a',
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

    def westxyz_available(self, domain):
        """
        通过西部数码判断是否可注册
        """

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'ASPSESSIONIDQQATDBSB=LEPMIJEBGHJLEOPJCMBPNABI; sl-session=n+1cVW01xGfWRywhseix0A==; _ga=GA1.2.1826926937.1740825590; _gid=GA1.2.1831307472.1740825590; PHPSESSID=65v2fjoom432tqpjpaj68gifj6; SERVICEID=12|Z8LkH; ads_n_tongji_ftime=2025-3-1%2018%3A40%3A27; _ga_Q0EHN509HH=GS1.2.1740825593.1.1.1740825628.25.0.0',
            'Host': 'www.west.xyz',
            'Referer': 'https://www.west.xyz/en/domain/whois.asp',
            'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        whois_westxyz_url = self.whois_westxyz_url_f.format(domain)
        response = requests.get(whois_westxyz_url, headers=headers)

        try:
            if response.status_code != 200:
                raise ValueError(f'status code {response.status_code}')

            resp = response.json()
            if 'code' in resp and (resp['code'] == 200 or resp['code'] == 100):
                return resp['regdate'] == ''
            else:
                raise ValueError(f'resp code {resp["code"]}')

        except Exception as e:
            print(f'Error: find domain: {domain}, err:{e}')
        return False

    def zzidc_available(self, domain):
        """
        通过判断景安网络是否可注册
        """

        data = {
            'domain': domain,
        }

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '14',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=12b8320f-056b-4857-ae8e-576a870136b1; __jsluid_s=4be4c292c75599d479a132ce8514b599; _pykey_=e2e80de0-0add-59c7-8b4b-0acd76ea36c6',
            'Host': 'www.zzidc.com',
            'Origin': 'https://www.zzidc.com',
            'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        response = requests.post(self.whois_zzzzy_url, data=data, headers=headers)

        try:
            if response.status_code != 200:
                raise ValueError(f'status code {response.status_code}')

            date_pattern = r'val:\s*(\d+)'

            val_match = re.search(date_pattern, response.text)
            if val_match:
                return val_match.group(1) == '1'

        except Exception as e:
            print(f'Error: find domain: {domain}, err:{e}')
        return False

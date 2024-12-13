import requests

from predeldomain.provider.provider import Provider


class CN(Provider):
    file_urls = {
        'today': 'https://www.cnnic.cn/NMediaFile/domain_list/1todayDel.txt',
        'tomorrow': 'https://www.cnnic.cn/NMediaFile/domain_list/future1todayDel.txt',
        'after_tomorrow': 'https://www.cnnic.cn/NMediaFile/domain_list/future2todayDel.txt',
    }

    def download_txt(self, url):
        """
        下载 TXT 文件
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(
                f'Failed to download TXT file from {url}, status code: {response.status_code}'
            )

    def is_domain_available(self, domain):
        """
        判断是否可注册
        """
        full_domain = f'{domain}.cn'
        if self.whois == 'isp':
            return self.isp_available(full_domain)
        elif self.whois == 'whois':
            return self.whois_available(full_domain)
        else:
            return True

    def _process_response(self, response, is_today=False):
        """
        处理响应数据并返回符合条件的域名列表
        """
        domain_list = []
        for line in response.splitlines():
            domain = (
                line.strip('[]').strip().replace('.cn', '')
            )  # 去除中括号,多余空格和.cn后缀
            if not self.match_mode(domain):  # 检查域名匹配模式
                continue
            if len(domain) <= self.length:
                if is_today:
                    if self.is_domain_available(domain):
                        domain_list.append(domain)
                else:
                    domain_list.append(domain)
        return domain_list

    def entry(self):
        """
        主函数
        """
        # 下载并处理今天的数据
        today_resp = self.download_txt(self.file_urls['today'])
        data_list = self._process_response(today_resp, True)

        # 下载并处理明天和后天的数据
        data_tomorrow = []
        data_after_tomorrow = []

        tomorrow_resp = self.download_txt(self.file_urls['tomorrow'])
        data_tomorrow = self._process_response(tomorrow_resp)

        after_tomorrow_resp = self.download_txt(self.file_urls['after_tomorrow'])
        data_after_tomorrow = self._process_response(after_tomorrow_resp)

        # 排序结果
        data_list.sort()
        data_tomorrow.sort()
        data_after_tomorrow.sort()
        self.data = [data_list, data_tomorrow, data_after_tomorrow]

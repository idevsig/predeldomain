import csv
from datetime import datetime
from datetime import timedelta
from io import StringIO

import requests

from predeldomain.provider.provider import Provider


class TOP(Provider):
    csv_file = 'top.csv'
    file_url = 'https://www.nic.top/upload/top/dellist.csv'

    def download_csv(self):
        """
        定义下载 CSV 文件的函数
        """
        response = requests.get(self.file_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(
                f'Failed to download CSV file, status code: {response.status_code}'
            )

    def is_domain_available(self, domain):
        """
        判断是否可注册
        """

        if self.whois == 'isp':
            params = {'domainName': domain}
            response = requests.post(
                'https://www.nic.top/cn/whoischeck.asp', data=params
            )
            return 'is available' in response.text
        elif self.whois == 'whois':
            return self.whois_available(f'{domain}.top')
        else:
            return True

    def entry(self):
        """
        主函数
        """

        resp_content = self.download_csv()
        # 将响应内容解码为文本
        content = resp_content.decode('gbk')

        # 使用 StringIO 创建类文件对象
        csv_file = StringIO(content)
        reader = csv.reader(csv_file)

        self.remove_file(self.csv_file)

        next(reader)  # 跳过 CSV 文件的头部

        data_list = []
        data_next = []

        for row in reader:
            data = row[0].replace('.top', '')
            if not self.match_mode(data):
                continue
            if len(data) <= self.length:
                given_time = datetime.strptime(row[1], '%Y/%m/%d %H:%M')
                if given_time < datetime.now():
                    if self.is_domain_available(data):
                        data_list.append(data)
                    else:
                        data_list.append(data)
                elif given_time < datetime.now() + timedelta(days=1):
                    data_next.append(data)

        data_list.sort()
        data_next.sort()
        self.data = [data_list, data_next]

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

        # 早期
        data_early = []
        data_today = []
        data_tomorrow = []
        data_future = []

        for row in reader:
            domain = row[0].replace('.top', '')
            if not self.match_mode(domain):
                continue
            if len(domain) <= self.length:
                given_time = datetime.strptime(
                    row[1], '%Y/%m/%d %H:%M'
                )  # 解析时间字符串
                current_date = datetime.now().date()  # 获取当前日期
                tomorrow_date = current_date + timedelta(days=1)  # 计算明天的日期

                # 检查日期
                if given_time.date() < current_date:  # 如果日期是过去
                    data_early.append(domain)  # 过去的数据
                if given_time.date() == current_date:  # 如果日期是今天
                    if (
                        given_time.time() > datetime.now().time()
                    ):  # 如果时间大于当前时间
                        continue
                    if not self.is_domain_available(
                        f'{domain}.top'
                    ):  # 判断域名是否可用
                        continue

                    data_today.append(domain)  # 今天过期且可用
                elif given_time.date() == tomorrow_date:  # 如果日期是明天
                    data_tomorrow.append(domain)  # 明天过期的数据
                elif given_time.date() > tomorrow_date:  # 如果日期是未来
                    data_future.append(domain)  # 添加到未来过期的数据列表

        data_early.sort()
        data_today.sort()
        data_tomorrow.sort()
        data_future.sort()
        self.data = [data_early, data_today, data_tomorrow, data_future]

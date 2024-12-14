import json
from datetime import datetime
from os import environ

from ipush import Lark
from ipush import PushDeer

from predeldomain.provider.provider import Provider
from predeldomain.provider.provider_cn import CN
from predeldomain.provider.provider_top import TOP


def write_log(data_list, suffix, type='text'):
    """
    处理数据
    """

    if len(data_list) == 0:
        return

    today = datetime.now().date()
    file_log = f'{suffix}_{today}.log'
    file_log_next = f'{suffix}_{today}_next.log'

    # print(data_list)

    if type == 'text':
        data_str = f'.{suffix}\n'.join(data_list[0]) + f'.{suffix}\n'
        with open(file_log, 'w') as f:
            f.write(data_str)

        for i in range(1, len(data_list)):
            if i == 1:
                wmode = 'w'
            else:
                wmode = 'a'

            data_str = f'.{suffix}\n'.join(data_list[i]) + f'.{suffix}\n'
            with open(file_log_next, wmode) as f:
                f.write(f'===========================================\n{data_str}')

    elif type == 'json':
        data_json = json.dumps(data_list[0], indent=4)
        with open(file_log, 'w') as f:
            f.write(data_json)

        merged_list = sum(data_list[1:], [])
        data_json = json.dumps(merged_list, indent=4)
        with open(file_log_next, 'w') as f:
            f.write(data_json)


def notify(data_list, suffix):
    """
    发送通知
    """
    if len(data_list) == 0:
        return

    content = ''
    content_markdown = ''
    content_text = ''
    # 今天数据
    if len(data_list[0]) > 0:
        content = '\n'.join(data_list[0])
        content_markdown = f'**域名 `{suffix}` 今天过期:**\n```bash\n{content}\n```'
        content_text = f'域名 {suffix} 今天过期:\n{content}\n'

    # 明天数据
    content_next = ''
    content_next_markdown = ''
    content_next_text = ''
    if len(data_list) > 1:
        content_next = '\n'.join(data_list[1])
        content_next_markdown = (
            f'**域名 `{suffix}` 明天过期:**\n```bash\n{content_next}\n```'
        )
        content_next_text = f'域名 {suffix} 明天过期:\n{content_next}\n'

    # 发送通知 PushDeer
    pushdeer_token = environ.get('PUSHDEER_TOKEN', '')
    if pushdeer_token != '':
        notify = PushDeer(pushdeer_token)
        if content:
            notify.settype('markdown').send(content_markdown)

        if content_next:
            notify.settype('markdown').send(content_next_markdown)

    # 发送通知 Lark
    lark_token = environ.get('LARK_TOKEN', '')
    lark_secret = environ.get('LARK_SECRET', '')
    if lark_token != '' and lark_secret != '':
        notify = Lark(lark_token, lark_secret)
        if content:
            notify.send(content_text)

        if content_next:
            notify.send(content_next_text)


def entry(args):
    """
    主函数
    """

    functions = {'top': TOP, 'cn': CN}

    # print(
    #     f'Domain Suffix: {args.suffix}, Length: {args.length}, Mode: {args.mode}, Whois: {args.whois}'
    # )
    provider = functions.get(args.suffix, Provider)(args.length, args.mode, args.whois)
    provider.entry()

    data_list = provider.data_all()
    write_log(data_list, args.suffix, args.type)

    notify(data_list, args.suffix)

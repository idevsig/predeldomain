import json
import sys
from datetime import datetime
from os import environ

from ipush import Lark
from ipush import PushDeer

from predeldomain.provider.provider import Provider
from predeldomain.provider.provider_cn import CN
from predeldomain.provider.provider_top import TOP


def write_log(provider, suffix, type='text'):
    """
    处理数据
    """

    if len(provider.data) < 2:
        return

    today = datetime.now().date()
    file_log = f'{suffix}_{today}.log'
    file_log_prev = f'{suffix}_{today}_prev.log'
    file_log_next = f'{suffix}_{today}_next.log'

    data = provider.data_all()
    data_early = provider.data_early()
    data_today = provider.data_today()

    if type == 'text':
        if len(data_early) > 0:
            with open(file_log_prev, 'w') as f:
                f.write(f'.{suffix}\n'.join(data_early) + f'.{suffix}\n')
        if len(data_today) > 0:
            with open(file_log, 'w') as f:
                f.write(f'.{suffix}\n'.join(data_today) + f'.{suffix}\n')

        for i in range(2, len(data)):
            if i == 2:
                wmode = 'w'
                title = '明天过期'
            else:
                wmode = 'a'
                title = '明天以后过期'

            data_str = f'.{suffix}\n'.join(data[i]) + f'.{suffix}\n'
            with open(file_log_next, wmode) as f:
                f.write(f'============={title}=====================\n{data_str}')

    elif type == 'json':
        data_json = json.dumps(data, indent=4)
        with open(file_log, 'w') as f:
            f.write(data_json)


def notify(provider, suffix):
    """
    发送通知
    """
    if len(provider.data) < 2:
        return

    data_today = provider.data_today()
    data_tomorrow = provider.data_tomorrow()

    content = ''
    content_markdown = ''
    content_text = ''
    # 今天数据
    if len(data_today) > 0:
        content = '\n'.join(data_today)
        content_markdown = f'**域名 `{suffix}` 今天过期:**\n```bash\n{content}\n```'
        content_text = f'域名 {suffix} 今天过期:\n{content}\n'

    # 明天数据
    content_next = ''
    content_next_markdown = ''
    content_next_text = ''
    if len(data_tomorrow) > 1:
        content_next = '\n'.join(data_tomorrow)
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

    if args.suffix not in functions:
        raise Exception(f'Unsupported suffix: {args.suffix}')

    if args.whois == 'nic':
        if args.suffix != 'top':
            print('nic.top only', file=sys.stderr)
            sys.exit(1)

    # print(
    #     f'Domain Suffix: {args.suffix}, Length: {args.length}, Mode: {args.mode}, Whois: {args.whois}'
    # )
    provider = functions.get(args.suffix, Provider)(
        args.length, args.mode, args.whois, args.delay, args.ouput
    )
    provider.entry()

    write_log(provider, args.suffix, args.type)

    notify(provider, args.suffix)

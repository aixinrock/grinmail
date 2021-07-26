import re
import logging
import time
import sys
import configparser

import zmail

from wallet import GrinWallet


def send_mail(receiver,subject,content,slate_file):
    mail = {'subject':subject,
            'content_text':content,
            'attachments':slate_file,
    }
    server.send_mail(receiver,mail)
    logger.info('已发送GrinMail交易邮件，等待回复')

def receive_mail(new_mail):
    logger.info('收到回复邮件 %s',new_mail['subject'])
    if new_mail['attachments']:
        if 'S2.slatepack' in new_mail['attachments'][0][0]:
            slatepack2 = new_mail['attachments'][0][1].decode()
            logger.debug('接收方回传的Slatepack2数据：%s',slatepack2)
            return slatepack2

    try:
        mail_content = new_mail['content_text'][0]
    except:
        return
    pattern = re.compile(r'BEGINSLATEPACK.[\s\S]*?ENDSLATEPACK.')
    slatepack = re.search(pattern,mail_content).group()
    slatepack2 = ' '.join(slatepack.split())
    logger.debug('正文中匹配到的Slatepack2数据：%s',slatepack)
    return slatepack2


def main():
    logger.info('开始生成Slatepack1数据...')
    wallet = GrinWallet(wallet_password)
    slatepack,slate_file = wallet.send(amount)
    logger.info('发送Slatepack1数据到邮箱 %s',receiver)
    subject = '[GrinMail] 收到Grin交易（Receive Grin slatepack1）'
    content = f'恭喜你！收到一笔Grin交易金额为 {amount} GRIN \n'\
              f'Congratulations! Received a transaction in the amount of {amount} GRIN.\n'\
              '你收到的slatepack1信息如下：\n'\
              'The slatepack1 message you received is as follows: \n'\
              '————————————————————————'\
              f'\n{slatepack}\n'\
              '————————————————————————\n'\
              '请将以上信息复制粘贴到钱包，或将附件提交到钱包，以获得回应slatepack信息,然后回复给发送者来完成交易。如果你使用GrinMail工具，则无需任何操作，自动回复。\n'\
              'Please copy and paste the slatepack message into the wallet, or submit the attachment to the wallet, get the response slatepack and reply to the sender to complete the transcation. if you use the GrinMail, you will reply automatically without any action.'
    send_mail(receiver,subject,content,slate_file)
    if not user.endswith('@gmail.com'):
        mail_id = server.get_latest()['id']
    slatepack2 = None
    while not slatepack2:
        time.sleep(20)
        if user.endswith('@gmail.com'):
            try:
                new_mail = server.get_latest()
            except:
                continue
            if 'slatepack2' in new_mail['subject']:
                slatepack2 = receive_mail(new_mail)
        else:
            new_mails = server.get_mails(start_index=mail_id + 1)
            if new_mails:
                for new_mail in new_mails:
                    if 'slatepack2' in new_mail['subject']:
                        slatepack2 = receive_mail(new_mail)
            else:
                continue
    logger.info('完结交易中...')
    result = wallet.finalize(slatepack2)
    if 'Transaction finalized successfully' in result:
        logger.info('已完结交易，成功提交上链')
    else:
        print(result)


if __name__ == '__main__':
    amount = float(sys.argv[2])
    receiver = sys.argv[1]
    config = configparser.ConfigParser()
    config.read('config.ini',encoding='utf-8')
    user = config.get('login','email')
    password = config.get('login','email_password')
    wallet_password = config.get('login','wallet_password')
    server = zmail.server(user,password)
    logging.basicConfig(level=logging.DEBUG,
    #filename='log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('GrinMail上线，开始运行...')
    main()
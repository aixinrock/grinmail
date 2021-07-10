import re
import logging
import time
import sys
import configparser

import pexpect
import zmail


def send(amount):
    child = pexpect.spawn('grin-wallet send ' + str(amount))
    child.expect('Password:')
    child.sendline(wallet_password)
    child.expect(pexpect.EOF)
    result = child.before.decode('utf-8')

    pattern = re.compile(r'/home.*?S1.slatepack')
    slate_file = re.search(pattern, result).group()
    logger.debug('Slatepack1已生成并存储在目录：%s',slate_file)

    return slate_file

def send_mail(receiver,slate_file):
    with open(slate_file,'r') as f:
        slatepack1 = f.read()
    
    mail = {'subject':'GrinMail 交易邮件（Grin trading mail）',
            'content_text':slatepack1,
            'attachments':slate_file,
    }
    server.send_mail(receiver,mail)
    logger.info('已发送GrinMail交易邮件，等待回复')

def receive_mail(mail_id):
    new_mails = server.get_mails(start_index=mail_id + 1)
    if new_mails:
        for new_mail in new_mails:
            logger.info('收到回复邮件 %s',new_mail['subject'])
            if new_mail['attachments']:
                if 'S2.slatepack' in new_mail['attachments'][0][0]:
                    slatepack2 = new_mail['attachments'][0][1].decode()
                    logger.debug('接收方回传的Slatepack2数据：%s',slatepack2)
                    return slatepack2
            else:
                pass

            try:
                mail_content = new_mail['content_text'][0]
            except:
                return
            if 'Slatepack2' in mail_content:
                pattern = re.compile(r'BEGINSLATEPACK.[\s\S]*?ENDSLATEPACK.')
                slatepack = re.search(pattern,mail_content).group()
                slatepack2 = ' '.join(slatepack.split())
                logger.debug('正文中匹配到的Slatepack2数据：%s',slatepack)
                return slatepack2
    
    return

def finalize(slatepack2):
    child = pexpect.spawn('grin-wallet finalize')
    child.expect('Password:')
    child.sendline(wallet_password)
    child.expect('message:')
    child.sendline(slatepack2)
    child.expect(pexpect.EOF)
    result = child.before.decode('utf-8')

    if 'Transaction finalized successfully' in result:
        logger.info('已完结交易，成功提交上链')
    else:
        print(result)

def main():
    logger.info('开始生成Slatepack1数据...')
    slate_file = send(amount)
    logger.info('发送Slatepack1数据到邮箱 %s',receiver)
    send_mail(receiver, slate_file)
    mail_id = server.get_latest()['id']
    slatepack2 = None
    while not slatepack2:
        time.sleep(60)
        slatepack2 = receive_mail(mail_id)
    logger.info('完结交易中...')
    finalize(slatepack2)


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
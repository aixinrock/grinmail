import time
import re
import logging
import configparser

import wexpect
import zmail


def terminal(slatepack):
    child = wexpect.spawn('grin-wallet receive -m')
    child.expect('Password:')
    wallet_password = config.get('login','wallet_password')
    child.sendline(wallet_password)
    child.expect('message:')
    child.sendline(slatepack)
    child.expect(wexpect.EOF)
    result = child.before

    pattern = re.compile(r'C.*?S2.slatepack')
    slate_file = re.search(pattern,result).group()
    with open(slate_file,'r') as f:
        slate2 = f.read()
    return (slate2,slate_file)


def get_slatepack(): 
    if new_mail['attachments']:
        if '.slatepack' in new_mail['attachments'][0][0]:
            slatepack = new_mail['attachments'][0][1].decode().replace('\n','')
            logger.debug('附件中匹配到slatepack数据：%s',slatepack)
            return slatepack

    try:
        mail_content = new_mail['content_text'][0]
        pattern = re.compile(r'BEGINSLATEPACK.[\s\S]*?ENDSLATEPACK.')
        slatepack = re.search(pattern,mail_content).group()
        slatepack = ' '.join(slatepack.split())
        logger.debug('正文中匹配到slatepack数据：%s',slatepack)
        return slatepack
    except:
        logger.info('正文和附件中均不含slatepack数据，此邮件不是Grin交易邮件。')
        return


def send_mail(sender,subject,content,slate_file):
    mail = {'subject':subject,
            'content_text':content,
            'attachments':slate_file,
    }
    try:
        server.send_mail(sender,mail)
    except:
        logger.info('由于网络原因，邮件未发送成功，60秒后重新发送。')
        time.sleep(60)
        send_mail(sender,subject,content,slate_file)


def receive_mail():
    logger.info('收到新邮件 "%s"',new_mail['subject'])
    slatepack = get_slatepack()
    if slatepack:
        logging.info('终端开始处理slatepack数据...')
        try:
            slate2,slate_file = terminal(slatepack)
        except:
            logging.info('Grin交易重复，或slatepack数据错误，请验证后再发！')
            return

        content = '收到你的Grin交易请求，生成回应slatepack2信息如下：\n'\
              'Received your Grin transaction request, slatepack2 message has been generated in response to you: \n'\
              '————————————————————————'\
              f'\n{slate2}\n'\
              '————————————————————————\n'\
              '请将以上信息复制粘贴到钱包，或将附件提交到钱包，来完结交易以提交上链。如果你使用GrinMail工具，则无需任何操作，自动回复。\n'\
              'Please copy and paste the slatepack message into the wallet, or submit the attachment to the wallet, finalize the transaction and submit the blockchain. if you use the GrinMail, you will reply automatically without any action.'
        subject = '[GrinMail] 请完结Grin交易（Finalize Grin slatepack2）'
        pattern = re.compile(r'<(.*?)>')
        sender = re.search(pattern,new_mail['from']).group(1)
        send_mail(sender,subject,content,slate_file)
        logger.info('回复Grin交易邮件成功，Bingo！')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini',encoding='utf-8')
    user = config.get('login','email')
    password = config.get('login','email_password')

    server = zmail.server(user,password)
    
    logging.basicConfig(level=logging.DEBUG,
    filename='log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('GrinMail上线，开始运行...')

    if not user.endswith('@gmail.com'):
        mail_id = server.get_latest()['id']
        logging.info('邮件ID获取成功，开始收取邮件')
            
    while True:
        time.sleep(20)
        if user.endswith('@gmail.com'):
            try:
                new_mail = server.get_latest()
            except:
                continue
            receive_mail()
        else:
            try:
                mails = server.get_mails(start_index=mail_id + 1)
            except:
                logging.info('网络原因断开，60秒后重试')
                time.sleep(60)
                continue
            if mails:
                logger.info('共收到 %s 封新邮件',len(mails))
                for new_mail in mails:
                    receive_mail()
                mail_id += len(mails)
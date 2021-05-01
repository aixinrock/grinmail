import time,pexpect,zmail,re,logging,configparser


def receive(slatepack):
    cli = pexpect.spawn('grin-wallet receive')
    cli.expect('Password:')
    grin_password = config.get('login','grin_password')
    cli.sendline(grin_password)
    cli.expect('message:')
    cli.sendline(slatepack)
    cli.expect(pexpect.EOF)
    result = cli.before.decode('utf-8')
    return result

def slate_message(result,sender):
    if 'Slatepack data follows' in result:
        pattern = re.compile(r'/home.*?S2.slatepack')
        slate_file = re.search(pattern,result).group()
        with open(slate_file,'r') as f:
            text = f.read()
        logger.info('已生成回应slatepack数据')
        subject = '回复你的slatepack信息，请完结交易'
        send_mail(sender,subject,text,slate_file)
    elif 'Transaction recieved and sent back to sender' in result:
        logger.info('此为TOR交易，自动完成交互任务。')
        subject = '已通过tor完成交易，请等待上链'
        text = subject
        send_mail(sender, subject, text)
    elif 'has already been received' in result:
        logger.info('此交易重复')
        subject = '交易已接收，请不要重复发送同一笔交易'
        text = subject
        send_mail(sender, subject, text)
    
def polling_mail(new_mail): 
    if new_mail['attachments']:
        if 'slatepack' in new_mail['attachments'][0][0]:
            slatepack = new_mail['attachments'][0][1].decode()
            return slatepack
        else:
            logger.info('附件中不含slatepack数据，开始检测正文内容...')
    try:
        mail_text = new_mail['content_text'][0]
        patt = re.compile(r'BEGINSLATEPACK.[\s\S]*?ENDSLATEPACK.')
        slatepack = re.search(patt,mail_text).group()
        slatepack = ' '.join(slatepack.split())
        return slatepack
    except:
        logger.info('正文中不含slatepack数据，此邮件不是grin交易邮件。')
        return

def send_mail(sender,subject,text,slate_file=None):
    mail = {'subject':subject,
            'content_text':text,
            'attachments':slate_file,
    }
    server.send_mail(sender,mail)
    logger.info('回复邮件成功，bingo！')

def main():
    try:
        new_mail = server.get_latest()
    except:
        return
    logger.info('收到一封新邮件 %s',new_mail['subject'])
    slatepack = polling_mail(new_mail)
    if slatepack:
        pattern = re.compile(r'<(.*?)>')
        sender = re.search(pattern,new_mail['from']).group(1)
        logging.info('开始处理slatepack数据...')
        result = receive(slatepack)
        slate_message(result, sender)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini',encoding='utf-8')
    user = config.get('login','email')
    password = config.get('login','email_password')
    server = zmail.server(user,password)
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('系统上线，开始运行')
    while True:
        main()
        time.sleep(10)
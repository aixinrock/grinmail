import time
import re
import logging
import configparser

import pexpect
import zmail

from wallet import GrinWallet

def terminal(slatepack):
    try:
        child = pexpect.spawn('grin-wallet receive')
        child.expect('Password:')
        wallet_password = config.get('login','wallet_password')
        child.sendline(wallet_password)
        child.expect('message:')
        child.sendline(slatepack)
        child.expect(pexpect.EOF)
        result = child.before.decode('utf-8')
    except:
        result = 'Slatepack data is wrong, please verify and resend.'
    logger.debug('终端返回结果：%s',result)

    return result

def handle_result(result):
    if 'Slatepack data follows' in result:
        pattern = re.compile(r'/home.*?S2.slatepack')
        slate_file = re.search(pattern,result).group()
        logger.debug('Slatepack2文件存储目录：%s',slate_file)
        with open(slate_file,'r') as f:
            text = f.read()
        logger.debug('生成回应Slatepack2数据：%s',text)
        logger.info('已生成回应Slatepack2数据')
        content = 'GrinMail交易邮件已收到，以下是生成回应的Slatepack2数据，'\
                  '你可以将其复制后直接粘贴进钱包，或者将附件下载提交到钱包，'\
                 f'以完结交易的方式提交上链。\n{text}'
        return (content,slate_file)

    elif 'Transaction recieved and sent back to sender' in result:
        logger.info('已通过TOR方式自动完成交互任务。')
        content = '你的Grin交易已通过Tor自动完成交互，请耐心等待区块确认以完成上链！'
        return (content,None)

    elif 'has already been received' in result:
        logger.info('此交易重复')
        content = '你之前提交的Grin交易已收到，请不要重复发送同一笔交易。'
        return (content,None)
    else:
        logger.info('Slatepack 数据错误')
        content = '对不起，你所发送的 Slatepack 数据有误，请检查验证或重新生成后再次发送。'
        return (content,None)

def polling_mail(new_mail): 
    if '古灵邮查询余额' in new_mail['subject'] or 'grinmail check balances' in new_mail['subject']:
        wallet_password = config.get('login','wallet_password')
        wallet = GrinWallet(wallet_password)
        total,confirmation,finalization,locked,spendable = wallet.info()
        content = f'''                 ____古灵币余额信息____

               总 资 产 ：  {total}
               可 花 费 ：  {spendable}
               上 链 中 ：  {confirmation}
               待 完 结 ：  {finalization}
               被 锁 定 ：  {locked}

                ____Grin Balances Info____

          Confirmed Total            : {total}
          Currently Spendable     : {spendable}
          Awaiting Confirmation : {confirmation}
          Awaiting Finalization    : {finalization}
          Locked by transaction  : {locked}
                
          '''
        send_mail(user,content,None)
        return
          
    if new_mail['attachments']:
        if 'slatepack' in new_mail['attachments'][0][0]:
            slatepack = new_mail['attachments'][0][1].decode()
            logger.debug('附件中收到的Slatepack1数据：%s',slatepack)
            return slatepack
        else:
            logger.info('附件中不含slatepack数据，开始检测正文内容...')

    try:
        mail_content = new_mail['content_text'][0]
        pattern = re.compile(r'BEGINSLATEPACK.[\s\S]*?ENDSLATEPACK.')
        slatepack = re.search(pattern,mail_content).group()
        slatepack = ' '.join(slatepack.split())
        logger.debug('正文中匹配到的Slatepack1数据：%s',slatepack)
        return slatepack
    except:
        logger.info('正文中不含slatepack数据，此邮件不是Grin交易邮件。')
        return

def send_mail(sender,content,slate_file):
    mail = {'subject':'GrinMail 交易邮件（Grin trading mail）',
            'content_text':content,
            'attachments':slate_file,
    }
    server.send_mail(sender,mail)
    logger.info('已回复GrinMail交易邮件，bingo！')

def receive_mail(new_mail):
    logger.info('收到一封新邮件 %s',new_mail['subject'])
    slatepack = polling_mail(new_mail)
    if slatepack:
        pattern = re.compile(r'<(.*?)>')
        sender = re.search(pattern,new_mail['from']).group(1)
        logging.info('终端开始处理Slatepack1数据...')
        result = terminal(slatepack)
        content,slate_file = handle_result(result)
        send_mail(sender,content,slate_file)

def main():
    if not user.endswith('@gmail.com'):
        mail_id = server.get_latest()['id']
    while True:
        time.sleep(20)
        if user.endswith('@gmail.com'):
            try:
                new_mail = server.get_latest()
            except:
                continue
            receive_mail(new_mail)
        else:
            mails = server.get_mails(start_index=mail_id + 1)
            if mails:
                logger.info('共收到 %s 封新邮件',len(mails))
                for new_mail in mails:
                    receive_mail(new_mail)
                mail_id += len(mails)


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

    main()
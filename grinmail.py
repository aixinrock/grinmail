import time
import re
import logging
import configparser

import zmail

from wallet import GrinWallet


def main():
    logger.info('收到新邮件 "%s"',new_mail['subject'])

    if '古灵邮查询余额' in new_mail['subject'] or 'grinmail check balances' in new_mail['subject']:
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
        subject = '[GrinMail] 古灵币余额信息（Grin Balances Info）'
        send_mail(user,subject,content,None)
        return
    slatepack = get_slatepack()
    if slatepack:
        if 'slatepack1' in new_mail['subject']:
            logging.info('标题中含有slatepack1关键字，这是一封Grin收币交易邮件')
            wallet_receive(slatepack)
            return
            
        if new_mail['attachments']:
            if 'S1.slatepack' in new_mail['attachments'][0][0]:
                logging.info('附件标题中含有S1关键字，这是一封Grin收币交易邮件')
                wallet_receive(slatepack)
                return
            
        logging.info('正文中含slatepack数据，将其当成slatepack1尝试receive收币...')
        result = wallet_receive(slatepack)
        if result:
            logging.info('此为Grin收币邮件，已成功回复回应邮件。')
            return
        logging.info('尝试将其当成slatepack2来finalize完结交易...')
        pass


def send_mail(sender,subject,content,slate_file):
    mail = {'subject':subject,
            'content_text':content,
            'attachments':slate_file,
    }
    server.send_mail(sender,mail)
    logger.info('已回复GrinMail邮件，bingo！')


def get_slatepack():
    if new_mail['attachments']:
        if '.slatepack' in new_mail['attachments'][0][0]:
            slatepack = new_mail['attachments'][0][1].decode()
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


def wallet_receive(slatepack):
    logging.info('终端开始处理slatepack数据...')
    try:
        slate2,slate_file = wallet.receive(slatepack)
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
    return '成功发送'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini',encoding='utf-8')
    user = config.get('login','email')
    password = config.get('login','email_password')
    wallet_password = config.get('login','wallet_password')
    
    wallet = GrinWallet(wallet_password)

    server = zmail.server(user,password)
    
    logging.basicConfig(level=logging.DEBUG,
    #filename='log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('GrinMail上线，开始运行...')

    if not user.endswith('@gmail.com'):
        mail_id = server.get_latest()['id']
    while True:
        time.sleep(20)
        if user.endswith('@gmail.com'):
            try:
                new_mail = server.get_latest()
            except:
                continue
            main()
        else:
            mails = server.get_mails(start_index=mail_id + 1)
            if mails:
                logger.info('共收到 %s 封新邮件',len(mails))
                for new_mail in mails:
                    main()
                mail_id += len(mails)
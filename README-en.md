# GrinMail
>A tool to receive Grin trading and send them back  automatically using the email system  

[中文介绍请戳这里](README.md)
## Introduction
The Grin trading is currently divided into two types: one is to send to the receiver directly through Tor, but both sides need to be online; the other is to use the slatepack, first the sender sends the slatepack to the receiver, and the receiver generates a response slatepack to the sender, then the sender submits it to the chain. The steps are more cumbersome, not as convenient as Bitcoin. So I figured out a way to simplify the steps as much as possible. The sender's operation is indispensable, can the receiver's operation be automated, without the need for a real person to receive or return the slatepack online? **GrinMail was born to solve this problem!!!**
## Principle
The sender sends an email to the recipient's mailbox with slatepack data(in the form of an attachment or copied into the body content). GrinMail will poll the mailbox to receive the email, find that there is slatepack data in the attachment or in the body content. The data is handed over to grin-wallet for processing, the response slatepack is generated and sent the email back to sender. The recipient can receive the coins automatically through the entire process, without having to be online,unless there is a bug(O(∩_∩)O maybe a lot (*^__^*) ).
## Configure
1. Linux system:  
Win will be supported in the next step, and Mac will wait for Grin to da moon.
2. Install grin-wallet and grin node:  
[Click to enter the official website to download](https://grin.mw/download), you can refer to the official website tutorial to install, initialize, create a new or import an existing wallet.
3. Enable Gmail POP3 and SMTP services:  
**Settings ——> Forwarding and POP/IMAP ——> POP download ——> Enable POP for mail that arrives from now on ——> Save Changes**  
4. Clone:  
`git clone git@github.com:aixinrock/grinmail.git`
## Operating
1. Configuration file  
Open config.ini, enter the emaill account, email password and Grin wallet password
2. Python Library  
`pip install -r requirements.txt`
3. Run  
`python3 grinmail.py`
## Useage
* Merchants/Stores/Third-party collection service
* To deposit on the exchange, need to bind it to the emaill of the user
* For lazy people who don't want to move their fingers
## Feedback
>Test email: kirwlauinshipd@gmail.com to accept small donations.  
Join the Telegram group to report bugs: t.me/grinmail  
Contact the developer: aixinrock@gmail.com
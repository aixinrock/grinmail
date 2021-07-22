# GrinMail new feature: one command send grins

GrinMail is a tool to receive coins automatically using the email system for Grin, I introduced it in the previous article, [please click here](README-en.md). According to @xiaojay 's suggestion, since the receipt of coins can be automatic, can send coins also reduce the operation steps, with just one command? After continuous hard work and exploration, I finally succeeded. This includes generating Slatpack message, sending it to the receiver's mailbox, waiting for a reply from the receiver, and receiving slatepack to finalize the transation. The entire process is automatically completed by the program. It no longer requires the user to click, copy, paste and other actions to minimize operations step. If the sender and receiver have installed GrinMail at the same time, then only one command from the sender is needed, others such as receive, finalize will be completed automatically, without manual work, greatly convenient for users. Now GrinMail becomes a terminal tool that can automatically receive coins and send coins with one command.

## Configure and useage
It requires Linux system, Python3 environment, official grin-wallet(modify the file *.grin/main/grin-wallet.toml* find the line: **check_node_api_http_addr = "http://gnode.goblinpool.cn:3413"** -this is the remote node of the Goblinpool), Enable email POP3 and SMTP services, clone the code and fill in the config.ini, then `cd ~/grinmail/` , finaly, you just simply type in the terminal:

`python3 send.py [email] [amount]`

[email] option is to fill in the recipient’s email address.
[amount] option is to fill in the amount of coins. For example, sending 1000 grins to grin@mw.com:

`python3 send.py grin@mw.com 1000`

That's it, you're done!

## Furture improve
GrinMail is currently running well on the Linux system, and the feature of automatic receive coins is also implemented in Win10 system, the next one command send grins can also be done in the Windowns. In general, the configuration environment is troublesome, the setup is cumbersome, not suitable for general users. In the furture, I will gradually improve in this area.

***Finally, thanks to @xiaojay and Goblinpool for their sponsorship and support!***
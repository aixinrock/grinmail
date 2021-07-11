# GrinMail (古灵邮)
>利用邮件系统自动接收Grin交易并回传的工具  

[English Introduction click here](README-en.md)

## 更新
2021.7.10 增加一键发币功能 [用法介绍](send.md)

2021.6.6 支持Windowns系统，直接运行如下代码:

`python3 grinmail-win.py`
## 简介
Grin交易方式目前分为两种：一种是直接通过Tor由发送方直接发给接收方，但是需要双方都在线；另一种是通过slatepack方式，先由发送方发送slatepack数据给接收方，接收方生成回应slatepack给发送方，再由发送方提交上链，步骤比较繁琐，没有比特币这种直接往地址上发币那样便捷。于是便想办法尽量使步骤简化，发送方操作必不可少，那么接收方的操作可不可以实现自动化呢，不需要真人在线接收或者回传slatepack数据呢？**GrinMail就是为了解决这个问题而诞生的！！！**
## 原理
发送方将带有slatepack数据（以附件形式或直接复制到正文内容中）的邮件发送到接收方的邮箱里，GrinMail会轮询邮箱接收到的邮件，发现附件中或正文内容中存在slatepack数据，便将数据交给grin-wallet处理，生成回应slatepack数据，发送给邮件发送者，发送方收到回应邮件即可上链提交。接收方全程自动化接收即可收币，不必亲自在线或上手操作，除非出现BUG（O(∩_∩)O哈哈~估计会不少(*^__^*) ）。
## 配置
1. Linux系统 or Win10系统：  
~~Mac等Grin 100美刀暴富了再说~~
2. 安装grin-wallet和grin node：  
[点击进入官网下载](https://grin.mw/download)，可参考官网教程安装、初始化、新建或导入已有钱包。
3. QQ邮箱开启POP3和SMTP服务：  
**设置 ——> 账户 ——> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 ——> 开启服务：POP3/SMTP服务 ——> 开启**  
*（需要手机发短信认证，获取授权码，填入配置文件email_password中）*
4. 克隆代码：  
`git clone https://github.com/aixinrock/grinmail.git`
## 操作
1. 配置文件  
点开config.ini，输入邮箱账号、邮箱授权码和Grin钱包密码（即在grin-wallet设置的密码）
2. Python依赖库  
`pip3 install -r requirements.txt`
3. 运行  
`python3 grinmail.py`
## 场景
* 商家/卖场/第三方自助收款服务
* 交易所充值自动化，只需跟用户注册的邮箱绑定即可
* 不想动手指的懒人福利套装
## 反馈
>问题bug反馈请加电报群组： http://t.me/grinmail
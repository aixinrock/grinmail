# GrinMail 一键发币功能用法

## 简单介绍
GrinMail 利用邮箱系统已经实现了自动收币功能，发币也可以通过邮箱系统来减少不必要的操作，一条命令即可完成。这其中包括生成Slatepack信息，发送到指定邮箱，等待邮箱回复，收到Slatepack进行完结交易等整个流程，依靠程序自动来完成，不再需要用户鼠标点击、复制、粘贴等动作，最大程度地减少操作步骤。

## 环境配置
1.Linux 系统

2.Python3 依赖库

`pip3 install -r requirements.txt`

3.grin-wallet 官方命令行钱包，如果不想更新全节点的话，可以直接修改目录.grin/main/grin-wallet.toml 文件中的check_node_api_http_addr = "http://gnode.goblinpool.cn:3413" ，此为哥布林矿池的远程节点。

4.开启邮箱的POP3和SMTP服务

5.克隆代码，点开config.ini，输入邮箱账号、邮箱授权码和Grin钱包密码（即在grin-wallet设置的密码），主要用到的是send.py文件。

## 用法说明
要使用一键发币功能，终端cd到grinmail目录下，格式如下：

`python3 send.py [email] [amount]`

[email]选项是填接收者的email地址,[amount]选项是填发币的数量，比如向10000@qq.com邮箱发送10000grin：

`python3 send.py 10000@qq.com 10000`

只需这一条命令，后续任务都会由程序自动完成。结合GrinMail自动收币功能，即可一键完成发币收币整个流程。

## 总结展望
GrinMail目前在Linux系统运行良好，自动收币功能在Win10也实现了，下一步一键发币功能也会在Windows系统完成。总的来说，配置环境比较麻烦，需要下载设置等较繁琐，不适合普通新手，未来会在这方面逐步改进。

**感谢@xiaojay大佬和goblinpool的赞助和支持！**

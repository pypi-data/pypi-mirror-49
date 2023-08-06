# python-sendmail


Python版邮件客户端。通过代理服务器发送邮件。

## 安装

```
pip install python-sendmail
```
    
## 安装的可执行程序

- pysendmail

## 程序帮助信息

```
D:\code\python-sendmail>pysendmail --help
Usage: pysendmail [OPTIONS] [CONTENT]

  通过代理服务器发送邮件。

  注意：

  如果命令行中没有提供邮件内容，则表示从STDIN中获取邮件内容。

Options:
  -f, --from-address TEXT  发件人，如：姓名 <name@example.com>、name@example.com。
                           [required]
  -t, --to-address TEXT    收件人，如：姓名 <name@example.com>、name@example.com。
                           [required]
  -s, --subject TEXT       邮箱主题。
  -a, --attach TEXT        邮件附件，可以使用多次。
  --html                   使用HTML格式。
  -e, --encoding TEXT      邮件内容编码格式，默认为UTF-8。
  -h, --host TEXT          邮箱代理服务器地址，默认为127.0.0.1。
  -p, --port INTEGER       邮箱代理服务器端口，默认为25。
  --ssl                    邮箱代理服务器要求使用ssl加密链接。
  -u, --user TEXT          邮箱代理服务器帐号，不提供则表示无需帐号认证。
  -P, --password TEXT      邮箱代理服务器密码，不提供则表示无需帐号认证。
  --help                   Show this message and exit.
```

## 使用案例


### 使用远程代理服务器，有认证，无附件

- 发件人：SENDER(sender@exmaple.com)
- 收件人：recipient@exmaple.com
- 主题：just a test mail
- 内容：just a test mail
- 服务器地址：stmp.example.com
- 服务器端口：465
- 是否使用ssl安全链接：是
- 帐号：sender@example.com
- 密码：senderPassword
- 附件：无

```
pysendmail -h stmp.example.com -p 465 --ssl -u sender@example.com -P senderPassword -f 'SENDER <sender@exmaple.com>' -t recipient@exmaple.com -s 'just a test mail' 'just a test mail'
```


### 使用本地代理服务器，无认证，有附件

- 发件人：sender@exmaple.com
- 收件人：recipient@exmaple.com
- 主题：just a test mail
- 内容：just a test mail
- 服务器地址：127.0.0.1
- 服务器端口：25
- 是否使用ssl安全链接：否
- 帐号：无认证
- 密码：无认证
- 附件：/path/to/attachment.pdf

```
pysendmail -f sender@exmaple.com -t recipient@exmaple.com -s 'just a test mail' -a /path/to/attachment.pdf 'just a test mail'
```
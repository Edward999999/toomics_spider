import urllib.request
import urllib
from http import cookiejar

# 定义登录地址
login_url = 'https://global.toomics.com'
# 定义登录所需要用的信息，如用户名、密码等，详见下图，使用urllib进行编码
login_data = urllib.urlencode({
    "name": 'fantimeng@gmail.com',
    "password": 'ti19905.8',
    "autologin": 1,
    "enter": "Sign in"})

# 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookiejar.CookieJar()  # 获取Cookiejar对象（存在本机的cookie消息）
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  # 自定义opener,并将opener跟CookieJar对象绑定
urllib.request.install_opener(opener)  # 安装opener,此后调用urlopen()时都会使用安装过的opener对象
response = opener.open(login_url, login_data).read()  # 访问登录页，自动带着cookie信息
print(response)  # 返回登陆后的页面源代码

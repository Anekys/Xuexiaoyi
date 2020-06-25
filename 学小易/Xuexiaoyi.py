import requests
def getanswer(text,token):                #一个简单的post请求获取答案内容
    if (token==False):
        return False
    headers={
        "Host":"app.51xuexiaoyi.com",
        "token":token,
        "device":"Auhqehd3s6Ml6mXky_5dV-Uv4zsdXeUYY7wKFktkH1ag",
        "platform":"android",
        "app-version": "1.0.6",
        "t":"1592904062239",
        "s":"e6a47dea8298225b1e9a9366bead8083",
        "content-type":"application/json;charset=utf-8",
        "accept-encoding":"gzip",
        "user-agent":"okhttp/3.11.0"
    }
    url="https://app.51xuexiaoyi.com/api/v1/searchQuestion?keyword="+text
    # data={"keyword":text}
    res = requests.post(url,headers=headers)
    # r=res.text.replace('%u',r'\\u').encode('utf-8').decode('unicode_escape')      #如果将返回值以文本形式显示本条语句可将usc2转为ansi编码进而正常显示文本内容
    r=res.json()        #返回的内容本身就是json
    if(r['code']==200):     #判断获取到的内容状态码是不是200(200代表着成功)
        #print(type(r['data']))
        return r['data']        #若成功则返回获取到的问题和答案(返回的类型是列表)
    else:
        return r['msg']         #若失败则返回错误信息
def outanswer(li):
    if isinstance(li,list):         #由于获取成功返回的是列表,所以这里先判断是不是列表进而得知是否成功
        for i in li:                #若成功,则可通过迭代的方式遍历列表
            print(" ")
            print('问题:')           #列表中的每个元素都是一个字典,这里通过格式化输出把字典里需要的内容输出
            print(i['q'])
            print(" ")              #输出空行为了看起来更方便
            print('答案:')
            print(i['a'])
            print(" ")
            print('*'*50)
    else:
        print(li)                   #若参数不为列表,则返回的是错误信息,所以这里可以打印错误信息
def login():                                                #登录函数(获取账号的token)
    username=input("请输入账号:")
    password=input("请输入密码:")
    url="https://app.51xuexiaoyi.com/api/v1/login?username="+username+"&password="+password
    headers={
        "Host":"app.51xuexiaoyi.com",
        "device":"Auhqehd3s6Ml6mXky_5dV-Uv4zsdXeUYY7wKFktkH1ag",
        "platform":"android",
        "app-version":"1.0.6",
        "t":"1593008524987",
        "s":"53029a76022a2f4a52c11f08a84759c0",
        "Content-Type":"application/json; charset=utf-8",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.11.0"
    }
    res=requests.post(url,headers=headers).json()
    if (res['code']==200):                                          #判断是否登录成功(获取到token)
        f=open('token.txt','w+')                                    #若成功,则储存在token.txt中,方便下次使用
        f.write(res['data']['api_token'])
        f.close()
        print("登陆成功!")
        return res['data']['api_token']
    else:
        return res['msg']
def main():
    print('Welcome to "学不易" 输入"exit"或点"x"即可退出')
    try:
        f=open('token.txt','w+')
        token=f.read()
        f.close()
        if(token==""):
            token=login()
    except:
        token=login()
    while True:
        questions=input("请输入题目:")
        if len(questions)>=6:
            res = getanswer(questions,token)
            outanswer(res)
        elif questions == 'exit':
            break
        else:
            print("题目必须大于6个字符")
    exit()
if __name__ == "__main__":
     main()




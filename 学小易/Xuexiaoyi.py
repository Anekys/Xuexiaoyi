import requests
def getanswer(text):                #一个简单的post请求获取答案内容
    headers={
        "Host":"app.51xuexiaoyi.com",
        "token":"你自己登录时的token",
        "device":"自己的device标识",
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
            print('问题:%s'%i['q'])           #列表中的每个元素都是一个字典,这里通过格式化输出把字典里需要的内容输出
            print(" ")
            print('答案:%s'%i['a'])
            print('*'*50)
    else:
        print(li)
def main():
    print('Welcome to "学不易" 输入"exit"或点"x"即可退出')     #程序运行逻辑

    while True:
        questions=input("请输入题目:")
        if len(questions)>=6:
            res = getanswer(questions)
            outanswer(res)
        elif questions == 'exit':
            break
        else:
            print("题目必须大于6个字符")
    exit()
if __name__ == "__main__":
     main()



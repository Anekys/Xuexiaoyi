import requests
import os
from aip import AipOcr
#这里调用了百度云智能大脑的图像识别API,以下三个Key均为调用API需要,可在你自己的百度云管理界面查询到
token=""                            #申明一个全局变量Token
APP_ID='16593668'                           #你的百度云APP_ID
APP_KEY='FhqfbBANUQ9H1Q1pj8tS97QH'          #你的百度云Key
SECRET_KEY='VtPljGlCiXym52xRmiZCoUNX4Z4dsmWT'   #你的百度云Secret_Key(老版本百度云的 Access Key)
client=AipOcr(APP_ID,APP_KEY,SECRET_KEY)
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
def login():            #调用API获取账号的token
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
    if (res['code']==200):
        f=open('token.txt','w+')
        f.write(res['data']['api_token'])
        f.close()
        print("登陆成功!")
        return res['data']['api_token']
    else:
        return res['msg']
def OCR(imagename):     #参数为图片文件路径,函数的功能为获取图片数据,并通过百度云的OCR文字识别提取出图片中的文字.
    with open(imagename, 'rb') as fp:
        image=fp.read()
        retlist=client.basicGeneral(image)
        text=""                                     #由于百度云的OCR识别将结果作为一个列表进行返回,所以这里通过for循环将列表迭代为一个文本
        for i in retlist['words_result']:
            text=text+i['words']
        return text
def Ocrmode():                          #OCR文字识别模式,可将题目截图到任意目录,输入图片绝对路径一键进行题目提取及答案获取的操作
    while True:
        print("请输入图片路径:")
        path=input("ocrmode>>>")
        if(os.path.exists(path)):           #检测图片是否存在,若存在,则进行文字识别并查询答案
            text=OCR(path)
            res=getanswer(text,token)
            outanswer(res)
        elif path=="exocr" or "EXOCR":
            return
        else:
            print("图片不存在或没有访问权限!")

def main():
    print('Welcome to "学不易" 输入"exit"或点"x"即可退出')
    print('直接输入题目即可获取答案,也可输入"OCR"进入图片识别模式')
    try:
        f=open('token.txt','r+')
        token=f.read()
        f.close()
        if(token==""):
            token=login()
            print("这里是空")
    except:
        token=login()
    while True:
        questions=input(">>>")
        if len(questions)>=6:
            res = getanswer(questions,token)
            outanswer(res)
        elif questions == 'exit':
            break
        elif questions=="ocr" or "OCR":
            Ocrmode()
        else:
            print("题目必须大于6个字符")
    exit()
if __name__ == "__main__":
     main()
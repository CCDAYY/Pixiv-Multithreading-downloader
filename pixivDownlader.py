import random
import dateutil.utils
import requests
import re
import time
from tqdm import  tqdm
import os

import datetime
save_path = ""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/',
    # change cookie!
    'cookie' :' '
}
def download(id, count):
    global save_path
    url = 'https://www.pixiv.net/artworks/%d' % id
    res = requests.get(url, headers=headers)
    pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
    pic_name = re.findall(r'"illustTitle":"(.+?)"', res.text)[0]
    # 获取后缀
    extension = re.findall(r'....$', pic_url)[0]
    pic_url = re.sub('.....$','',pic_url)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', pic_name) != None:
        pic_name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', '', pic_name)

    # 下载图片
    for i in range(0,int(count)):
        url = pic_url+str(i)+extension
        #print('正在下载id为：%d的第%d张图片'%(id,i+1),end='   ')
        pic = requests.get(url, headers=headers,stream=True)
        total = int(pic.headers.get('content-length', 0))
        pic_url = (save_path + '\%s%d%s') % (pic_name, i+1, extension) # change path
        with  open(pic_url, 'wb') as f, tqdm(
                desc=pic_url,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                position=0,
                leave=False
        ) as bar:
            for data in pic.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
        pic_url = re.sub('.....$', '', pic_url)
def trending():
    id = []
    count = []
    for i in range(1, 2):
        url = 'https://www.pixiv.net/ranking.php?p=%d&format=json' % i
        res = requests.get(url, headers=headers)
        id = id + re.findall('"illust_id":(\d+)', res.text)
        count = count + re.findall('"illust_page_count":"(\d+)"', res.text)
    if len(id) == len(count):
        for i in tqdm(range(0, len(id)),desc="downloading",unit="pic",position=0):
            download(int(id[i]), int(count[i]))
            time.sleep(0.01)

def getids():
    global save_path
    id=[]
    name= input("what you want to search:\n->")
    page = int(input("what page you choose(may have mult pages):\n->"))

    url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, page)
    res = requests.get(url, headers=headers)
    id = id + re.findall(r'"id":"(.+?)"', res.text)
    if len(id)==0:
        return False
    save_path = str(".\ ")[:2] + name
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)
    rtes = []
    for i in range(len(id)):
        if len(id[i]) > 9:
            print(id[i])
        else:
            rtes.append(id[i])
    for x in tqdm(range(len(rtes)),desc="downloading",unit="pic",position=0):
        r = random.randrange(0,2)
        download(int(rtes[x]),1)
        #time.sleep(r)
    #getids(name,page+1)
#name =搜索的关键词
#page = 第几页
def changer():
    global save_path
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))
    id=[]
    rtes = []
    likes = str(likes)+"users"
    url = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'.format(sname,likes,sname,likes)
    res = requests.get(url, headers=headers)
    id = id + re.findall(r'"id":"(.+?)"', res.text)
    if len(id) == 0:
        return False
    save_path = str(".\ ")[:2] + sname
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)
    for i in range(len(id)):
        if len(id[i]) > 9:
            pass
        else:
            rtes.append(id[i])
    print(len(rtes),"pictures")
    for x in tqdm(range(len(rtes)),desc="downloading",unit="pic",position=0):
        download(int(rtes[x]), 1)
        time.sleep(0.01)
def cos(n):
    global save_path
    if n ==1:# search with ranking

        b = (changer())
        if b:
            print("finished")
        else:
            print("no pictures found")
    if n ==2 : #trending
        day = dateutil.utils.today()
        dd = day.strftime('%d') + day.strftime('%b')
        save_path = str(".\_trending%s") %(dd)
        if os.path.exists(save_path) == True:
            pass
        else:
            os.mkdir(save_path)
        trending()

    if n == 3:
        a=(getids())
        if a:
            print("finished")
        else:
            print("no pictures found")

cos(int(input("1:(searching with rank ) 2:(daily trending mode), 3:(normal searching)\n->")))



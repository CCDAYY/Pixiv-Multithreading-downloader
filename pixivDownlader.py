import random
import dateutil.utils
import requests
import re
import time
from tqdm import  tqdm
import os
save_path = ""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/',
    # change cookie!
    'cookie' :'first_visit_datetime_pc=2022-07-06+12%3A31%3A34; yuid_b=Y3l3JyA; p_ab_id=9; p_ab_id_2=7; p_ab_d_id=70900205; c_type=25; privacy_policy_notification=0; a_type=1; b_type=1; login_ever=yes; privacy_policy_agreement=5; _fbp=fb.1.1659843712837.595619200; _gcl_au=1.1.862064737.1667556191; PHPSESSID=52047359_e3gMlROeZGrEuxqHzdsut0PJVhbfcjfM; device_token=c3d4b67bed3141e3982fa9bc29b18943; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; __cf_bm=Burdid_KvyU8YFG33q92u_33gThKu_UoI1.sIdS1l3Y-1668134383-0-Ab63mpah8azxLXJ8QpB5sa76ETjJVMS3oKrHj77XbfWSjtbIqCwsMvPE1P9bz/jzogp6aHj9KyoFm/c+wawQKie0p3lVt3ed5PhB0Y6v5qnvZBRcYDEvx09R6tQ0+/eF2eDMqX5ij/lHCGA0UWkLfwglRfH3JflFYpZIZ3OC1VpEXPjH/9AKvlaUIh+qOJ4gQQ==; _gid=GA1.2.276021848.1668134391; tag_view_ranking=B6uEbiYg7i~CluIvy4vsU~jYh2eZgGpA~_EOd7bsGyl~uusOs0ipBx~RTJMXD26Ak~jhuUT0OJva~fHzsW6IqUG~yRoNh0Qhm9~ziiAzr_h04~9ODMAZ0ebV~Lt-oEicbBr~LJo91uBPz4~AauDVIJZFs~ubfcowqpt0~zbkuXp-SeA~OTwy05NHTP~lkoWqucyTw~VyMzgidqJ2~o7hvUrSGDN~Wxk4MkYNNf~QliAD3l3jr~HKacS-D5BU~MKnVucuYOn~e2yEFDVXjZ~Ie2c51_4Sp~cb-9gnu4GK~MnGbHeuS94~mkdwargRR2~JrQgdjRZtN~LF9kqwfMs-~dI30gMiyFa~qDi7263PSz~1G1bsV2xcg~CMvJQbTsDH~tlXeaI4KBb~mLrrjwTHBm~47Y4K-mkZp~UC88m8Ncjp~R6781hHvcD~LtqwLKiXpU~S6OJ9uijaS~rc-tS2ndS_~hVuZfaQFy1~ACntaietug~xSHgVV_CZp~0zADS3mWo2~mz8TBIAkOD~0HfyRN74pw~-JElyH-DNN~fidt6AhIsl~4Y3V8ANC-b~WM3631l9jF~spPqEvHEF2~lJoTN1o2SZ~1MsYTGMqRa~QTp6AjCbvf~qtVr8SCFs5~jm40SVtdHx~N9g3b-m0G9~VlPGsfUYUq~C8c7zUdH1w~zKLqKSPEAG~1s4b4irzBH~e2syg_rHyV~59dAqNEUGJ~P8OX_Lzc1b~GicHBP_mt1~7TL10-HUQU~nhidBJEVl0~D6xAR9Wod9~9LhLC1Kxwa~az4Twa7Ghs~gOsOYSdg91~Bzyu1zjric~OqRhcPLny7~HOW72W2vi2~T1etFHYy1i~pnCQRVigpy~uW5495Nhg-~d_xJYFN472~eoZbvaNuhK~P8_hhAfbil~2870udwj0N~WbBWp_OUQ1~T9evV3tl5m~mEXH62aTbl~eTX0s8V6Tb~Xxky0ZAyIM~E2xZO-a_vM~gxGILk9xEc~BX9ZK9kJFw~cyc7E50MAG~n3GBuX-EM5~yroC1pdUO-~ZQJ8wXoTHu~xF0JX9eOwX~npWJIbJroU~GfzIxzFqfY~DxQj_Ks20P; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1668134381.33.1.1668134591.0.0.0; _ga=GA1.1.390407410.1659769130'
}
def download(id, count):
    global save_path
    url = 'https://www.pixiv.net/artworks/%d' % id
    res = requests.get(url, headers=headers)
    pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
    print(pic_url,"download picurl ")
    pic_name = re.findall(r'"illustTitle":"(.+?)"', res.text)[0]
    print(pic_name, "download pic_name ")
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
        pic_url = (save_path + '\%s%d%s%s') % (pic_name, i+1,'_'+str(id), extension) # change path
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

def NormalS():
    global save_path
    id=[]
    name= input("what you want to search:\n->")
    page = 1
    url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, page)
    #print(url)
    total = getTotal(url)
    #print(str(total)+" pages found!")
    dettt = int(input("type 1 search specific pages, or type 2 search a range pages, type 3 download all pages:"))

    if dettt==1:
        det = int(input("how many pages you want to download"))
        id= M_Pid_search(det,0,1,name)
    elif dettt==2:
        star = int(input("start from which pages?:"))
        end = int(input("start from which pages?:"))

        id = M_Pid_search(star,end,2,name)
    elif dettt==3:
        for x in range(total):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, x+1)
            print(k)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(0, 5))
    else:
        return False

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
          pass
        else:
            rtes.append(id[i])
    rest = 0
    for x in tqdm(range(len(rtes)),desc="downloading",unit="pic",position=0):

        download(int(rtes[x]),1)
        time.sleep(random.randrange(0,3))
        rest+=1
        if(rest>50):
            print("rest for 10 second")
            time.sleep(10)
            rest = 0

    #getids(name,page+1)
#name =搜索的关键词
#page = 第几页
def changer():
    global save_path
    #total = 0
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))
    id=[]
    rtes = []
    likes = str(likes)+"users"
    page = 1
    url = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(sname,likes,sname,likes,page)
    total = getTotal(url)
    for x in range(total):
        k = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(
            sname, likes, sname, likes, x + 1)
        res = requests.get(k, headers=headers)
        id = id + re.findall(r'"id":"(.+?)"', res.text)


    if len(id) == 0:
        return False
    n_Num = sname + str(likes)
    save_path = str(".\ ")[:2] + n_Num

    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)

    for i in range(len(id)):
        if len(id[i]) > 9:
            pass
        else:
            rtes.append(id[i])
    print(len(id),"pictures")
    for x in tqdm(range(len(rtes)),desc="downloading",unit="pic",position=0):
        download(int(rtes[x]), 1)
        time.sleep(0.01)
def getTotal(url):
    res= requests.get(url,headers=headers)
    total = re.findall(r'"total":(.+?),', res.text)
    print(total,"gettotal")
    page = 1
    ct= int(total[0])
    if ct > 60:
        page += int(ct / 60)
        return page
    else:
        return 1
def M_Pid_search(num,end,mode,name):
    id =[]
    if mode ==1:
        for x in range(num):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, x+1)
            print(k)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(0, 5))
        return id
    elif mode==2:
        for x in range(num,end+1):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, x+1)
            print(k)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(0, 5))
        return id

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
        a=(NormalS())
        if a:
            print("finished")
        else:
            print("no pictures found")
#download(101821127,3)
cos(int(input("1:(searching with rank ) 2:(daily trending mode), 3:(normal searching)\n->")))



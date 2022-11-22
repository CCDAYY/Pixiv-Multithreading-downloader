import random
import dateutil.utils
import requests
import re
import time
from tqdm import  tqdm
import os
save_path = ""

c_k = input("type y to change cookies->")
cook = "first_visit_datetime_pc=2021-09-02+23%3A43%3A13; p_ab_id=3; p_ab_id_2=6; p_ab_d_id=1362319497; yuid_b=N0F1eBc; privacy_policy_notification=0; b_type=1; ki_r=; login_ever=yes; ki_s=214908%3A0.0.0.0.2%3B214994%3A0.0.0.0.2%3B215190%3A0.0.0.0.2%3B219376%3A0.0.0.0.2%3B221691%3A0.0.0.0.2; ki_t=1632313976963%3B1640175147711%3B1640175165221%3B5%3B49; c_type=25; a_type=1; privacy_policy_agreement=5; _gcl_au=1.1.1543749531.1664107948; device_token=a9b76dd3d13a3deb263669b9715aadcf; first_visit_datetime=2022-11-03+18%3A26%3A00; PHPSESSID=52047359_GX3stRHI2353liHSwVNL08254B5edAc3; _ga_MZ1NL4PHH0=GS1.1.1667521370.6.0.1667521370.0.0.0; tag_view_ranking=_EOd7bsGyl~lkoWqucyTw~uusOs0ipBx~ziiAzr_h04~jhuUT0OJva~ZNRc-RnkNl~B6uEbiYg7i~CluIvy4vsU~fHzsW6IqUG~RTJMXD26Ak~mkdwargRR2~_hSAdpN9rx~yTWt5hzG4w~P8OX_Lzc1b~qDi7263PSz~dI30gMiyFa~pzZvureUki~q1r4Vd8vYK~CbkyggmWCV~nWC-P2-9TI~ZPjQtvhTg3~UotTWDag3B~mLrrjwTHBm~9Gbahmahac~6293srEnwa~MnGbHeuS94~RgJEiMBANx~_wgwZ79S9p~bv3Hjql-Z1~Ie2c51_4Sp~9dh32MPwDj~Lt-oEicbBr~JL8rvDh62i~JrQgdjRZtN~Bzyu1zjric~EUwzYuPRbU~QliAD3l3jr~w8ffkPoJ_S~K8esoIs2eW~P-Zsw0n2vU~pzzjRSV6ZO~LJo91uBPz4~q3eUobDMJW~bq1HPY2wZ-~pnCQRVigpy~rOnsP2Q5UN~CHzc3gIECp~hZzvvipTPD~TqiZfKmSCg~faZX-CfhYv~yREQ8PVGHN~1s4b4irzBH~QIc0RHSvtN~hW_oUTwHGx~BSlt10mdnm~OUqETMPW2Z~YbOo-qnBCR~aTW6kYb0Ak~IsJjJpzDo3~83nP16VbYh~Thyk9saBEx~0IB1cxSXTq~2V0-EgyHVg~CLEmkBaAcu~BOHDnbK1si~FuSOTTQp_1~PiKFMvIHS1~xF0JX9eOwX~BC84tpS1K_~6ImQE2rhA3~jH0uD88V6F~ETjPkL0e6r~v-OL0-Ncw6~jk9IzfjZ6n~D6xAR9Wod9~KvAGITxIxH~YvAixcnlGi~t1Am7AQCDs~sAwDH104z0~IBgoeiGDSP~CMvJQbTsDH~LRbdzYYhoA~RDY8AkVSDu~oCqKGRNl20~j2lJ8_51Vq~npWJIbJroU~Sgh7s9dZ-K~_AKBg0O8RH~8NU7YH_PAG~59dAqNEUGJ~e9EFq9kkOU~08iLUivxxM~Q4duCCWLbW~0zADS3mWo2~mz8TBIAkOD~OTwy05NHTP~gGjtVdrrFe~NE-E8kJhx6~ZMIwqQI05A~zeOOAJeQjD; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.759326914.1668594580; __cf_bm=LnXXQnjlxs_eClL7mldyr7_34_xU8d3qude8sSWNUFw-1668595597-0-AZkBIqAxiw9NlWYOyx2e2GXKPrFR5MJqxdvLUGT3wioSvzBHjDohnSOTs6VHQ2lUQRie5ZFamW8HzQE2JaYavFSZSUoHJtej01qfQEf1keDuzAcHKb5CPG5wswRXbR5dmBFPSuv+ixfg1CZcegEYgWOTfqpJSilTme0rUhyEU/wdy/ntCs5rtnEi9JivztazmA==; _ga_75BBYNYN9J=GS1.1.1668594574.46.1.1668595597.0.0.0; _ga=GA1.2.1138408233.1634023850; _gat_UA-1830249-3=1"
if c_k =="y":
    cook = input("new cookiee->")
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/',
    # change cookie!
    'cookie' : cook
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
        print("download id:" + str(id) )
        pic = requests.get(url, headers=headers,stream=True)
        total = int(pic.headers.get('content-length', 0))
        pic_url = (save_path + '/%s%d%s%s') % (pic_name, i+1,'_'+str(id), extension) # change path
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

            try:
                download(int(id[i]), int(count[i]))
            except:
                time.sleep(0.01)
                download(int(id[i]), int(count[i]))


def NormalS():
    global save_path
    id=[]
    name= input("what you want to search:\n->")
    page = 1
    url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, page)
    total = getTotal(url)
    print(str(total)+" pages found!")
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
            print("getting ids pls wait")
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, x+1)
            res = requests.get(k, headers=headers)
            print(k)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(2, 5))
    else:
        return False

    if len(id)==0:
        return False
    new = []
    for x in range(len(id)):
        if len(id[x]) > 9:
            pass
        else:
             new.append(id[x])
    id = new
    ## create file
    save_path = str("./ ")[:2] + name
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)

    iddownloader(id)

def changer():
    global save_path
    #total = 0
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))
    id=[]
    rtes = []
    likes = str(likes)+"users"
    page = 1

    n_Num = sname + str(likes)
    save_path = str("./ ")[:2] + n_Num
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)

    url = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(sname,likes,sname,likes,page)
    total = getTotal(url)
    print(str(total)+" pages found!")
    a = input("press y to start download")
    if a == "y":
        for i in range(total):
            id = getpageids(sname,likes,1)
            if len(id) == 0:
                return False
            else:
                iddownloader(id)
    else:
        pass
def iddownloader(id):
    isDown = []
    for i in range(len(id)):
        isDown.append(True)

    for x in tqdm(range(len(id)),desc="Downloading",unit="pic",position=0,leave=False):
        try:
            randomid = random.randrange(0,len(id))
            if isDown[randomid] :
                download(int(id[randomid]),1)
                isDown[randomid]= False
            time.sleep(random.randrange(0,3))
        except:
            print("fail download id :"+id[x])
            time.sleep(10)
            download(int(id[x]), 1)

def getpageids(sname,likes,total):
    id = []
    new = []
    for x in range(total):
        k = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(sname, likes, sname, likes, x + 1)
        res = requests.get(k, headers=headers)
        id = id + re.findall(r'"id":"(.+?)"', res.text)
        time.sleep(3)
    for x in range(len(id)):
        if len(id[x]) > 9:
            pass
        else:
            new.append(id[x])
    id = new

    return id


def getTotal(url):
    res= requests.get(url,headers=headers)
    total = re.findall(r'"total":(.+?),', res.text)
    print(total,"images found")
    page = 1
    ct= int(total[0])
    if ct > 60:
        page += int(ct / 60)
        return page
    else:
        return 1
def M_Pid_search(num,end,mode,name):
    id =[]
    print("getting ids pls wait for a while")
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
            #print(k)
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
        save_path = str("./_trending%s") %(dd)
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

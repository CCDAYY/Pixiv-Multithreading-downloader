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
    'cookie' :'first_visit_datetime_pc=2021-09-02+23%3A43%3A13; p_ab_id=3; p_ab_id_2=6; p_ab_d_id=1362319497; yuid_b=N0F1eBc; privacy_policy_notification=0; b_type=1; ki_r=; login_ever=yes; ki_s=214908%3A0.0.0.0.2%3B214994%3A0.0.0.0.2%3B215190%3A0.0.0.0.2%3B219376%3A0.0.0.0.2%3B221691%3A0.0.0.0.2; ki_t=1632313976963%3B1640175147711%3B1640175165221%3B5%3B49; c_type=25; a_type=1; privacy_policy_agreement=5; _gcl_au=1.1.1543749531.1664107948; device_token=a9b76dd3d13a3deb263669b9715aadcf; _gid=GA1.2.475150194.1667211960; PHPSESSID=52047359_hjqQhxsmEMiOjNibxuSOdy93puSUu1DA; _ga_MZ1NL4PHH0=GS1.1.1667295085.4.1.1667297203.0.0.0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; tag_view_ranking=_EOd7bsGyl~lkoWqucyTw~uusOs0ipBx~ziiAzr_h04~jhuUT0OJva~ZNRc-RnkNl~B6uEbiYg7i~CluIvy4vsU~fHzsW6IqUG~mkdwargRR2~RTJMXD26Ak~yTWt5hzG4w~P8OX_Lzc1b~qDi7263PSz~dI30gMiyFa~q1r4Vd8vYK~CbkyggmWCV~pzZvureUki~_hSAdpN9rx~nWC-P2-9TI~ZPjQtvhTg3~UotTWDag3B~9Gbahmahac~6293srEnwa~mLrrjwTHBm~_wgwZ79S9p~bv3Hjql-Z1~Ie2c51_4Sp~9dh32MPwDj~Lt-oEicbBr~RgJEiMBANx~MnGbHeuS94~JrQgdjRZtN~Bzyu1zjric~EUwzYuPRbU~QliAD3l3jr~w8ffkPoJ_S~K8esoIs2eW~P-Zsw0n2vU~pzzjRSV6ZO~LJo91uBPz4~q3eUobDMJW~bq1HPY2wZ-~pnCQRVigpy~rOnsP2Q5UN~CHzc3gIECp~hZzvvipTPD~yREQ8PVGHN~1s4b4irzBH~QIc0RHSvtN~hW_oUTwHGx~BSlt10mdnm~OUqETMPW2Z~YbOo-qnBCR~aTW6kYb0Ak~IsJjJpzDo3~83nP16VbYh~Thyk9saBEx~0IB1cxSXTq~2V0-EgyHVg~CLEmkBaAcu~BOHDnbK1si~FuSOTTQp_1~PiKFMvIHS1~ETjPkL0e6r~v-OL0-Ncw6~jk9IzfjZ6n~TqiZfKmSCg~D6xAR9Wod9~KvAGITxIxH~YvAixcnlGi~JL8rvDh62i~t1Am7AQCDs~sAwDH104z0~IBgoeiGDSP~CMvJQbTsDH~LRbdzYYhoA~RDY8AkVSDu~oCqKGRNl20~j2lJ8_51Vq~npWJIbJroU~Sgh7s9dZ-K~_AKBg0O8RH~8NU7YH_PAG~59dAqNEUGJ~e9EFq9kkOU~08iLUivxxM~Q4duCCWLbW~0zADS3mWo2~mz8TBIAkOD~OTwy05NHTP~gGjtVdrrFe~NE-E8kJhx6~ZMIwqQI05A~zeOOAJeQjD~gLsOxE-l0I~yc2ONDWbV-~-djhIhdgci~sJh6R-X25I~faZX-CfhYv; _ga_75BBYNYN9J=GS1.1.1667460064.37.0.1667460064.0.0.0; _ga=GA1.2.1138408233.1634023850; _gat_UA-1830249-3=1; __cf_bm=Akt3kTCzIgYCxzL9zDvOjlnG3QoJRBlo2jBWRX9XBck-1667460065-0-AUk0QWVewfDKNSNaaBZm3r0ZNoI/LHdnanl3Uad4i5o52YIGA8W/yUMvbD+63MgJkgaeRj+twY5dTGnfZtkSHp2/KSfijRj/kLTw6H5JBzQK5OUEpM0vvXA3Kztxt95v2RuK45vj8h5RlLk0kolyHzrdUH1n6ne153iprxCr6G9VNInu+24IFQ4gSNG7zKyJLg=='
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



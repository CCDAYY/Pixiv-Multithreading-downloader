import os
import random
import re
import time
from threading import  Thread
import dateutil.utils
import requests
from tqdm import tqdm
import ast

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    TextColumn
)
progress_d = Progress(
    TextColumn("[progress.description]{task.description}"),
    TaskProgressColumn(),
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
)
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    #2transient=True

)
save_path = ""
# c_k = input("type y to change cookies->")
cook = "first_visit_datetime_pc=2021-09-02+23%3A43%3A13; p_ab_id=3; p_ab_id_2=6; p_ab_d_id=1362319497; yuid_b=N0F1eBc; privacy_policy_notification=0; b_type=1; ki_r=; login_ever=yes; ki_s=214908%3A0.0.0.0.2%3B214994%3A0.0.0.0.2%3B215190%3A0.0.0.0.2%3B219376%3A0.0.0.0.2%3B221691%3A0.0.0.0.2; ki_t=1632313976963%3B1640175147711%3B1640175165221%3B5%3B49; c_type=25; a_type=1; privacy_policy_agreement=5; _gcl_au=1.1.1543749531.1664107948; device_token=a9b76dd3d13a3deb263669b9715aadcf; first_visit_datetime=2022-11-03+18%3A26%3A00; PHPSESSID=52047359_GX3stRHI2353liHSwVNL08254B5edAc3; _ga_MZ1NL4PHH0=GS1.1.1667521370.6.0.1667521370.0.0.0; tag_view_ranking=_EOd7bsGyl~lkoWqucyTw~uusOs0ipBx~ziiAzr_h04~jhuUT0OJva~ZNRc-RnkNl~B6uEbiYg7i~CluIvy4vsU~fHzsW6IqUG~RTJMXD26Ak~mkdwargRR2~_hSAdpN9rx~yTWt5hzG4w~P8OX_Lzc1b~qDi7263PSz~dI30gMiyFa~pzZvureUki~q1r4Vd8vYK~CbkyggmWCV~nWC-P2-9TI~ZPjQtvhTg3~UotTWDag3B~mLrrjwTHBm~9Gbahmahac~6293srEnwa~MnGbHeuS94~RgJEiMBANx~_wgwZ79S9p~bv3Hjql-Z1~Ie2c51_4Sp~9dh32MPwDj~Lt-oEicbBr~JL8rvDh62i~JrQgdjRZtN~Bzyu1zjric~EUwzYuPRbU~QliAD3l3jr~w8ffkPoJ_S~K8esoIs2eW~P-Zsw0n2vU~pzzjRSV6ZO~LJo91uBPz4~q3eUobDMJW~bq1HPY2wZ-~pnCQRVigpy~rOnsP2Q5UN~CHzc3gIECp~hZzvvipTPD~TqiZfKmSCg~faZX-CfhYv~yREQ8PVGHN~1s4b4irzBH~QIc0RHSvtN~hW_oUTwHGx~BSlt10mdnm~OUqETMPW2Z~YbOo-qnBCR~aTW6kYb0Ak~IsJjJpzDo3~83nP16VbYh~Thyk9saBEx~0IB1cxSXTq~2V0-EgyHVg~CLEmkBaAcu~BOHDnbK1si~FuSOTTQp_1~PiKFMvIHS1~xF0JX9eOwX~BC84tpS1K_~6ImQE2rhA3~jH0uD88V6F~ETjPkL0e6r~v-OL0-Ncw6~jk9IzfjZ6n~D6xAR9Wod9~KvAGITxIxH~YvAixcnlGi~t1Am7AQCDs~sAwDH104z0~IBgoeiGDSP~CMvJQbTsDH~LRbdzYYhoA~RDY8AkVSDu~oCqKGRNl20~j2lJ8_51Vq~npWJIbJroU~Sgh7s9dZ-K~_AKBg0O8RH~8NU7YH_PAG~59dAqNEUGJ~e9EFq9kkOU~08iLUivxxM~Q4duCCWLbW~0zADS3mWo2~mz8TBIAkOD~OTwy05NHTP~gGjtVdrrFe~NE-E8kJhx6~ZMIwqQI05A~zeOOAJeQjD; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.759326914.1668594580; __cf_bm=LnXXQnjlxs_eClL7mldyr7_34_xU8d3qude8sSWNUFw-1668595597-0-AZkBIqAxiw9NlWYOyx2e2GXKPrFR5MJqxdvLUGT3wioSvzBHjDohnSOTs6VHQ2lUQRie5ZFamW8HzQE2JaYavFSZSUoHJtej01qfQEf1keDuzAcHKb5CPG5wswRXbR5dmBFPSuv+ixfg1CZcegEYgWOTfqpJSilTme0rUhyEU/wdy/ntCs5rtnEi9JivztazmA==; _ga_75BBYNYN9J=GS1.1.1668594574.46.1.1668595597.0.0.0; _ga=GA1.2.1138408233.1634023850; _gat_UA-1830249-3=1"
# if c_k =="y":
# cook = input("new cookiee->")
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/',
    # change cookie!
    'cookie': cook
}
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.google.com/',
}





def download(id, count):
    global save_path
    url = 'https://www.pixiv.net/artworks/%d' % id
    res = requests.get(url, headers=headers)
    pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
    '''
    r = open("request.txt","a",encoding='utf-8')
    r.write(str(res.text))
    r.close()
    '''
    pic_name = re.findall(r'"illustTitle":"(.+?)"', res.text)[0]
    # 获取后缀
    extension = re.findall(r'....$', pic_url)[0]
    pic_url = re.sub('.....$', '', pic_url)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', pic_name) != None:
        pic_name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', '', pic_name)

    ################################  proxy stuffs
    for i in range(0, int(count)):
        url = pic_url + str(i) + extension
        if is_use_proxy:
            c = getRandomIp()
            prox = {"http": "http" + "://" + c,}
        else:
            prox = None
    ################################

    for i in range(0, int(count)):
        url = pic_url + str(i) + extension
        print("download id:" + str(id))
        pic = requests.get(url, headers=headers, stream=True,proxies=prox)
        total = int(pic.headers.get('content-length', 0))
        pic_url = (save_path + '/%s%d%s%s') % (pic_name, i + 1, '_' + str(id), extension)  # change path
        with  open(pic_url, 'wb') as f:
            f.write(pic.content)
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
        for i in tqdm(range(0, len(id)), desc="downloading", unit="pic", position=0):

            try:
                download(int(id[i]), int(count[i]))
            except:
                time.sleep(0.1)
                download(int(id[i]), int(count[i]))


def NormalS():
    global save_path

    name = input("what you want to search:\n->")
    page = 1
    mode = 0
    start = 0
    end = 0
    tpage = 0

    url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(
        name, name, page)
    total = getTotalPage(url)
    print(str(total) + " pages found!")
    dettt = int(input("type 1 search specific pages, or type 2 search a range pages, type 3 download all pages:"))

    if dettt == 1:
        det = int(input("how many pages you want to download"))
        mode = 1
        tpage = det

    elif dettt == 2:
        star = int(input("start from which pages?:"))
        endd = int(input("end pages?:"))
        mode = 2
        start = star
        end = endd
    elif dettt == 3:
        mode = 3

    ## create file
    save_path = str("./ ")[:2] + name
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)
    i = 1
    thd = int(input("use how many thread use to download ?: "))
    poxy = input("type y use proxy? : ")
    while i <= total:
        if mode == 1:
            if i <= tpage:
                id = getpageids(name, None, 1, i)
                if len(id) == 0:
                    i = total + 1
                t_line = line()
                print(thd,len(id)//thd,"<<<<<<<<<<<<<<<<<<<<<")
                t_line.creat(thd,len(id)//thd)
                start_Thead(id,poxy,thd,t_line)

            if i > tpage:
                i = total + 1
        elif mode == 2:
            # rage
            if i > start and i < end:
                id = getpageids(name, None, 1, i)
                start_Thead(id,poxy,thd)
        elif mode == 3:
            id = getpageids(name, None, 1, i)
            start_Thead(id,poxy,thd)
        i += 1


def changer():
    global save_path
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))

    likes = str(likes) + "users"
    page = 1

    n_Num = sname + str(likes)
    save_path = str("./ ")[:2] + n_Num
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)

    url = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(
        sname, likes, sname, likes, page)
    page = getTotalPage(url)
    print(str(page) + " pages found!")
    a = input("press y to start download")
    id = []
    if a == "y":

        for i in range(page):
            print("download page: " + str(i + 1))
            id = getpageids(sname, likes, 1, i + 1)
            print(id)
            if len(id) == 0:
                return False
            else:
                pass
                iddownloader(id)
    else:
        pass


def iddownloader(id,t,task_obj):
    isDown = []
    for i in range(len(id)):
        isDown.append(True)
    with progress:
        t = task_obj.get_obj()[int(t)]
        for x in range(len(id)):
            try:
                randomid = random.randint(0, len(id) - 1)
                while not isDown[randomid]:
                    randomid = random.randint(0, len(id) - 1)
                isDown[randomid] = False
                progress.update(t, completed=x)
                print(x, "index update")
                download(int(id[randomid]), 1)
            except:
                print("fail download id :" + id[x])
                time.sleep(10)
                download(int(id[randomid]), 1)
            time.sleep(random.randrange(0, 3))


def getpageids(sname, likes, total, page):
    id = []
    if likes == None:
        for x in range(total):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(
                sname, sname, page)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(3)
    else:
        for x in range(total):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}%20{}%E5%85%A5%E3%82%8A?word={}%20{}%E5%85%A5%E3%82%8A&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(
                sname, likes, sname, likes, page)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(3)

    id = cleanArray(id)
    return id


def cleanArray(arr):  # 9 digets
    new = []
    for x in range(len(arr)):
        if len(arr[x]) > 9:
            pass
        else:
            new.append(arr[x])
    arr = new
    return arr


def getTotalPage(url):
    res = requests.get(url, headers=headers)
    total = re.findall(r'"total":(.+?),', res.text)
    print(total, "images found")
    page = 1
    ct = int(total[0])
    if ct > 60:
        page += int(ct / 60)
        return page
    else:
        return 1


def M_Pid_search(num, end, mode, name):
    id = []
    print("getting ids pls wait for a while")
    if mode == 1:
        # get total id by pages
        for x in range(num):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(
                name, name, x + 1)
            print(k)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(0, 5))
        return id
    elif mode == 2:
        for x in range(num, end + 1):
            k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(
                name, name, x + 1)
            # print(k)
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randrange(0, 5))
        return id

def start_Thead(id,poxy,thdN,thead_obj):
    global process_L

    if poxy == "y":
        is_use_proxy=True
    else:
        is_use_proxy=False
    div = len(id) // thdN
    k = 1
    while k <= thdN:
        arr = id[div * (k - 1):div * (k)]
        t = Thread(target=iddownloader, args=(arr,k-1,thead_obj,))
        t.start()
        k += 1

def cos(n):
    global save_path
    global is_use_proxy
    is_use_proxy = input("type Y to use the proxy when download")

    if n == 1:  # search with ranking

        changer()
    elif n == 2:  # trending
        day = dateutil.utils.today()
        dd = day.strftime('%d') + day.strftime('%b')
        save_path = str("./_trending%s") % (dd)
        if os.path.exists(save_path) == True:
            pass
        else:
            os.mkdir(save_path)
        trending()

    elif n == 3:
        NormalS()

def ip_proxy():
    # testing the workable ip proxy and save in local file
    ipproxies = []
    ipproxies_Good=[]
    a = open("proxy.txt", "r", encoding="utf-8")
    text = a.read()
    ip_pool = re.findall(r'"ip":"(.+?)"', text)
    prot_pool = re.findall(r'"port":"(.+?)"', text)

    for i in range(len(ip_pool)):
        ipproxies.append("{}:{}".format(ip_pool[i], prot_pool[i]))
    for i in range(len(ip_pool)):
        try:
            res = requests.get(url="https://i.pximg.net/img-master/img/2022/11/27/02/27/56/103127937_p0_master1200.jpg", headers=headers,proxies={"http": "http" + "://" + ipproxies[i]},timeout=1)
            if res.status_code==200:
                print(ipproxies[i],"可用")
                print({"http": "http" + "://" + ipproxies[i]})
                ipproxies_Good.append(ipproxies[i])

        except:
            print(ipproxies[i], "不可用")
            print({"http": "http" + "://" + ipproxies[i]})
    print(ipproxies_Good)
    with open("ip_work.txt",'w') as f:
        f.write(str(ipproxies_Good))
def getRandomIp():
    ips = open("ip_work.txt","r")
    convered = ast.literal_eval(ips.read())
    return random.choice(convered)
def down_newProxy():
    res = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=https",headers=head)
    with open("proxy.txt","w",encoding="utf-8") as f:
        f.write(res.text)

class line():
    def __init__(self):
        self.obj=[]
    def creat(self,num,total):
        color = ["red","blue","pink","cyan"]
        for i in range(num):
            self.obj.append(progress.add_task(description="[{}]task_{}_{}".format(random.choice(color),i,str(random.randint(100,999))), total=total))
    def get_obj(self):
        return self.obj
    def reset(self):
        line()



# download(33165101,1)

cos(int(input("1:(searching with rank ) 2:(daily trending mode), 3:(normal searching)\n->")))
# NormalS()
# id = getpageids("scaramouche","1000",1,1)
#down_newProxy()
#ip_proxy()
#print(getRandomIp())
#print(type(getRandomIp()))
#res = requests.get("https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=1")
#down_newProxy()
#download(103070297,1)
import os
import os.path
import random
import re
import time
from threading import Thread
import requests
from tqdm import tqdm
import ast
import hashlib
import threading
from datetime import datetime
import shutil
from rich import print
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    TextColumn,
    MofNCompleteColumn
)
import traceback


progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    MofNCompleteColumn(),
    # TransferSpeedColumn(),
    transient=True

)

save_path = "./"
# c_k = input("type y to change cookies->")
cook = "first_visit_datetime_pc=2021-09-02+23%3A43%3A13; p_ab_id=3; p_ab_id_2=6; p_ab_d_id=1362319497; yuid_b=N0F1eBc; privacy_policy_notification=0; b_type=1; ki_r=; login_ever=yes; ki_s=214908%3A0.0.0.0.2%3B214994%3A0.0.0.0.2%3B215190%3A0.0.0.0.2%3B219376%3A0.0.0.0.2%3B221691%3A0.0.0.0.2; ki_t=1632313976963%3B1640175147711%3B1640175165221%3B5%3B49; c_type=25; a_type=1; privacy_policy_agreement=5; _gcl_au=1.1.1543749531.1664107948; first_visit_datetime=2022-11-03+18%3A26%3A00; _ga_MZ1NL4PHH0=GS1.1.1667521370.6.0.1667521370.0.0.0; tag_view_ranking=_EOd7bsGyl~uusOs0ipBx~jhuUT0OJva~lkoWqucyTw~ziiAzr_h04~RTJMXD26Ak~B6uEbiYg7i~fHzsW6IqUG~CluIvy4vsU~ZNRc-RnkNl~mkdwargRR2~dI30gMiyFa~qDi7263PSz~_hSAdpN9rx~P8OX_Lzc1b~pzZvureUki~mLrrjwTHBm~yTWt5hzG4w~q1r4Vd8vYK~Lt-oEicbBr~CbkyggmWCV~9Gbahmahac~6293srEnwa~UotTWDag3B~Bzyu1zjric~QliAD3l3jr~MnGbHeuS94~RgJEiMBANx~ZPjQtvhTg3~_wgwZ79S9p~bv3Hjql-Z1~nWC-P2-9TI~Ie2c51_4Sp~LJo91uBPz4~JL8rvDh62i~JrQgdjRZtN~9dh32MPwDj~EUwzYuPRbU~w8ffkPoJ_S~K8esoIs2eW~aTW6kYb0Ak~IsJjJpzDo3~83nP16VbYh~Thyk9saBEx~0IB1cxSXTq~jH0uD88V6F~9ODMAZ0ebV~nQRrj5c6w_~gGjtVdrrFe~BSlt10mdnm~P-Zsw0n2vU~pzzjRSV6ZO~bq1HPY2wZ-~pnCQRVigpy~rOnsP2Q5UN~CHzc3gIECp~D6xAR9Wod9~cb-9gnu4GK~pa4LoD4xuT~tlI9YiBhjp~RybylJRnhJ~2pZ4K1syEF~TqiZfKmSCg~faZX-CfhYv~yREQ8PVGHN~1s4b4irzBH~QIc0RHSvtN~hW_oUTwHGx~OUqETMPW2Z~YbOo-qnBCR~2V0-EgyHVg~CLEmkBaAcu~BOHDnbK1si~FuSOTTQp_1~PiKFMvIHS1~OqRhcPLny7~MmeCZpWKlw~sq89u71dz_~9lkAIZCWYJ~WcKJlmc3yI~LpjxMAWKke~t2ErccCFR9~NXxDJr1D_u~Wxk4MkYNNf~zx-g5-W1ik~lD5tMyRpMY~T9RlZXWwcd~tfLhZBEOFy~wKl4cqK7Gl~zKLqKSPEAG~w6DOLSTOSN~o7hvUrSGDN~jy1Ljjlbd1~xF0JX9eOwX~BC84tpS1K_~6ImQE2rhA3~ETjPkL0e6r~v-OL0-Ncw6~jk9IzfjZ6n~KvAGITxIxH; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.1088489866.1669880446; __cf_bm=0aX0teIJy1x7dHT52js_p1kzOBP39peCRN2vJUitwHI-1669942388-0-AfexysZqwif0DHcChJtMX/VPvzq8z+thC+YnHqZ5aRvkTXsmOlVYhuJ8MF+45xNhT95ISflNJEGX8NGzxNElrT5Q3KoSRfMitw++orunvJvrjJ9MO40Z/IZ2fFGLJtrQIxrWOgBsfjNBXFPJcsJZqE3v0guRVDl8LE/zyMiKE3YieV5m1oyH58yUurS+fjdE+f0G15jdd95nCuSzvYM5/BU=; PHPSESSID=52047359_IOPTVFnqi9jltYj8tSaKOugFZ0q36LkB; device_token=984aa28b59e17511e41f4fe4f864e95e; _ga=GA1.2.1138408233.1634023850; _ga_75BBYNYN9J=GS1.1.1669942414.64.1.1669942548.0.0.0"
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
lines_variable = []  # the rich.progress objects
is_use_proxy = False  # global variables
filter_likes = None
lock = threading.Lock()
def download(id, count):
    global save_path
    local_save_path= ''
    or_samve_path=save_path
    if is_use_proxy:
        c = getRandomIp()
        prox = {"http": "http" + "://" + c, }
    else:
        prox = None
    i_data = ill_detail(int(id))
    if i_data==None:
        print(f"{id} is not a illustration")
        return None
    count=i_data[3]
    #print(count,id)
    if count > 1:
        local_save_path = save_path + '/%s' % (str(id))
        if os.path.exists(local_save_path) == True:
            pass
        else:
            os.mkdir(local_save_path)
    else:
        local_save_path=save_path
    for i in range(0, int(count)):
        url_ = i_data[1] # [0]likes [1]url [2] pic name(required decode!)
        extension = url_[len(url_) - 4:]  # get the extention
        total_like= i_data[0]
        url_ = url_[:len(url_) - 5] + str(i) + extension
        pic_name=i_data[2].encode().decode('unicode_escape')
        url = url_
        pic_url = (local_save_path + '/%s%d%s%s') % (pic_name,i + 1, '_' + str(id), extension)
        # useing the api to get picture by url

        if not os.path.exists(pic_url):
            if filter_likes != None:
                if total_like >= filter_likes:
                    api_pic_request = requests.get(url, headers={'Referer': 'https://app-api.pixiv.net/'}, params=None, data=None,
                                                   stream=True,timeout=10,proxies=prox)
                     # change path
                    print(f'id{id} fit condition!')
                    with  open(pic_url, 'wb') as f:
                        shutil.copyfileobj(api_pic_request.raw, f)
                else:
                   print(f'id{id} not fit condition!')
                   break
            elif filter_likes== None:
                api_pic_request = requests.get(url, headers={'Referer': 'https://app-api.pixiv.net/'}, params=None,
                                               data=None,
                                               stream=True, timeout=10,proxies=prox)
                pic_url = (local_save_path + '/%s%d%s%s') % (pic_name+"_",i + 1, '_' + str(id), extension)  # change path
                pic_url=re.sub('[\\\ |]','',pic_url)
                with  open(pic_url, 'wb') as f:
                    shutil.copyfileobj(api_pic_request.raw, f)

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
    global filter_likes
    name = input("what you want to search:\n->")
    ll= input("use the likes filter? (y or n )-> ")
    mode_search = input("mode:safe,r18 or all->")
    if ll == 'y':
        filter_likes=int(input("how much likes?->:"))
    else:
        filter_likes=None
    page = 1
    mode = 0
    start = 0
    end = 0
    tpage = 0
    url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(name, name, page)
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
    while i <= total:
        if mode == 1:
            if i <= tpage:
                id = getpageids(name, None, 1, i,mode_search)
                if len(id) == 0:
                    i = total + 1
                print(f"start downloading page{i}")
                start_Thead(id, is_use_proxy, thd)
                time.sleep(10)
            if i > tpage:
                i = total + 1
        elif mode == 2:
            # rage
            if i > start and i <= end:
                id = getpageids(name, None, 1, i,mode_search)
                start_Thead(id, is_use_proxy, thd)
                time.sleep(10)
        elif mode == 3:
            id = getpageids(name, None, 1, i,mode_search)
            start_Thead(id, is_use_proxy, thd)

            for i in range(len(lines_variable)):
                lines_variable[i].remove()
        i += 1



def changer():
    global save_path
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))

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
    a = input("press y to start download->:")
    id = []
    if a == "y":

        for i in range(page):
            print("download page: " + str(i + 1))
            id = getpageids(sname, likes, 1, i + 1)
            if len(id) == 0:
                return False
            else:
                pass
            start_Thead(id, False, thd)
    else:
        pass


def iddownloader(id, pLines_variables):
    isDown = []
    for i in range(len(id)):
        isDown.append(True)
    with progress:
        i = 0
        task = pLines_variables.get_obj()
        while i < len(id):
            try:
                randomid = random.randint(0, len(id) - 1)
                while not isDown[randomid]:
                    randomid = random.randint(0, len(id) - 1)
                isDown[randomid] = False
                download(int(id[randomid]), 1)
                i += 1
                print(f"id:{id[randomid]} [bold green]successful download")
                progress.update(task, description=f"Thread [bold yellow]#{pLines_variables.get_taskid()}->[bold red]ID:{id[randomid]}",completed=i)
                time.sleep(random.randint(0, 2))
            except Exception as e :
                #traceback.print_exc() #only for debugging
                print(str(e))
                print(f"id:{id[randomid]} [bold red] exception occurred fail to download")
                i += 1
                time.sleep(random.randint(5,15))




def getpageids(sname, likes, total, page,mode):
    id = []
    if likes == None:
        for x in range(total):
            k = "https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode={}&p={}&s_mode=s_tag&type=all&lang=zh".format(sname, sname, mode, page)
            "k = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag_full&type=all&lang=zh&format=json'.format(sname, sname, page)"
            res = requests.get(k, headers=headers)
            id = id + re.findall(r'"id":"(.+?)"', res.text)
            time.sleep(random.randint(2,5))
    else:
        for x in range(total):
            likes = str(likes) + "users"
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
        if len(arr[x]) == 9 or len(arr[x]) == 8:
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
def start_Thead(id, poxy, thdN):
    global process_L
    global Thread_varables
    global lines_variable
    Thread_varables = []
    if poxy == "y":
        is_use_proxy = True
    else:
        is_use_proxy = False

    av = len(id) // thdN
    remainder = len(id)%thdN

    for i in range(thdN):
        lines_variable.append(create_process_lines())
        if i < thdN-1:
            lines_variable[i].creat(av, i + 1)
        else:
            lines_variable[i].creat(av+remainder, i + 1)

    k = 0
    while k < thdN:
        if k < thdN-1:
            arr=id[av * k:av * (k + 1)]
        else:
            arr=id[av * k:av * (k + 1) + remainder]
        thread = Thread(target=iddownloader, args=(arr, lines_variable[k]))
        Thread_varables.append(thread)
        thread.start()
        time.sleep(0.1)
        k += 1
    for x in Thread_varables:
        x.join()
        time.sleep(0.1)
    print(threading.active_count(), ": Threads are working")
    print(progress.finished)
    for i in lines_variable:
        i.remove()
    lines_variable=[]
    Thread_varables = []


def get_access_token():
    local_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    hash_secret = "28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c"
    headers_token = {'app-os': 'ios', 'app-os-version': '14.6',
                     'user-agent': 'PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)', 'x-client-time': local_time,
                     'x-client-hash': hashlib.md5((local_time + hash_secret).encode("utf-8")).hexdigest()}
    data = {
        "get_secure_url": 1,
        "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
        "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
        "grant_type": "refresh_token",
        "refresh_token": "TeG9sEHMAlfq8Y_Ru-ciZC--tkfQJ2C4WqcFdgUKUO8"
    }
    headers_ = {
        'app-os': 'ios',
        'app-os-version': '14.6',
        'user-agent': 'PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)',
        'Authorization': 'Bearer NHaa7POWzfx_nueyWFb9YmEd5xL1h5_jcXBmwvUSyr8'
    }

    url = "https://oauth.secure.pixiv.net/auth/token"
    get_access_token = requests.post(url, headers=headers_token, data=data)
    headers_['Authorization'] = "Bearer " + re.findall('"access_token":"(.+?)",', get_access_token.text)[0]

    with open("access_tkoen.txt", "w") as f:
        f.write(str(headers_))
    return headers_


def ill_detail(id):
    # return an array contain total_view & pic_url
    api_main = "https://app-api.pixiv.net"
    ill_detail_url = "%s/v1/illust/detail" % api_main
    ill_detail_params = {
        "illust_id": id,
    }
    res = requests.get(ill_detail_url, headers=get_access_token(), params=ill_detail_params)
    try:
        likes = int(re.findall(r'"total_view":(.+?),', res.text)[0])
    except:
        return None
    ill_name_raw = repr(re.findall(r'"title":"(.+?)"', res.text)[0])
    ill_name_raw=ill_name_raw.encode().decode('unicode_escape')
    ill_name_raw=ill_name_raw.replace("'",'')
    ill_name_raw=re.sub('[\\\  /,"],[/^u]','',ill_name_raw)
    page_count= int(re.findall(r'"page_count":(.+?),',res.text)[0])
    try:
        pic_url = re.findall(r'"original_image_url":"(.+?)"', res.text)[0]
    except:
        pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
    if re.search('[\\\ \ \* \? \" \ \< \> \| ,]', pic_url) != None:
        pic_url = re.sub('[\\\ \ \* \? \" \ \< \> \| ,]', '', pic_url)
    return [likes, pic_url,ill_name_raw,page_count]


def Choser():
    global save_path
    global is_use_proxy
    global thd
    try:
        test = requests.get("http://www.pixiv.net",headers= headers,timeout=1)
        if test.status_code==200:
            n = int(input("1:(searching with rank(by tags)) 2:(different ranking mode), 3:(normal searching) 4(update proxy ) 5(user likes) 6 (download from illustrator)\n->"))
            if n == 1 or n == 2 or n == 3:
                is_use_proxy = input("type Y to use the proxy when download")
                thd = int(input("use how many thread use to download ?: "))
            if n == 1:  # search with ranking
                changer()
            elif n == 2:  # trending
                ranking()
            elif n == 3:
                NormalS()
            elif n == 4:
                print("updating proxy[bold yellow]------")
                down_newProxy()
                ip_proxy()
            elif n == 5:
                api_main = "https://app-api.pixiv.net"
                user_like_para = {"user_id": 52047359, "filter": "for_ios", "restrict": "public", "max_bookmark_id": None,
                                  "tag": None}
                user_like = "%s/v1/user/bookmarks/illust" % api_main
                rc = requests.get(user_like, params=user_like_para, headers=get_access_token())
                r = re.findall(r'"id":(.+?),', rc.text)
                id=cleanArray(r)
                start_Thead(id,is_use_proxy,4)
            elif n ==6:
                illustrator_id=input("type illustrator id there->")
                illustrator_mode(illustrator_id)
            else:
                pass
    except:
        print(print("fail to send request to pixiv.net\npls check you network or turn on VPN on"))
        pass



def ip_proxy():
    # testing the workable ip proxy and save in local file
    ipproxies = []
    ipproxies_Good = []
    a = open("proxy.txt", "r", encoding="utf-8")
    text = a.read()
    ip_pool = re.findall(r'"ip":"(.+?)"', text)
    prot_pool = re.findall(r'"port":"(.+?)"', text)

    for i in range(len(ip_pool)):
        ipproxies.append("{}:{}".format(ip_pool[i], prot_pool[i]))
    for i in range(len(ip_pool)):
        try:
            res = requests.get(url="https://pixiv.net",
                               headers=headers, proxies={"http": "http" + "://" + ipproxies[i]}, timeout=1)
            if res.status_code == 200:
                # print(ipproxies[i], "可用")
                print({"http": "http" + "://" + ipproxies[i]})
                ipproxies_Good.append(ipproxies[i])

        except:
            # print(ipproxies[i], "不可用")
            print({"http": "http" + "://" + ipproxies[i]})
    print(ipproxies_Good)
    with open("ip_work.txt", 'w') as f:
        f.write(str(ipproxies_Good))
    print(f"{len(ipproxies_Good)} proxies available[green bold] ")
    print(f"proxies had been written in to file!!! update if necessary[red bold]")


def getRandomIp():
    ips = open("ip_work.txt", "r")
    convered = ast.literal_eval(ips.read())
    return random.choice(convered)


def down_newProxy():
    res = requests.get(
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=https",
        headers=head)
    with open("proxy.txt", "w", encoding="utf-8") as f:
        f.write(res.text)


# process line
class create_process_lines():
    def __init__(self):
        self.obj = None
        self.total = 0
        self.taks_Numbers = 0

    def creat(self, total, taks_Number):
        self.taks_Numbers = taks_Number
        self.total = total
        self.obj=progress.add_task(description=f"Job [bold yellow]#{taks_Number}#", total=total)

    def get_obj(self):
        return self.obj

    def get_total(self):
        return self.total

    def get_taskid(self):
        return self.taks_Numbers
    def remove(self):
        progress.remove_task(self.obj)

def raw_processer(text):
    id=[]
    id = re.findall(r'"id":(.+?),', text)
    return cleanArray(id)

def illustrator_mode(id):
    api_main = "https://app-api.pixiv.net"
    user_ill = "%s/v1/user/illusts" % api_main
    user_detail = "%s/v1/user/detail" %api_main
    global save_path
    save_path ="./{}".format(id)
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)
    print(save_path)
    params_user = {
        "user_id": id,
        "filter": "for_ios",
    }
    params = {
        "user_id": id,
        "filter": "for_ios",
        "offset": 1,
    }
    user_detaill=requests.get(user_detail,headers=get_access_token(),params=params_user)
    user_total_ill=re.findall(r'"total_illusts":(.+?),',user_detaill.text)[0]
    print(user_total_ill)
    user_detaill= int(user_total_ill)//30
    print(user_detaill)
    for i in range(user_detaill):
        params["offset"]=i*30
        resc = requests.get(user_ill, headers=get_access_token(), params=params)
        start_Thead(raw_processer(resc.text), None, 4)

def ranking():
    global save_path
    types = ["day","week","month","day_male","day_female","week_original","week_rookie","day_manga","day_r18","day_male_r18","day_female_r18","week_r18","week_r18g"]
    param = {"mode": "day", "filter": "for_ios", "date": None, "offset": None}
    type_Rank_url = "https://app-api.pixiv.net/v1/illust/ranking"
    now = datetime.now()
    day = now.strftime("_%m_%d_%Y")
    for i in range(len(types)):
        print(f"{types[i]}: {i+1}",end=" ")
    choose = int(input("\nwhich type ranking you want to apply(by numbers)->\n:"))-1
    if choose<=len(types):
        print(f"using {types[choose]} mode")
        param["mode"]=types[choose]
    else:
        print("using default mode -> day")
        param["mode"]="day"
    save_path = str(f"./{types[choose]}%s") % (day)
    if os.path.exists(save_path) == True:
        pass
    else:
        os.mkdir(save_path)
    r= requests.get(type_Rank_url,params=param,headers=get_access_token())
    id = raw_processer(r.text)
    start_Thead(id,is_use_proxy,thd)

Choser()


api_main = "https://app-api.pixiv.net"
user_ill = "%s/v1/user/illusts" % api_main
type_Rank_url = "https://app-api.pixiv.net/v1/illust/ranking"

'''_MODE: TypeAlias = Literal[
    "day",
    "week",
    "month",
    "day_male",
    "day_female",
    "week_original",
    "week_rookie",
    "day_manga",
    "day_r18",
    "day_male_r18",
    "day_female_r18",
    "week_r18",
    "week_r18g",
    "",
]'''




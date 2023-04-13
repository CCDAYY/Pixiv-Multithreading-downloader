from __future__ import annotations

import ast
import hashlib
import os
import os.path
import random
import re
import shutil
import time
import traceback
from datetime import datetime
from threading import Thread
import requests
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TimeElapsedColumn,
    TextColumn,
    MofNCompleteColumn
)

progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    MofNCompleteColumn(),
    # TransferSpeedColumn(),
    transient=True

)

try:
    with open("cookie.txt", "r") as f:
        cook = f.read()
except:
    print("error no cookie")
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
fail_id = []
filter_likes = None
thd = 4
illustration_pool = []

def creat_dir(path):
    if os.path.exists(path) == True:
        pass
    else:
        os.mkdir(path)
save_path = "./pixiv"
creat_dir(save_path)

def getpictures(path):
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg')]
    for x in range(len(files)):
        files[x]=files[x].replace('\\','/')
    return files

def download(id):
    global save_path
    global fail_id

    try:
        i_data = ill_detail(int(id))
        total_like = i_data[0]
        count = i_data[3]
        local_save_path = save_path
        for i in range(0, int(count)):
            url_ = i_data[1]  # [0]likes [1]url [2] pic name(required decode!)
            extension = url_[len(url_) - 4:]  # get the extention
            url_ = url_[:len(url_) - 5] + str(i) + extension
            pic_name = i_data[2].encode().decode('unicode_escape')
            url = url_
            pic_url = (local_save_path + '/%s%d%s%s') % (pic_name, i + 1, '_' + str(id), extension)
            pic_url = re.sub('[\\\ |"<>!*?]', '', pic_url)
            print(f'[bold yellow] {pic_url}')
            # useing the api to get picture by url
            files = getpictures(save_path)
            if not pic_url in files:
                if filter_likes != None:
                    if total_like >= filter_likes:
                        api_pic_request = master_request(method="GET", url=url,header={'Referer': 'https://app-api.pixiv.net/'},is_token=False, parameters=None)
                        print(f'id{id} fit condition!')
                        try:
                            with  open(pic_url, 'wb') as f:
                                shutil.copyfileobj(api_pic_request.raw, f)
                        except:
                            with  open(f'local_save_path+/{id+extension}', 'wb') as f:
                                shutil.copyfileobj(api_pic_request.raw, f)
                    else:
                        print(f'id{id} not fit condition!')
                        break

                elif filter_likes == None:
                    api_pic_request = master_request(method="GET", url=url,header={'Referer': 'https://app-api.pixiv.net/'}, is_token=False,parameters=None)
                    try:
                        with open(pic_url, 'wb') as f:
                            shutil.copyfileobj(api_pic_request.raw, f)
                    except:
                        with  open(f'local_save_path+/{id + extension}', 'wb') as f:
                            shutil.copyfileobj(api_pic_request.raw, f)

        lines_variable[0].update()
    except:
        #print(f"{f}-> fail during download ")
        lines_variable[0].update()
        time.sleep(random.randint(0, 5))


def raw_processer(text):
    id = re.findall(r'"id":(.+?),', text)
    user_id = re.findall(r'"user":{"id":(.+?),', text)
    new_id = []
    for i in range(len(id)):
        if not id[i] in user_id:
            new_id.append(id[i])
    return new_id


def NormalS():
    global save_path
    global filter_likes
    name = input("what you want to search:\n->")
    ll = input("use the likes filter? (y or n )-> ")
    if ll == 'y':
        filter_likes = int(input("how much likes?->:"))
    else:
        filter_likes = None
    mode = ["partial_match_for_tags", "exact_match_for_tags", "title_and_caption"]
    print(mode[:])
    choose = int(input("which one-> (EX,0,1,2)"))
    mode_search = mode[choose]

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
    save_path = save_path + '/' + name
    save_path = re.sub('[\\\ |"<>!*?]', '', save_path)
    creat_dir(save_path)
    i = 1
    while i <= total:

        if mode == 1:
            id = getpageids(sname=name, page=i, total=1, mode=mode_search)
            if i <= tpage:
                if len(id) == 0:
                    i = total + 1
                print(f"start downloading page:{i}[bold yellow]")
                start_Thead(id, thd)
                print(f"[bold green ]finsihed the page:{i}")
                time.sleep(10)
            if i > tpage:
                i = total + 1
        elif mode == 2:
            print(f"start downloading page:{i}[bold yellow]")
            id = getpageids(sname=name, page=i, total=1, mode=mode_search)
            # rage
            if i > start and i <= end:
                start_Thead(id, thd)
                time.sleep(10)
            print(f"[bold green ]finsihed the page:{i}")
        elif mode == 3:
            print(f"start downloading page:{i}[bold yellow]")
            id = getpageids(sname=name, page=i, total=1, mode=mode_search)
            start_Thead(id, thd)
            print(f"[bold green ]finsihed the page:{i}")
            time.sleep(10)
        i += 1


def changer():
    global save_path
    sname = input("type the things that you want to seach :\n")
    likes = int(input("choose either of : 50,100,300,500,1000,5000,10000 :\n"))
    page = 1
    n_Num = sname + str(likes)
    save_path = save_path + "/" + n_Num
    creat_dir(save_path)
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
            start_Thead(id, thd)
    else:
        pass


def getpageids(sname: str, total: int, page: int | None = None, mode: str | None = None):
    if mode == None:
        mode = "exact_match_for_tags"
    id = search(name=sname, search_mode=mode, offset=page * 30)
    return id





def getTotalPage(url):
    res = master_request(method="GET", url=url, header=headers, is_token=False)
    total = re.findall(r'"total":(.+?),', res.text)
    print(total, "images found")
    page = 1
    ct = int(total[0])
    if ct >= 30:
        page += ct // 30
        return page
    else:
        return 1


def bar_line_live():
    with progress:
        while not progress.finished:
            progress.update(lines_variable[0].get_obj(),
                            description=f"Thread [bold yellow]#{lines_variable[0].get_taskid()}->[bold red]",
                            completed=lines_variable[0].get_completed())
            time.sleep(0.1)


def start_Thead(id, thdN):
    print("start the thread")
    global process_L
    global Thread_varables
    global lines_variable
    Thread_varables = []
    global illustration_pool

    lines_variable.append(create_process_lines())
    lines_variable[0].creat(total=len(id), taks_Number=1)
    Line_Thread = Thread(target=bar_line_live)
    Line_Thread.start()
    for i in range(len(id)):
        illustration_pool.append(cread_ill_objects())
        illustration_pool[i].creat(id[i], False)
    print(f'{len(id)} picture going to download[bold green]')
    for dev in range((len(id) // thdN)):
        temp_job_list = []
        for group in range(thdN):
            random_choose = random.choice(illustration_pool)
            while random_choose.is_downloaded():
                random_choose = random.choice(illustration_pool)
            thread = Thread(target=download, args=(random_choose.get_ill_id(),))
            random_choose.setter()
            temp_job_list.append(thread)
        for jobs in temp_job_list:
            jobs.start()
            time.sleep(0.01)
        for wait in temp_job_list:
            wait.join()
            time.sleep(0.01)
    for objs in illustration_pool:
        if not objs.is_downloaded():
            download(objs.get_ill_id())
            objs.setter()
    lines_variable[0].reset_complete()
    lines_variable[0].remove()
    illustration_pool = []

def search(name: str, search_mode: str, offset: str | int | bool, duration: str | None = None,
           start_date: str | None = None):
    url = "https://app-api.pixiv.net/v1/search/illust"
    param = {
        "word": name,
        "search_target": search_mode,
        "offset": offset,
        "sort": "date_desc",
        "filter": "for_ios",
        "duration": None,
        "start_date": None,
        "end_date": None,
    }
    try:
        res = master_request(method="GET", url=url, is_token=True, parameters=param)
        return raw_processer(res.text)
    except:
        return []

def ill_detail(id: object) -> object:
    # return an array contain total_view & pic_url
    api_main = "https://app-api.pixiv.net"
    ill_detail_url = "%s/v1/illust/detail" % api_main
    ill_detail_params = {
        "illust_id": id,
    }

    res = master_request(method="GET", url=ill_detail_url, is_token=True, parameters=ill_detail_params)
    if res ==None:
        return None
    likes = int(re.findall(r'"total_view":(.+?),', res.text)[0])
    ill_name_raw = repr(re.findall(r'"title":"(.+?)"', res.text)[0])
    page_count = int(re.findall(r'"page_count":(.+?),', res.text)[0])
    ill_name_raw = ill_name_raw.encode().decode('unicode_escape')
    ill_name_raw = ill_name_raw.replace("'", '')
    ill_name_raw = ill_name_raw.replace("\/", '')

    try:
        pic_url = re.findall(r'"original_image_url":"(.+?)"', res.text)[0]
    except:
        pic_url = re.findall(r'"original":"(.+?)"', res.text)[0]
    if re.search('[\\\ \ \* \? \" \ \< \> \| ,]', pic_url) != None:
        pic_url = re.sub('[\\\ \ \* \? \" \ \< \> \| ,]', '', pic_url)

    return [likes, pic_url, ill_name_raw, page_count]


def Choser():
    global save_path
    global thd
    try:
        test = master_request(method="GET", url="http://www.pixiv.net", header=headers, is_token=False)
        if test.status_code == 200:
            n = int(input(
                "1:(searching with rank(by tags)) 2:(different ranking mode), 3:(normal searching)  4(user likes) 5 (download from illustrator)\n->"))

            if n == 1 or n == 2 or n == 3:
                thd = int(input("use how many thread use to download ?: "))
            if n == 1:  # search with ranking
                changer()
            elif n == 2:  # trending
                ranking()
            elif n == 3:
                NormalS()
            elif n == 4:
                name = input("you pixiv id->>")
                UserLiked(name)
            elif n == 5:
                illustrator_id = input("type illustrator id there->")
                illustrator_mode(illustrator_id)
            else:
                pass
        else:
            print("unable to establish the connection[bold red]")
    except Exception as e:
        print(traceback.format_exc(), "line Chooser()")


def illustrator_mode(id):
    api_main = "https://app-api.pixiv.net"
    user_ill = "%s/v1/user/illusts" % api_main
    user_detail = "%s/v1/user/detail" % api_main
    global save_path
    global thd
    save_path = save_path + f"/user_{id}"
    creat_dir(save_path)
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
    user_detaill = master_request(method="GET", url=user_detail, is_token=True, parameters=params_user)
    user_total_ill = re.findall(r'"total_illusts":(.+?),', user_detaill.text)[0]
    print(user_total_ill)
    remainder = int(user_total_ill) % 30
    if int(user_total_ill) % 30 !=0 and int(user_total_ill)//30>0:
        user_detaill = int(user_total_ill)//30 +1
    else:
        user_detaill=1
    for i in range(user_detaill):
        print(f"total pages:{user_detaill}, finished{i}")
        resc = master_request(method="GET", url=user_ill, is_token=True, parameters=params)
        if i == user_detaill-1:
            params["offset"] = params["offset"] + remainder
        else:
            params["offset"] = params["offset"] + 30
        start_Thead(raw_processer(resc.text), thd)
        time.sleep(2)



def ranking():
    global save_path
    global thd
    types = ["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie", "day_manga", "day_r18",
             "day_male_r18", "day_female_r18", "week_r18", "week_r18g"]
    param = {"mode": "day", "filter": "for_ios", "date": None, "offset": None}
    type_Rank_url = "https://app-api.pixiv.net/v1/illust/ranking"
    now = datetime.now()
    day = now.strftime("_%m_%d_%Y")
    for i in range(len(types)):
        print(f"{types[i]}: {i + 1}", end=" ")
    choose = int(input("\nwhich type ranking you want to apply(by numbers)->\n:")) - 1
    if choose <= len(types):
        print(f"using {types[choose]} mode")
        param["mode"] = types[choose]
    else:
        print("using default mode -> day")
        param["mode"] = "day"
    save_path = save_path + str(f"/{types[choose]}%s") % (day)
    creat_dir(save_path)
    r = master_request(method="GET", url=type_Rank_url, parameters=param, is_token=True)
    id = raw_processer(r.text)
    start_Thead(id, thd)


def master_request(method: str, url: str, is_token: bool | True, header: dict | None = None,
                   parameters: dict | str | None = None, data: dict | None = None, retry:int|None=6):
    acc_t = token()
    try:
        if method == "GET":
            if is_token:
                res = requests.get(url=url, params=parameters, headers=acc_t.get_access_token(), stream=True, timeout=1)

                if res.status_code in {200, 301, 302}:
                    return res
                else:
                    if retry>0:
                        print("retrying：",retry)
                        time.sleep(random.randint(1,3))
                        acc_t.update_token()
                        return master_request(method=method, url=url, is_token=is_token, header=header,
                                              parameters=parameters, data=data,retry=retry-1)
            else:
                res = requests.get(url=url, params=parameters, headers=header, stream=True, timeout=1)
                if res.status_code in {200, 301, 302}:
                    return res
                else:
                    if retry>0:
                        print("retrying：",retry)
                        time.sleep(random.randint(1, 3))
                        acc_t.update_token()
                        return master_request(method=method, url=url, is_token=False, header=header, parameters=parameters,
                                              data=data,retry=retry-1)
        elif method == "POST":
            try:
                return requests.post(url=url, headers=header, params=parameters, data=data, timeout=1)
            except Exception as e:
                print("error： ", e)
                return requests.post(url=url, headers=header, params=parameters, data=data, timeout=1)
    except:
        print(f"[bold red ]exception occor retrying :{retry}")
        if retry>0:
            return master_request(method=method, url=url, is_token=is_token, header=header,parameters=parameters, data=data,retry=retry-1)
        print(f"fail request")


def UserLiked(user_id):
    api_main = "https://app-api.pixiv.net"

    user_like_para = {"user_id": user_id, "filter": "for_ios", "restrict": "public",
                      "max_bookmark_id": None,
                      "tag": None}

    user_like = "%s/v1/user/bookmarks/illust" % api_main
    rc = master_request(method="GET", url=user_like, parameters=user_like_para, is_token=True)
    start_Thead(raw_processer(rc.text), thd)


class create_process_lines():
    def __init__(self):
        self.obj = None
        self.total = 0
        self.completed = 0
        self.taks_Numbers = 0

    def creat(self, total, taks_Number):
        self.taks_Numbers = taks_Number
        self.total = total
        self.obj = progress.add_task(description=f"Job [bold yellow]#{taks_Number}#", total=total)

    def get_obj(self):
        return self.obj

    def get_total(self):
        return self.total

    def get_taskid(self):
        return self.taks_Numbers

    def remove(self):
        progress.remove_task(self.obj)

    def update(self):
        self.completed += 1

    def get_completed(self):
        return self.completed

    def reset_complete(self):
        self.completed = 0


class cread_ill_objects():
    def __init__(self):
        self.id = 0
        self.is_downloable = False

    def creat(self, id, download_status):
        self.id = id
        self.is_downloable = download_status

    def get_ill_id(self):
        return self.id

    def is_downloaded(self):
        return self.is_downloable

    def setter(self):
        self.is_downloable = True


class token():
    def __init__(self):
        self.url = "https://oauth.secure.pixiv.net/auth/token"
        self.local_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
        self.hash_secret = "28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c"
        self.headers_token = {'app-os': 'ios', 'app-os-version': '14.6',
                              'user-agent': 'PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)',
                              'x-client-time': self.local_time,
                              'x-client-hash': hashlib.md5(
                                  (self.local_time + self.hash_secret).encode("utf-8")).hexdigest()}
        self.data = {
            "get_secure_url": 1,
            "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
            "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
            "grant_type": "refresh_token",
            "refresh_token": "TeG9sEHMAlfq8Y_Ru-ciZC--tkfQJ2C4WqcFdgUKUO8"
        }
        self.headers_ = {
            'app-os': 'ios',
            'app-os-version': '14.6',
            'user-agent': 'PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)',
            'Authorization': 'Bearer NHaa7POWzfx_nueyWFb9YmEd5xL1h5_jcXBmwvUSyr8'
        }

    def get_access_token(self):
        with open("access_tkoen.txt", "r") as r:
            header = ast.literal_eval(r.read())
        return header

    def update_token(self):
        get_access_token = requests.post(url=self.url, headers=self.headers_token, data=self.data)
        self.headers_['Authorization'] = "Bearer " + re.findall('"access_token":"(.+?)",', get_access_token.text)[0]
        with open("access_tkoen.txt", "w") as f:
            f.write(str(self.headers_))


if __name__ == "__main__":
    #print(getpictures("./pixiv/wanderer"))
    #print(search(name="wanderer",offset=0,search_mode="exact_match_for_tags"))
    #print(ill_detail(54395645))
    Choser()

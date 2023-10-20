import csv
import time
import requests
import json
headers={
        # "authority": "rn01-sycdn.kuwo.cn",
        # "method": "GET",
        # "path": url,
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        # "accept-encoding": "gzip, deflate, br",   
        # "Referer":"https://www.webofscience.com/wos/author/results/1/relevance/2",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": "dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; group=group-c; bm_sz=011C1A6AA8D8C0BC0AC840128D116EB6~YAAQrjMsFzxB6AuLAQAAIj+oEhXm9RKs+aeMw9DXSgKuvPkO2oaUCeTqSDXqsfUdjfuPqQIXEVQYGOb0MfIIFY4LSN6fO8BOgiNUg2SUtw2u4Zr/CZJ06Y6PD8KfDABm4FKQpX2Uhqfug8CHpXpq6zJGayDoPNQxO6jwzJc3eZYGfl18WZS29v64OUtyoy3dFOI08ZM29SNyHuhex2Ynov11rj+HvU9tdrjPoMSlTZi8PyUrTYtjAYXyS8WrNyC4LRJ6fHW0syM6Q6DXKT/TUhx9PanCdtNMXMJ1tuU4mS2/bxotqskoZjg=~4338745~4534322; _sp_ses.840c=*; _abck=36A9D7FEDFB36DD63E38BCA519FC6055~0~YAAQrjMsF9ZB6AuLAQAAo0WoEgrttNxljDbSRLUEIu4MUy+Ll0oMjOiGFzGu6tJ2iNvLkl2BEz9YqP70RIOgCqtZA/d44w1XXOVPABB2V8sVEOrYHMp41Z3iuHKDYB0Jedpv5DtiUpP4totnkkD8sfhO5wDEYIJazrzwY/bjKCkoXOqTLblYz1IMtPd+tKEae0zAXArS65FrDIIkMWlAqN0FI0sZwtUY//scSHQ6uM9VEBJujwGbspkre3DgSWlymQNJCZJJxWWSaP5HCpunMj9spOz2/yjycPY2m1yx+h22eiNEvuaVMjE1OBckwyILH9eXz/T6EsB8CO+kRvnI64NdtEehKORfPlaCmzifemitjS2Ktze56KVGuELQmKZtQVZ9AisO8Qx+P7g630T11VrxEkBtQz6RMTVXgaVWxQ==~-1~-1~-1; sessionid=zklubvgarjmub75urzqk6xer22txofei; _sp_id.840c=2284771f-afe5-4ecd-b903-7c027986fd66.1696825098.1.1696825665..40415ac0-395f-41cd-89ac-050d4d7636b2..fac70629-2d5f-4e10-8c8d-92e0d2f473b9.1696825266626.14",
        "pragma": "no-cache",
        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Microsoft Edge\";v=\"91\", \"Chromium\";v=\"91\"",
        "sec-ch-ua-mobile": "?0",
        "Sec-Ch-Ua-Platform":"Windows",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "X-1p-Wos-Sid":"USW2EC0EE8aHpdolBRLMPC1V23C2E",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48"
}

def getUrl(url):
    try:
        resp = requests.get(url, headers=headers, timeout = 30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding  
        return resp
    except Exception as e:
        print("wrong:",e)
        return None

def postUrl(url,data):
    try:
        resp = requests.post(url, data=data, headers=headers, timeout = 30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp
    except Exception as e:
        print("wrong:",e)
        return None

def saveCsv(dictData,name,Tag = False):

    import os
    path = "field school rank"
    if os.path.exists(path) == False:
        print("creating", path, "path")
        os.makedirs(path)
    print("to csv..")
    name = name.replace("/"," & ")
    with open(f'{path}/{name}.csv', 'a', encoding='utf-8',newline='') as csvfile:
        fp = csv.DictWriter(csvfile,fieldnames=["University","ranking","field"])
        if Tag:
            fp.writeheader()
        try:
            fp.writerows(dictData)
        except Exception as e:
            print(e)

def get_school(field,page,rank):
    url = f"https://www.usnews.com/best-colleges/api/search?format=json&schoolType=national-universities&study={field}&_sort=rank&_sortDirection=asc&_page={page}"
    resp = getUrl(url).json()
    items = resp["data"]["items"]
    schoolDatas = []
    for item in items:
        displayName = item["institution"]["displayName"]
        # rank = item["institution"]["rankingSortRank"]
        schoolData = {
            "University":displayName,
            "ranking":rank,
            "field":field
        }
        rank += 1
        print(schoolData)
        schoolDatas.append(schoolData)
    return schoolDatas,rank
    # print(item)
    # break


def pagingSave():
    f = open('field.json', 'r')
    content = f.read()
    f.close()
    fields = json.loads(content)
    for field in fields["field"]:
        rank = 1
        for page in range(1, 8):
            try:
                datas,rank = get_school(field, page,rank)
            except Exception as e:
                print("no more university：",e)
                break
            try:
                if page == 1:
                    saveCsv(datas, field, True)
                else:
                    saveCsv(datas, field, False)
            except Exception as e:
                print("failed")
                time.sleep(10)
                saveCsv(datas, field)

def singleSave():
    f = open('field.json', 'r')
    content = f.read()
    f.close()
    fields = json.loads(content)
    csvfile = open('field School rank.csv', 'a', encoding='utf-8',newline='')
    fp = csv.DictWriter(csvfile, fieldnames=["University", "ranking", "field"])
    fp.writeheader()
    for field in fields["field"]:
        rank = 1
        for page in range(1, 8):
            try:
                datas,rank = get_school(field, page,rank)
                fp.writerows(datas)
            except Exception as e:
                print("no more university：", e)
                break
    csvfile.close()

# pagingSave()
singleSave()
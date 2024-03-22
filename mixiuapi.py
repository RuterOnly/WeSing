
import time
import requests
import re

def getWeSingInfo(id:str):
    """
    用全民K歌用户ID获取全民K歌用户基础信息
    """
    WeSingInfo = {
        '头像':'',
        '昵称':'',
        '等级':'',
        '信息':'',
        '性别':'',
        '年龄':'',
        '地区':'',
        '作品数':'',
        '粉丝数':'',
        '关注数':'',
    }
    try:
        URL = 'https://node.kg.qq.com/personal?uid=' + id
        resp = requests.get(
            URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
        # print(resp.content.decode("utf-8"))
        if resp.status_code == 200:
            text = resp.content.decode("utf-8")
            re_ = "分享([\s\S]*?)的个人主页[\s\S]*?作品: (.*?); 粉丝: (.*?); 关注: (.*?)\"[\s\S]*?<meta itemprop=\"image\" content=\"(.*?)\" />[\s\S]*?icon_level_big icon_lb(.*?)\"[\s\S]*?<div class=\"my_show__info\">([\s\S]*?)<span class=\"icon icon_(.*?)\"></span>([\s\S]*?)岁([\s\S]*?)</div>[\s\S]*?<!-- 粉丝 关注 数-->"
            group = re.search (re_, text)
            if group == None:return
            groups =  group.groups()
            WeSingInfo['昵称'] = groups[0]
            WeSingInfo['作品数'] = groups[1]
            WeSingInfo['粉丝数'] = groups[2]
            WeSingInfo['关注数'] = groups[3]
            WeSingInfo['头像'] = groups[4]
            WeSingInfo['等级'] = groups[5]
            WeSingInfo['信息'] = groups[6].strip()
            WeSingInfo['性别'] = groups[7]
            WeSingInfo['年龄'] = groups[8].strip()
            WeSingInfo['地区'] = groups[9].strip()
    except:
        pass 

    return WeSingInfo

       

def getWeSingList(id:str,pages:str):
    """
    用全民K歌用户ID得到歌曲列表
    """
    times =  str(int(round(time.time() * 1000)))
    print(times)
    try:
        URL = 'http://cgi.kg.qq.com/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_0&inCharset=GB2312&outCharset=utf-8&g_tk=5381&g_tk_openkey=5381&type=get_uinfo&start=' + pages + '&num=10&touin=&share_uid=' + id + '&_= ' + times
        resp = requests.get(
            URL,
            headers={
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Language': 'zh-cn',
                'Referer': 'http://cgi.kg.qq.com',
                })
        if resp.status_code == 200:
            text = resp.content.decode("utf-8")
            re_ =  re.compile("\"ksong_mid\":([\s\S]*?)\",[\s\S]*?\"shareid\":([\s\S]*?)\",[\s\S]*?\"time\":([\s\S]*?),[\s\S]*?\"title\":([\s\S]*?)\",")
            
            group = re_.finditer(text)
            # 只能匹配第一个
            # group = re.search (re_, text)
            if group == None:return
            WeSingList = []
            for content in group:
                WeSingSing = {
                '歌名':'',
                '发布时间':'',
                '歌曲地址':'',
                '歌词地址':'', }
                WeSingSing['歌名'] = content[4].replace('"', '').strip()
                WeSingSing['发布时间'] = content[3].replace('"', '').strip()
                WeSingSing['歌曲地址'] = 'http://node.kg.qq.com/play?s=' + content[2].replace('"', '').strip()
                txt  = content[1].replace('"', '').strip()
                WeSingSing['歌词地址'] = f"http://node.kg.qq.com/cgi/fcgi-bin/fcg_lyric?jsonpCallback=callback_0&g_tk=360831677&outCharset=utf-8&format=jsonp&ksongmid={txt}&g_tk_openkey=360831677&_=1513746815547"
                WeSingList.append(WeSingSing) 
           
    except:
        pass 

    return WeSingList



def remove_html(string):
    regex = re.compile(r'<[^>]+>')
    return regex.sub('', string)

def getWeSingSingText(url:str):
    """
    用全民K歌歌曲地址获取全民K歌歌曲基础信息
    """
    WeSingInfo = {
        '简介':'',
        '封面':'',
        '分数':'',
        '收听量':'',
        '评论量':'',
        '歌曲地址':''
    }
    try:
        URL = url
        resp = requests.get(
            URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},timeout = 30)
        # print(resp.content.decode("utf-8"))
        if resp.status_code == 200:
            text = resp.content.decode("utf-8")
            re_ = "<img class=\"album_img\" style=\"display: block;\" src=\"([\s\S]*?)\" />[\s\S]*?<i class=\"icon icon_ear\"></i>([\s\S]*?)<i class=\"icon icon_talk\"></i>([\s\S]*?)<i class=\"icon icon_cup\"></i>([\s\S]*?)\n[\s\S]*?<p class=\"singer_say__cut\">([\s\S]*?)</p>[\s\S]*?\"playurl\":\"([\s\S]*?)\""
            group = re.search (re_, text)
            if group == None:return
            groups =  group.groups()
            WeSingInfo['简介'] = remove_html(groups[4].strip())
            WeSingInfo['封面'] = remove_html(groups[0].strip())
            WeSingInfo['分数'] = remove_html(groups[3].strip())
            WeSingInfo['收听量'] = remove_html(groups[1].strip())
            WeSingInfo['评论量'] = remove_html(groups[2].strip())
            WeSingInfo['歌曲地址'] = groups[5].strip()
    except:
        pass 

    return WeSingInfo

def getWeSingSongLyrics(url:str):
    """
    用全民K歌歌词地址获取全民K歌歌词信息
    """
    texts = ''
    try:
        URL = url
        resp = requests.get(
            URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
        if resp.status_code == 200:
            text = resp.content.decode("utf-8")
            re_ = "lyric\":\"([\s\S]*?)\"}}"
            group = re.search (re_, text)
            if group == None:return
            groups =  group.groups()
            texts =  groups[0].strip()
    except:
        pass 
    return texts


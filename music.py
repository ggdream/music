import requests,json,execjs,codecs,time,re
from urllib.request import quote
# from threading import Thread   不加多线程一是为了两种方案代码调整时更方便，二是因为爬取的数据量不多。想要更快运行可以加上
from prettytable import PrettyTable

"""
一、********************************************************QQ音乐**********************************************************
1：获取歌曲mid属性值的api接口：https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=&n=&w=&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0
                                    注：参数searchid由JS源码的“Math.random()”生成并经过“replace('0.','')”等处理，参数p和n分别是页和数量，参数w是我们输入的内容
2:获取歌曲下载地址参数的api接口：https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5165537029515912g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=
    {"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"4776407682","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"4776407682","songmid":["0039pE7x1okPVP"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}
    注：guid是固定值，跟cookie有一些关系。只有一个参数songmid，即第一个api获取到的mid
data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"4776407682","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"4776407682","songmid":["000qJ4H21yDGVW"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}
data传入时必须用json.dumps方法序列化data中的字典和列表。

二、*******************************************************网易云音乐*******************************************************
1.JS加密源码的api接口：https://s3.music.126.net/web/s/pt_frame_index_602f2359d1be3191cc19c9d1c0c170df.js?602f2359d1be3191cc19c9d1c0c170df(不需要data)
2.获取歌曲地址的api接口：https://music.163.com/weapi/cloudsearch/get/web?csrf_token=和
                      https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=(data分别为1.params，2.encSecKey。都经过了JS加密)
Js中说明4个参数来源的源码:var bUS5X=window.asrsea(JSON.stringify(i6c),bry8q(["流泪","强"]),bry8q(Sj0x.md),bry8q(["爱心","女孩","惊恐","大笑"]));e6c.data=k6e.cx7q({params:bUS5X.encText,encSecKey:bUS5X.encSecKey})
源码里window.asrsea=d，所以这四个参数对应d函数里的（d,e,f,g）：
    Sj0x.emj={"色":"00e0b","流感":"509f6","这边":"259df","弱":"8642d","嘴唇":"bc356","亲":"62901","开心":"477df","呲牙":"22677","憨笑":"ec152","猫":"b5ff6","皱眉":"8ace6","幽灵":"15bb7","蛋糕":"b7251","发怒":"52b3a","大哭":"b17a8","兔子":"76aea","星星":"8a5aa","钟情":"76d2e","牵手":"41762","公鸡":"9ec4e","爱意":"e341f","禁止":"56135","狗":"fccf6","亲亲":"95280","叉":"104e0","礼物":"312ec","晕":"bda92","呆":"557c9","生病":"38701","钻石":"14af6","拜":"c9d05","怒":"c4f7f","示爱":"0c368","汗":"5b7a4","小鸡":"6bee2","痛苦":"55932","撇嘴":"575cc","惶恐":"e10b4","口罩":"24d81","吐舌":"3cfe4","心碎":"875d3","生气":"e8204","可爱":"7b97d","鬼脸":"def52","跳舞":"741d5","男孩":"46b8e","奸笑":"289dc","猪":"6935b","圈":"3ece0","便便":"462db","外星":"0a22b","圣诞":"8e7","流泪":"01000","强":"1","爱心":"0CoJU","女孩":"m6Qyw","惊恐":"8W8ju","大笑":"d"}
    Sj0x.md=["色","流感","这边","弱","嘴唇","亲","开心","呲牙","憨笑","猫","皱眉","幽灵","蛋糕","发怒","大哭","兔子","星星","钟情","牵手","公鸡","爱意","禁止","狗","亲亲","叉","礼物","晕","呆","生病","钻石","拜","怒","示爱","汗","小鸡","痛苦","撇嘴","惶恐","口罩","吐舌","心碎","生气","可爱","鬼脸","跳舞","男孩","奸笑","猪","圈","便便","外星","圣诞"]
    i6c={"大笑":"86","可爱":"85","憨笑":"359","色":"95","亲亲":"363","惊恐":"96","流泪":"356","亲":"362","呆":"352","哀伤":"342","呲牙":"343","吐舌":"348","撇嘴":"353","怒":"361","奸笑":"341","汗":"97","痛苦":"346","惶恐":"354","生病":"350","口罩":"351","大哭":"357","晕":"355","发怒":"115","开心":"360","鬼脸":"94","皱眉":"87","流感":"358","爱心":"33","心碎":"34","钟情":"303","星星":"309","生气":"314","便便":"89","强":"13","弱":"372","拜":"14","牵手":"379","跳舞":"380","禁止":"374","这边":"262","爱意":"106","示爱":"376","嘴唇":"367","狗":"81","猫":"78","猪":"100","兔子":"459","小鸡":"450","公鸡":"461","幽灵":"116","圣诞":"411","外星":"101","钻石":"52","礼物":"107","男孩":"0","女孩":"1","蛋糕":"337",18:"186","圈":"312","叉":"313"}
    d=JSON.stringify(i6c)，e=bry8q(["流泪","强"])，f=bry8q(Sj0x.md)，g=bry8q(["爱心","女孩","惊恐","大笑"])，可以看出来，d不固定，e、f和g都是固定值
JS后四个参数至少由表情字符拼接而成（stringify有s、ids等内容的掺杂并和i6c表情集有关，bryq8在源码中定义为拼接函数），把JS化为python代码，并输出e，f，g结果：
    e='010001'
    f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    g='0CoJUm6Qyw8W8jud'
d参数JS代码过于复杂，所以我选择了打断点，看后台打印出的d值，找他的规律。果然，找到了规律：
    1：接口https://music.163.com/weapi/cloudsearch/get/web?csrf_token=的d值规律：
        d={hlpretag:"<span class = "s-fc7">",hlposttag:"</span>",s:"",type:"1",csrf_token:"",total:"true",offset:"0"}
        注：其中s为歌曲名称url编码值，其他均为固定值
    2：接口https://music.163.com/weapi/song/enhance/player/url?csrf_token=的d值规律：
        d={'ids': "", 'br': 320000, 'csrf_token': ""}
        注：其中ids为歌曲的id（api一最重要的作用就是获取这个值）；br值代表音质，有两个值（320000,128000），就用最好的320000（均为mp3格式）。
        96000值(标准)的歌曲连接在另一个api中（api：https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=）这里不多说了（这个是m4a格式）。
        
三、******************************************************酷我音乐**********************************************************
1：获取歌曲rid的api接口:http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=&pn=&rn=&reqId=（key值经过url编码）
2：获取歌曲地址的api接口:http://www.kuwo.cn/url?format=mp3&rid=&response=url&type=convert_url3&br=128kmp3&from=web&t=&reqId=
                       （rid由第一个api接口获取，pn是第几页，rn是当夜歌曲数量，t为1000倍时间戳的整数部分）

四、**************************************************酷狗音乐**************************************************************
1、获取歌曲hash的api接口：https://songsearch.kugou.com/song_search_v2?callback=jQuery1124037741722730857785_%d&keyword=%s&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=%d
                        （注：共三个参数，即两个时间戳(相差2)和一个歌名的url编码。获取FileHash值）
2、获取歌曲play_url的api接口：https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery1910019528111140116433_%d&hash=%s&album_id=&dfid=%s&mid=%s&platid=4&_=%d
                             （注：共五个参数，即两个时间戳(相差1)、接口一获取到的FileHash、cookie里的kg_dfid和kg_mid）
jQuery callback是回调函数，是随机值。不带着也可以访问，但是怕服务器以此作为反爬识别措施之一，还是带上为好
"""


#                       源码如下：
'''
*******************************************************QQ音乐************************************************************
'''
class QQMusic():
    def __init__(self,name):
        self.name=name
    def get_mid(self):
        url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=57951070373539875&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%s&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'%quote(self.name)
        headers={
            'Referer':'https://y.qq.com/portal/search.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response=json.loads(requests.get(url=url,headers=headers).content.decode('utf-8'))['data']['song']['list']
        return [x['mid'] for x in response],list(map(lambda x:['QQ',''.join(x['title'].split()),'/'.join([i['name'] for i in x['singer']])],response))
    def sprider(self):
        songmids,informations=self.get_mid()
        for songmid,information in zip(songmids,informations):
            data='%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%224776407682%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%224776407682%22%2C%22songmid%22%3A%5B%22'+songmid+'%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
            url='https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey23927290711706184&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%s'%data
            headers={
                'Referer':'https://y.qq.com/portal/player.html',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            response=json.loads(requests.get(url=url,headers=headers).content.decode('utf-8'))['req_0']['data']
            if response['midurlinfo'][0]['purl']!='':
                URL=response['sip'][0]+response['midurlinfo'][0]['purl']
                information.append(URL)
            else:
                information.append('-'*180)
        return informations
"""
******************************************************网易云音乐*********************************************************
"""
class CloudMusic():
    def __init__(self,name):
        self.name=name
        self.e='010001'
        self.f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g='0CoJUm6Qyw8W8jud'
    def get_data(self,d):
        self.d =d
        with open('cloud.js', encoding='utf-8')as f:
            JS = f.read()
        data_ = execjs.compile(JS).call('d', self.d, self.g)
        self.i=data_['A'][::-1]
        data={
            'params': data_['encText'],
            'encSecKey': format(int(codecs.encode(self.i.encode('utf-8'), 'hex_codec'), 16) ** int(self.e, 16) % int(self.f, 16), 'x').zfill(256)
        }
        return data
    def  get_id(self):
        url='https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        headers={
            'Referer':'https://music.163.com/search/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        d='{hlpretag:"<span class = \'s-fc7\'>",hlposttag:"</span>",s:"%s",type:"1",csrf_token:"",total:"true",offset:"0"}'%self.name
        response=json.loads(requests.post(url=url,headers=headers,data=self.get_data(d)).content.decode('utf-8'))['result']['songs']
        return [x['id'] for x in response],list(map(lambda x:['网易云',x['name'],'/'.join([i['name'] for i in x['ar']])],response))
    def sprider(self):
        IDs,informations=self.get_id()
        for ID,information in zip(IDs,informations):
            url='https://music.163.com/weapi/song/enhance/player/url?csrf_token='
            headers={
                'Referer':'https://music.163.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            d=str({'ids':"[%s]"%str(ID),'br':320000,'csrf_token':""})
            response = json.loads(requests.post(url=url, headers=headers, data=self.get_data(d)).content.decode('utf-8'))['data'][0]['url']
            if response!='':
                information.append(response)
            else:
                information.append('-'*180)
        return informations
"""
*******************************************************酷我音乐**********************************************************
"""
class CoolMeMusic():
    def __init__(self,name):
        self.name =name
        self.headers = {
            'Referer': 'http://www.kuwo.cn/search/list?key=%s' % quote(self.name),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    def get_id(self):
        url='http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%s&pn=1&rn=30&reqId='%(quote(self.name))
        response=json.loads(requests.get(url=url,headers=self.headers).content.decode('utf-8'))['data']['list']
        return [x['rid'] for x in response],list(map(lambda x:['酷我',x['name'],x['artist']],response))
    def sprider(self):
        rids,informations=self.get_id()
        for rid,information in zip(rids,informations):
            url='http://www.kuwo.cn/url?format=mp3&rid=%d&response=url&type=convert_url3&br=128kmp3&from=web&t=%d&reqId='%(rid,int(time.time()*1000))
            response=json.loads(requests.get(url=url,headers=self.headers).content.decode('utf-8'))['url']
            if response!='':
                information.append(response)
            else:
                information.append('-'*180)
        return informations
"""
*******************************************************酷狗音乐**********************************************************
"""
class CoolDogMusic():
    def __init__(self,name):
        self.name=name
        self.dfid='1aAcF31Utj2l0ZzFPO0Yjss0'
        self.mid='7df6a46dd0a23d920fe7929f492ef251'
    def get_id(self):
        url='https://songsearch.kugou.com/song_search_v2?callback=jQuery1124018638456262994435_%d&keyword=%s&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=%d'%(
            int(time.time()*1000)-2,quote(self.name),int(time.time()*1000))
        headers={
            'Referer':'https://www.kugou.com/yy/html/search.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response=json.loads(re.findall('[(](.*)[)]',requests.get(url=url,headers=headers).content.decode('utf-8'))[0])['data']['lists']
        return [x['FileHash'] for x in response],list(map(lambda x:['酷狗',x['SongName'].replace('<em>','').replace('</em>',''),x['SingerName']],response))
    def sprider(self):
        Hashs,informations=self.get_id()
        for Hash,information in zip(Hashs,informations):
            url='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107306344625120932_%d&hash=%s&album_id=&dfid=%s&mid=%s&platid=4&_=%d'%(
                int(time.time()*1000)-1,Hash,self.dfid,self.mid,int(time.time()*1000))
            headers={
                'Referer':'https://www.kugou.com/song/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko'
            }
            proxies={
                'https':'39.104.62.226:8080'
            }
            response=json.loads(re.findall('[(](.*)[)]', requests.get(url=url, headers=headers,proxies=proxies).content.decode('utf-8'))[0])['data']['play_url']
            if response!='':
                information.append(response)
            else:
                information.append('-'*180)
        return informations


def start(name):
    a=QQMusic(name)
    b=CloudMusic(name)
    c=CoolMeMusic(name)
    d=CoolDogMusic(name)
    print('>>开始爬取QQ音乐')
    a_=a.sprider()
    print('>>开始爬取网易云音乐')
    b_=b.sprider()
    print('>>开始爬取酷我音乐')
    c_=c.sprider()
    print('>>开始爬取酷狗音乐')
    d_=d.sprider()
    print('\n》全部爬取完成，正在整合数据!')
    ALL=a_+b_+c_+d_
    table=PrettyTable(['音乐源','歌曲名称','歌手名称','试听链接（打开即可下载）'])
    for i in ALL:
        table.add_row(i)
    print('\n','>>>>>>>>>歌曲：%s'%name)
    print(table)

if __name__ == '__main__':
    name=input('输入歌曲名称：')
    start(name)
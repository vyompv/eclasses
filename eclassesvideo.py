import bs4
import requests
import urllib
import urllib.request
import os
import pprint
import socket
from socket import error as SocketError, timeout as SocketTimeout
from bs4 import BeautifulSoup
from requests import session
from pprint import pprint

path = "C:/Workspace/"
headers={}
lit=True


def getcourses(name,link):
    global path,headers
    payload = {
        'username' : 'xxxxxx',
        'password' : 'xxxxxxx'
    }
    refer='http://wwwwwwwwwww.com'
    login_url='http://yyyyyy.com/index.htm'
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"
    headers['Referer']=refer
    with session() as c:
        
        request=c.post(login_url, headers=headers,data = payload)
        #print(request.headers)
        #print(request.text)
        path=path+"/videos"
        if not os.path.exists(path):
            os.mkdir(path)
        
        pw = request.text
        soup=BeautifulSoup(pw)
        #print(soup)
        vlinkarray=[]
        vtitlearray=[]
        for li in soup.findAll('div',{'class':'info'}):
                for links in li.find_all('a'):
                    vlinkarray.append(links.get('href'))
                title=clean(li.text)
                vtitlearray.append(title)
        i=1
        for ti,li in zip(vtitlearray,vlinkarray):
            print("Next courssectionlist "+ti) 
            if ti.find("CN-Problems") == -1: 
                    coursesectionlist(path+('/%0*d-' % (3, i))+ti,li,c)
                    i=i+1
        logout=[]
        for li in soup.findAll('div',{'class':'logininfo'}):
                for links in li.find_all('a'):
                    logout.append(links.get('href'))
        wp = urllib.request.urlopen(logout[1]) 

def coursesectionlist(name,link,c):
    #if(name.find("Theory_of_Computation")==-1):
     #  return
    global lit
    print(name+":")
    pat =name
    if not os.path.exists(pat):
        os.mkdir(pat)
    url=link
    wp = c.get(url,headers=headers)
    pw = wp.text
    soup=BeautifulSoup(pw)
    vlinkarray=[]
    vtitlearray=[]
    j=0
    if name.find("Graph_Ther") != -1:
        for links in soup.findAll('div',{'class':'activityinstance'}):
            vlinkarray.append(links.contents[j]['href'])
            title=clean(links.text.replace(' Page',''))
            vtitlearray.append(title)
    #print(soup)
    #print(soup.prettify())
    for links in soup.findAll('h3',{'class':'section-title'}):
        vlinkarray.append(links.contents[j]['href'])
        title=clean(links.text)
        vtitlearray.append(title)
    i=1
    for ti,li in zip(vtitlearray,vlinkarray):
        print("Next coursesectiontitle "+ti) 
        if ti.find("Practice_questions") == -1: 
            if ti.find("Practice_Questions") == -1:
                #if ti.find("Properties_of_CFL_s") != -1:
                    coursesectiontitlelist(pat+('/%0*d-' % (3, i))+ti,li,c)
                    i=i+1
        


def coursesectiontitlelist(name,link,c):
    pat =name
    if not os.path.exists(pat):
        os.mkdir(pat)
    url=link
    wp = c.get(url,headers=headers)
    pw = wp.text
    soup=BeautifulSoup(pw)
    #print(soup)
    vlinkarray=[]
    vtitlearray=[]
    for li in soup.findAll('li',{'class':'type_activity'}):
            for links in li.find_all('a'):
                vlinkarray.append(links.get('href'))
            title=clean(li.text)
            vtitlearray.append(title)
    i=1
    for ti,li in zip(vtitlearray,vlinkarray):
       print("Next video "+ti) 
       if ti.find("Normalization_practice_questions_set_1") == -1:  
          if ti.find("Solutions_to_practice_set_1") == -1: 
            if ti.find("Practice_questions_on_transactions-1") == -1:
                if ti.find("Solutions_to_questions_on_transactions-1") == -1:
                    if ti.find("Practice_Questions_Set_1") == -1:
                        if ti.find("Solutions_to_Set_1") == -1:
                                print(pat)
                                video(pat,('%0*d-' % (3, i)),li,c)
                                i=i+1


def video(pat,name,link,c):
    url=link
    wp = c.get(url,headers=headers)
    pw = wp.text
    soup=BeautifulSoup(pw)
    title=soup.find("div", {"role": "main"}).h2.string
    title=name+title
    title=clean(title)
    print(pat+"/"+title)
    universities=soup.findAll('iframe')
    soup = BeautifulSoup(pw)
    #print(soup)
    refer=url
    for link in universities:
            linksrc=link.attrs['src']
            #response.close()
            response=c.get(linksrc,headers=headers)
            content = response.text
            #print(content)
            content_list = content.splitlines(True)
            #pprint(content_list)
            #print(content_list[0])
           
            str=content_list[0]
            str_list=str.split(',')
            if len(str_list)<15:
                if not os.path.exists(pat+'/'+title+'.mp4'):
                    print("Youtube:"+title)
                    open(pat+'/'+title+'.mp4', "w").close()
                break    
            
            if("ns3.pdl-secure" in str):
                print("secured-link-> "+str.split("ns3.pdl-secure\",")[1].split(",")[0].split(":\"")[1].split("\"")[0])
                str1=str.split("ns3.pdl-secure\",")[1].split(",")[0].split(":\"")[1].split("\"")[0]
            elif("ns3.pdl" in str):
                print("link-> "+str.split("ns3.pdl")[1].split(",")[1].split(":\"")[1].split("\"")[0])
                str1=str.split("ns3.pdl")[1].split(",")[1].split(":\"")[1].split("\"")[0]
            if os.path.exists(pat+'/'+title+'.mp4'):
                if os.path.getsize(pat+'/'+title+'.mp4') > 100:
                    print("Already Downloaded")
                    break 
            DownloadThreadFunc(str1,(pat+'/'+title+".mp4"))        

def DownloadThreadFunc(self,name):
    try:
        handle = urllib.request.urlopen(self)
        meta=handle.info()
        print(meta)
        meta.size = int(handle.info()["Content-Length"])
        meta.actualSize = 0
        blocksize = 64*1024
        fo = open(name, "wb")
        while meta.actualSize!=meta.size:
            block = handle.read(blocksize)
            meta.actualSize += len(block)
            if len(block) == 0:
                break
            fo.write(block)
        fo.close()
    except (urllib.URLError, socket.timeout) as e:
        try:
            fo.close()
        except:
            pass
        error("Download failed.", unicode(e))  
            
def clean(text):
    text=text.strip()    
    for ch in ['__','___']:
        text=text.replace(ch,"_")    
        for ch in ['__','-_-']:
            text=text.replace(ch,"_")
            for ch in ['-_','_-','--',':']:
                text=text.replace(ch,"-")
                for ch in ['\\','`','*','_','{','}','[',']','(',')','>','#','+','.','!','$','\'',' ','/','?',',','|']:
                    text = text.replace(ch,"_")
    for ch in ['__','___']:
        text=text.replace(ch,"_")    
    return text

print("Downloading Videos...")            
urlcourses="http://wwwwwwwwwww.com"
getcourses('test',urlcourses)  
print("Download Successfully Completed")          
import requests
from bs4 import BeautifulSoup
import codecs
import time
import datetime
import threading
import time
dataz=[]
class myThread (threading.Thread):
    def __init__(self,page):
        threading.Thread.__init__(self)
        self.page = page
    def run(self):
          global dataz
          extractPage(self.page)

# Dont use this one! Outdated. Has no Threading and takes forever. Only for testing
def vtCrawler(root):
    output = codecs.open("posts.txt","w","utf-8-sig")
    glue = "?page="
    data=[]
    tiem = time.time()

    for times in range(1,100):
        print(root+glue+str(times))
        web = requests.get(root+glue+str(times))
        soup = BeautifulSoup(web.text,"html.parser")
        topics = soup.find("div",{"id":"contentDiv"})
        try:
            dalton = soup.find("div",class_="center msg").contents[1].text
            print("Dalton")
            web = requests.get(root+glue+str(times))
            soup = BeautifulSoup(web.text,"html.parser")
            topics = soup.find("div",{"id":"contentDiv"})
        except: print("Tudo Bem")
        finally:
            try:
              for topic in topics.contents[3].contents[1].contents[5].contents:
                if(len(topic) > 2):
                    topicurl = topic.contents[3].contents[1].contents[1].attrs['href']
                    print(topicurl)
                    data.append(extractTopic(root+topicurl))
            except:
               print("error")


    for topic in data:
        if(topic is not None):
            try:
                for post in topic:
                    post = post + "\n"
                    output.write(post)
            except:
              print("none")
        else:
             pass
    output.close()
    print("============time============", time.time() - tiem)

#The function below uses Threading. Still working on it.
def crawl():
    tiem = time.time()
    output = codecs.open("posts.txt","w","utf-8-sig")
    glue = "?page="
    root = "http://forum.jogos.uol.com.br/vale-tudo_f_57"
    for g in range(1,5):
      bagofThreads = []
      tiea = g * 100
      if(g != 1): v = v + 100
      else: v = 1

      for p in range(v,tiea):
        tr = myThread(root+glue+str(p))
        bagofThreads.append(tr)

      for t in bagofThreads:
        t.start()

      time.sleep(500)

      for t in bagofThreads:
        t.join()

    for topic in dataz:
        if(topic is not None):
            try:
                for post in topic:
                    post = post + "\n"
                    output.write(post)
            except:
              print("none")
        else:
             pass
    output.close()
    print("============time============", time.time() - tiem)

def extractPage(vtp):
    global dataz
    tries=0
    glue="http://forum.jogos.uol.com.br/vale-tudo_f_57"
    web = requests.get(vtp)
    soup = BeautifulSoup(web.text,"html.parser")
    topics = soup.find("div",{"id":"contentDiv"})
    while(tries < 6):
      try:
          dalton = soup.find("div",class_="center msg").contents[1].text
          web = requests.get(vtp)
          soup = BeautifulSoup(web.text,"html.parser")
          topics = soup.find("div",{"id":"contentDiv"})
          tries = tries + 1
          print("try number: ", tries)
      except:
          tries=7
    try:
        for topic in topics.contents[3].contents[1].contents[5].contents:
            if(len(topic) > 2):
                topicurl = topic.contents[3].contents[1].contents[1].attrs['href']
                print(topicurl)
                dataz.append(extractTopic(glue+topicurl))
    except:
        print("Topics Not found")

def extractTopic(url):
    page=1
    maxpage=0
    limit= 40
    glue="?page="
    topicPosts=[]
    web = requests.get(url)
    soup = BeautifulSoup(web.text,"html.parser")
    pages = soup.find("div",{"id":"paginacao"})
    maxpage = findLastPage(pages)
    if(maxpage > 40): return

    while((page-1 < maxpage) & (page-1 < limit)):
      print("page: ", page, "max page:", maxpage)
      topicPosts.append("====================================== page "+str(page)+" ======================================")
      web = requests.get(url+glue+str(page))
      soup = BeautifulSoup(web.text,"html.parser")
      body = soup.find("div",class_="autoClear posts-container")
      extractPosts(body,topicPosts)
      page = page + 1

    return topicPosts

def extractPosts(body,topicPosts):
    for i in body.contents:
            if((i is not None) & (i != "\n")):
                 if(len(i.contents)>1):
                     userInfo = i.contents[1].contents
                     userName = userInfo[1].contents[1].text.replace("\n","")
                     try:
                         postdate = userInfo[3].contents[3].contents[1].text[25:-1]
                         userText = userInfo[3].contents[5].text.replace("\t","").replace("\n","")
                     except:
                         postdate = '12/12/1999 xx:xx'
                         userText = userInfo[3].contents[3].text.replace("\t","").replace("\n","")

                     topicPosts.append(userName+"\t"+postdate+"\t"+userText)

def findLastPage(pages):
    max=0
    text = pages.text
    text = text.replace("\t"," ")
    text = text.replace("\n"," ")
    for i in text.split(" "):
      try:
          cur = int(i)
          if(cur > max): max = cur
      except:
          pass
    return max

def hasuser(dic,user):
    if(user in dic): return dic[user]
    else: return ""


#Functions to measure users
def averageTime():
    users={}
    usersMeanTime={}
    posts = codecs.open("posts.txt",encoding="utf8")
    for i in posts.readlines():
        if(len(i.split("\t"))<2):pass
        else:
            i = i.split("\t")
            date = i[1].split(" ")
            if((len(date) == 2)):
               if(date[1] != "xx:xx"):
                   users[i[0]] = hasuser(users,i[0]) + " " + date[1]

    for u in users:
        auxtime = 0
        n=0
        for ti in users[u].split(" "):
           if((ti != '"') & (ti != "")):
               n = n + 1
               ti = ti.split(":")
               auxtime = auxtime + float(ti[0]) + float(ti[1])/60
        auxtime = auxtime/n
        auxtime = str(round(auxtime,2))
        asplit = auxtime.split(".")
        n1 = float(asplit[0])
        n2 = float(asplit[1])
        if(n2 > 59):
            n1 = n1 + 1
            ax = n2 - 60
            n1 = str(int(n1))
            n2 = int(ax)

            if((n2 > 9) & (len(str(n2)) == 1)):
                n2 = str(n2)
            elif(len(str(n2))== 1):
                n2 = "0"+str(n2)
            if(len(n1)==1): n1 = "0"+n1

            auxtime = n1+":"+str(n2)
        else:
            n1 = str(int(n1))
            n2 = int(n2)
            if((n2 > 9) & (len(str(n2)) == 1)):
                n2 = str(n2)+"0"
            elif(len(str(n2)) == 1):
                n2 = "0"+str(n2)

            if(len(n1)==1): n1 = "0"+n1

            auxtime = n1+":"+str(n2)
        usersMeanTime[u] = auxtime
    return usersMeanTime

def timePeriod(path):
    users={}
    usersperiod={}
    posts = codecs.open(path,encoding="utf8")
    for i in posts.readlines():
        if(len(i.split("\t"))<2):pass
        else:
            i = i.split("\t")
            date = i[1].split(" ")
            if((len(date) == 2)):
               if(date[1] != "xx:xx"):
                   users[i[0]] = hasuser(users,i[0]) + " " + date[1]

    for u in users:
        mor=0
        non=0
        nigh=0
        madr=0
        n=0.0
        for us in users[u].split(" "):
          if(len(us.split(":"))>1):
           n = n + 1.0
           n1 = int(us.split(":")[0])
           if(0<=n1<=5):
               madr= madr + 1
           elif(5<n1<12):
               mor = mor + 1
           elif(12<=n1<17):
               non = non + 1
           elif(17<=n1<24):
               nigh = nigh + 1
        madr = round(100 * (madr/n),2)
        non = round(100 * (non/n),2)
        nigh = round(100 * (nigh/n),2)
        mor = round(100 * (mor/n),2)
        usersperiod[u] = [str(mor)+"%",str(non)+"%",str(nigh)+"%",str(madr)+"%",str(n)]
    print("Periodos que os users abaixo postam: ")
    for u in usersperiod:
        aux = usersperiod[u]
        printstring = u + ": manha(" + aux[0] + ") " + "tarde(" + aux[1] + ")"
        printstring = printstring + " noite(" + aux[2] + ") " + "madrugada(" + aux[3] + ")" + " posts: " + aux[4]
        print(printstring)


#vtCrawler("http://forum.jogos.uol.com.br/vale-tudo_f_57")
#timePeriod("posts2.txt")
crawl()



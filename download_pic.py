# coding:utf8
import requests, urllib,urllib2
from bs4 import BeautifulSoup
import os
import time
import socket

#url = 'http://cl.wm3.lol/htm_data/8/1704/2335131.html'
#path='d:/pachong111/'

# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

def download_pic(url,path):#下载某一个帖子中图片
    source_code = requests.get(url)
    plain_text = source_code.text
    Soup = BeautifulSoup(plain_text, 'lxml')
    download_links = []
    foler_path=path
    images = Soup.find_all('input')

    for pic_tag in Soup.find_all('input'):
        if pic_tag.get('src') != None:
            pic_link = pic_tag.get('src')
            #print pic_link
            pic_link=str(pic_link).strip()
            download_links.append(pic_link)
    i=0
    #print '下载新帖子了,帖子名字是： '+str(path)+'  帖子的链接是 '+str(url)
    print path,url
    for item in download_links:
        socket.setdefaulttimeout(10)  # 10秒内没有打开web页面，就算超时
        try:
            i=i+1
            urllib.urlretrieve(item, foler_path + item[-10:])
            print ('下载第 '+str(i)+' 张图成功！ 图片是 '+item)
        except Exception as e:
            print '下载第 '+str(i)+' 张图超时！ 图片是 '+item


def getnexturls(rooturl):#获取这一页所有帖子的url
    source_code = requests.get(rooturl)
    source_code.encoding = 'gb2312'
    plain_text = source_code.text 
    Soup = BeautifulSoup(plain_text, 'lxml')
    titles = Soup.select('tbody > tr > td.tal > h3 > a')
    errors = Soup.select('td.tal > h3 > a > b > font')
    # print len(errors)
    # for e in errors:
    #      print e.get_text()
    # reals= list(set(titles)^set(errors)) #titles集合删除errors集合
    reals = titles[8:]  # 直接过滤前八个

    # for i in titles:
    #     if i not in errors:
    #         reals.append(i)
    nexturls=[]
    for real in reals:  # 创建对应的文件夹
        nexturls.append('http://cl.wm3.lol/'+real.get('href'))
    return nexturls

def createdir(rooturl,rootpath):  #获取这一页所有帖子的标题并创建对应的目录
    source_code = requests.get(rooturl)
    source_code.encoding = 'gb2312'
    plain_text = source_code.text
    Soup = BeautifulSoup(plain_text, 'lxml')
    titles = Soup.select('tbody > tr > td.tal > h3 > a')
    errors = Soup.select('td.tal > h3 > a > b > font')
    # print len(errors)
    # for e in errors:
    #      print e.get_text()
    # reals= list(set(titles)^set(errors)) #titles集合删除errors集合
    reals = titles[8:]  # 直接过滤前八个  只需要针对第一页
    '''#ajaxtable > tbody:nth-child(2) > tr:nth-child(11) > td.tal > h3 > a > b > font
    #ajaxtable > tbody:nth-child(2) > tr:nth-child(13) > td.tal > h3 > a
    '''
    nexturls=[]
    dirpath=[]
    # for i in titles:
    #     if i not in errors:
    #         reals.append(i)
    folder = rootpath
    #os.mkdir(folder)#先创建根目录
    for real in reals:  # 创建对应的文件夹
        try:
            os.mkdir(folder+unicode(real.get_text()).replace('!','').replace('"','').replace('-',''))
            dirpath.append(folder+unicode(real.get_text()).replace('!','').replace('"','').replace('-','')+'/')
            nexturls.append('http://cl.wm3.lol/' + real.get('href'))
            #print 'success to create dir'
        except Exception as e:
            print 'fail to create dir ',folder+unicode(real.get_text())
    return nexturls,dirpath


def main():
    #rootpath='D:\\download111\\'#x下载到本地的地址
    #rooturl='http://cl.wm3.lol/thread0806.php?fid=8'#网址
    rooturl1 = 'http://cl.wm3.lol/thread0806.php?fid=8&search=&page={}'
    rootpath = 'd:/testdownload/'
    urls = [rooturl1.format(str(i)) for i in range(1, 101, 1)]
    i = 1
    os.mkdir(rootpath)
    for url in urls:
        folder=rootpath + u'第' + str(i) + u'页'+'\\'
        os.mkdir(folder)  # 中文前加一个u解决创建中文文件夹乱码问题
        nexturls,dirpath = createdir(url, folder)  # nexturls和dirpath 长度一致
        #print len(nexturls),len(dirpath)
        i = i + 1
        #print url
        time.sleep(2)
        for j in range(len(nexturls)):
            print nexturls[j],len(nexturls)
            download_pic(nexturls[j],dirpath[j])
            time.sleep(2)

    # nexturls = getnexturls(rooturl)
    # dirpath = createdir(rooturl,rootpath)#nexturls和dirpath 长度一致

    # for i in range(len(nexturls)):
    #     #print nexturls[i],dirpath[i][12:-6],len(nexturls)
    #     download_pic(nexturls[i],dirpath[i])
    #     time.sleep(2)



main()


# rooturl1='http://cl.wm3.lol/thread0806.php?fid=8&search=&page={}'
# urls=[rooturl1.format(str(i)) for i in range (1,101,1)]
# i=1
# rootpath='d:/testdownload/'
# os.mkdir(rootpath)
# for url in urls:
#     os.mkdir(rootpath + u'第' + str(i) + u'页')#中文前加一个u解决创建中文文件夹乱码问题
#     i=i+1
#     print url




# result = urllib2.urlopen('http://www.babehub.com/content/140305/1592-anna-leah-femjoy-11.jpg')  # 打开链接
# print result.getcode()
# socket.setdefaulttimeout(3)           #6秒内没有打开web页面，就算超时
# try:
#     urllib.urlretrieve('http://www.babehub.com/content/140305/1592-anna-leah-femjoy-11.jpg', 'D:\download\Anna Leah and Marta[24P]\\11.jpg')
# except Exception as e:
#     print "超时"
#
# print "success"
#createdir(rooturl,rootpath)
#download_pic(url,path)
# os.makedirs('d:/pachong/pachong')
# os.mkdir('d:/pachong111')
# folders=['d:/pachong/pachong{}'.format(str(i)) for i in range(0,10,1)]批量创建文件夹
# for folder in folders:
#     os.mkdir(folder)


# def A():
#     a=[1,2]
#     b=[2]
#     return a,b
# a,b=A()
# print a,b

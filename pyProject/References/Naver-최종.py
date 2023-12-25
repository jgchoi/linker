import os
import sys
import requests
from tkinter import ttk
from bs4 import BeautifulSoup
import urllib.request
from tkinter import messagebox


if __name__ == "__main__":
    id = input("id : ")
    links = []
    list = []
    os.makedirs("%s" %id, exist_ok = True)
    os.makedirs("%s/html" %id, exist_ok = True)
    os.makedirs("%s/삽화" %id, exist_ok = True)
    os.makedirs("%s/대화형 이미지" %id, exist_ok = True)


    for i in range(10000):
        fi = False
        get = requests.get(f"https://novel.naver.com/webnovel/list?novelId={id}&page={i+1}")

        soup = BeautifulSoup(get.text, "html.parser")

        for s in soup.select(".volumeComment"):
            link = f'https://novel.naver.com{s.select("a")[0].attrs["href"]}'
            if link in links:
                fi = True
                break
            links.append(link)

        if fi == True:
            break
    
    links.reverse()

    for i in links:
        tmplist = []
        req = requests.get(i)
        soup = BeautifulSoup(req.content, "html.parser")
        content_list = soup.find(class_="viewer_container nanum")
        #대화형 이미지 리스트 추가
        tmplist = soup.select("#content > div.section_area_viewer > div.viewer_container.nanum > div > p > a > img")
        for j in tmplist:
            if j not in list:
                list.append(j)
        #삽화 다운
        image = soup.select("#content > div.section_area_viewer > div.viewer_container.nanum > div > p > img")
        num = links.index(i) + 1
        if len(image) == 0:
            pass
        elif len(image) == 1 :
            img1 = image[0].get("src")
            urllib.request.urlretrieve(img1, "%s/삽화/%s_1.png" %(id, num))
        else:
            img1 = image[0].get("src")
            urllib.request.urlretrieve(img1, "%s/삽화/%s_1.png" %(id, num))
            img2 = image[1].get("src")
            urllib.request.urlretrieve(img2, "%s/삽화/%s_2.png" %(id, num))
    length = len(list)
        
    #대화형 이미지 다운
    for k in range (0, length):
        img = list[k].get("src")
        urllib.request.urlretrieve(img, "%s/대화형 이미지/%s.png" %(id, k+1))

    num = 1
    for i in links:
        req = requests.get(i)
        soup = BeautifulSoup(req.content, "html.parser")
        content = soup.find(class_="viewer_container nanum")
        sys.stdout = open("%s/html/%s.html" %(id, num),"w", encoding="UTF-8")
        print(content)
        sys.stdout.close()
        num = num + 1
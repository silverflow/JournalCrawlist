from bs4 import BeautifulSoup
import requests as rq
'''
중앙일보 기자 목록 페이지를 파싱해서 이름과 이메일을 가져오는 프로그램
'''
#함수 정의
#url의 body에 기자목록을 가져옴
def get_pages(bs):
    return bs.select('body .bd ul.list li')
#기자목록 중에서 이름과 이메일을 파싱함
def data_parse(pages):
    for page in pages:
        name = page.find('h2').text.strip()
        email = page.find('span', class_="icon_email").text.strip()
        print(name,email)

url= 'https://news.joins.com/Reporter'
page_path='?page=%d'
number = 2

res = rq.get(url)
bs = BeautifulSoup(res.content, 'lxml')
pages = get_pages(bs)
data_parse(pages)


while True:
    sub_path = page_path%(number)
    number += 1
    res = rq.get(url + sub_path)

    bs = BeautifulSoup(res.content, 'lxml')
    pages = get_pages(bs)

    if(len(bs.select('p.no_result'))>0):
        print("수집종료\n페이지가 끝남")
        break
    data_parse(pages)
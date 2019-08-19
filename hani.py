from bs4 import BeautifulSoup
import requests as rq
import DBConn
'''
19.08. v0.1
한겨례 전체 기사를 최근 약 2년간의 기사를 크롤링해서 이름과 메일주소를 파싱함
1. DB에 동일한 이름 && 이메일을 가진 경우에는 중복제거를 위해 DB에 insert하지 않음
2. 기자가 아닌경우 가져오지않음(교수거나 평론가 특파원 등)
3. 두명일 경우 앞에 사람 이름만 가져옴
4. 기자가 붙었고 이름도 있지만 이메일이 없는 경우는 가져오지 않음
5. 두글자인 경우가 있으니까 기자를 제외하고 한 단어로 가져오기
'''
#함수 정의
#url의 body에 기자목록을 가져옴
def get_pages(bs):
    return bs.findAll('div',{'class':'article-text'})
number = 798889
url= 'http://www.hani.co.kr/arti/%d.html' % number

res = rq.get(url)
bs = BeautifulSoup(res.content, 'lxml')
body = get_pages(bs)
for ele in body:
    name = ele.findAll('p')
    email = ele.find('a').get_text()
    print(name,email)
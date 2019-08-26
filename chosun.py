from bs4 import BeautifulSoup
import requests as rq
import DBConn
'''
19.08.19 v0.1
조선일보 기자 목록 페이지를 파싱해서 이름과 이메일을 가져오는 프로그램
중복제거 안한 버전
'''
#함수 정의
#url의 body에 기자목록을 가져옴
def get_pages(bs):
    return bs.select('.gizadb')
#기자목록 중에서 이름과 이메일을 파싱함
def data_parse(pages):
    for page in pages:
        name = page.find('td', class_="gizaName").text.strip()
        name = name.split('\n')[0]
        email = page.find('td', class_="gizaEmail").text.strip()
        email = email.split('\n')[0]
        curs.execute(sql, (name, email,"조선일보"))
        print(name,email)
#DB 커넥트 정보
conn = DBConn.conn()
#conect에서 cursor 생성
curs = conn.cursor()
#SQL문 실행 이름, 이메일, 언론사에 인서트하는 쿼리문
sql = ("INSERT INTO `journalistinfo` (`journal_name`, `journal_email`,`press`) VALUES (%s,%s,%s)")

url= 'https://nolooknews.com/db/search/belongto/%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4/'

res = rq.get(url)
bs = BeautifulSoup(res.content, 'lxml')
pages = get_pages(bs)
data_parse(pages)

#DB에 데이터 쓰기
conn.commit()
#DB 커넥트 닫기
conn.close()
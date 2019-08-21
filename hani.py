from os.path import split

import requests as rq
from bs4 import BeautifulSoup
import re
import DBConn

'''
19.08. v0.1
한겨례 전체 기사를 최근 약 2년간의 기사를 크롤링해서 이름과 메일주소를 파싱함
    1. DB에 동일한 이름 && 이메일을 가진 경우에는 중복제거를 위해 DB에 insert하지 않음
    2. 기자가 아닌경우 가져오지않음(교수거나 평론가 특파원 등)
    3. 두명일 경우 앞에 사람 이름만 가져옴
    4. 기자가 붙었고 이름도 있지만 이메일이 없는 경우는 가져오지 않음
    5. 두글자인 경우가 있으니까 기자를 제외하고 한 단어로 가져오기
크롤링 규칙
    1. 이메일과 기자 이름이 둘다 존재하고 경우에만 출력(교수나 논설위원 등 다 제외)
    2. 선임, 인턴기자 제외 근데 인턴기자는 어차피 한겨례 이메일주소가 없어서 이메일 체크단에서 걸러짐
    3. 이름이 여러개여도 제외
    4. 마지막으로 리스트에 넣은것 중복확인(이메일and이름이 같은 경우)하고 커밋
    5. 이름이 공백이면 날리기
'''
#함수 정의
#url의 body에 기자목록을 가져옴
def get_pages(bs):
    return bs.findAll('div',{'class':'article-text'})
def contains_word(t):
    return t and '기자' in t
#이메일 정규식
e_reg = re.compile('[a-zA-Z0-9._%+-]+@hani.co.kr')
#문장에 선임이 들어있는지 확인
j_reg = re.compile('선임')
#문장에 인턴이 들어있는지 확인
i_reg = re.compile('인턴')
#크롤링 시작값 1씩늘어남 17년도 기사부터 긁어옴
#number = 798890

number = 906500
db_list = [{}]
#while문 조건문에 크롤링을 끝마칠 최종 아티클 넘버를 입력
while number<906530:
    url= 'http://www.hani.co.kr/arti/%d.html' % number
    res = rq.get(url,timeout=1)
    bs = BeautifulSoup(res.content, 'lxml')
    body = get_pages(bs)
    for ele in body:
        number += 1
        #파싱한거 String으로 만들어줌
        content = ele.text.strip()
        #기자 이름 가져옴
        name = ele.find_all(text=contains_word)

        #페이지내에 이메일이 없을 경우 1차로 이메일 거름
        if(len(e_reg.findall(content))<1):
            print("이메일이 없구나")
            continue
        elif(len(name)>0):
            #기자 이름이 존재할 경우
            #맨 마지막 이메일만 가져옴
            email = e_reg.findall(content)[-1]


            #맨 마지막 기자만 선택 
            name = ele.findAll(text=contains_word)[-1]

            if(j_reg.findall(name) or i_reg.findall(name)):
                print("너는 필시 선임기자거나 인턴기자겠구나 그렇다면 썩 나가거라")
                continue
            else:
                #선임이나 인턴이 아닌 순수혈통 기자
                #기자 공백 글자빼기
                name = name.strip()
                name = name.split(' ')
                if(len(name)==2):
                    #리스트에서 기자찾아서 인덱스 넘버 변수저장
                    list_num = name.index('기자')
                    j_name = name[list_num-1]
                    db_list[name] = email
                    
                else:
                    print("기자 이름이 많아서 버림")
                    continue
        else:
            print("이메일이 존재하지만 기자이름이 없구만기래")
            continue
print(db_list)
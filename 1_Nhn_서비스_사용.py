#!/usr/bin/env python
# coding: utf-8

# ### 1. Nhn 뉴스 제목 검색
# * request, beautifulsoup 사용
# * css selector - attribute(속성 선택자) 사용

# In[18]:


import requests
from bs4 import BeautifulSoup # bs4 module 안에 BeautifulSoup class
from urllib.parse import urljoin # built in module


# In[2]:


url = 'https://news.naver.com/'
response = requests.get(url)
response.status_code # http 상태코드 2XX는 모두 성공
print('status code : ', response.status_code)
print('response header : ', response.headers)
response.headers['content-type']


# * http protocol
# * http method
# * **GET** url에 append해서 보내는 방식, 조회
# * **POST** body stream에 data를 담아서 보내는 방식, 등록, 갱신

# In[3]:


response.text # 페이지 소스 보기


# * network - news.naver.com - headers - response headers : 웹 페이지 상에서 보여지는 정보들
# * cookie: 사용자 정보를 client쪽에 저장되어 있다.
# * session: 사용자 정보를 서버쪽에 저장되어 있다.
# * - http protocol은 connectionless(웹 사용자가 많아서 다른사람들이 사용할 수 있도록 connection을 끊어서 서버의 용량을 확보)

# In[4]:


# 응답 데이터 텍스트
html = response.text


# In[26]:


# BeautifulSoup 객체 생성
soup = BeautifulSoup(html, 'html.parser')
tag_list = soup.select("a[href*=read.nhn]")
print(type(tag_list), len(tag_list))
for idx, a_tag in enumerate(tag_list):
#     print(a_tag)
    title = a_tag.text.strip() # a_tag type: bs4.element.Tag
    link = urljoin(url, a_tag['href'])
    print(idx, title,link)
    print('----------------------------')


# ### 2. Nhn 번역서비스 Papago 사용하기
# * urllib를 사용하기
# * requests 를 사용하기
# ###### urllib 사용

# In[28]:


# 네이버 Papago NMT API 예제
import os
import sys
import urllib.request

client_id = "Zo1vTslyKxKYskf_qfUk"
client_secret = "X5kGpbWEbv"

encText = urllib.parse.quote("Yesterday all my troubles seemed so far away.")
# query string: source=en&target=ko&text=
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"

request = urllib.request.Request(url) # request 객체 생성
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode() # status code처럼
if(rescode==200): # 정상
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)


# ###### requests 예제로 변환하기

# In[51]:


import requests

client_id = "Zo1vTslyKxKYskf_qfUk"
client_secret = "X5kGpbWEbv"

url = "https://openapi.naver.com/v1/papago/n2mt"
encText = "Yesterday all my troubles seemed so far away."

req_headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}
params = {
    "source":"en",
    'target':'ko',
    'text':encText
}
response = requests.post(url, headers=req_headers, data=params)
print('응답헤더값들: ',response.headers)
print('요청헤더값들', response.request.headers)
print('status code ', response.status_code)

if response.status_code == 200:
    print(response.text)
else:
    print('Error Code ', response.status_code)


# In[52]:


myjson = response.json()
print(type(myjson), myjson)


# In[53]:


myjson['message']['result']['translatedText']


# ### requests의 request, session 객체를 사용하는 방식으로 변환
# * request라는 객체를 만들어서 추출하기
# * post니까 body에서 header 

# In[57]:


import requests
# Request와 Session 클래스를 import
from requests import Request, Session

client_id = "majtsrBC2FKggVSIxjCp"
client_secret = "w0N76kN3PV"

url = "https://openapi.naver.com/v1/papago/n2mt"
encText = "Yesterday all my troubles seemed so far away."

req_headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}
params = {
    "source":"en",
    'target':'ko',
    'text':encText
}
# Session 객체 생성
session = Session()
# Request 객체 생성
req = Request('POST', url, headers=req_headers, data=params)
# request의 prepare() 함수 호출
prepped = req.prepare() # file읽는 시간이 있어서 준비시간을 가질수있도록 prepare() 함수 호출
#session의 send() 함수를 호출해서 서버에 요청을 전달
response = session.send(prepped)

print('응답헤더값들: ',response.headers)
print('요청헤더값들', response.request.headers)
print('status code ', response.status_code)

if response.status_code == 200:
    print(response.json()['message']['result']['translatedText'])
else:
    print('Error Code ', response.status_code)


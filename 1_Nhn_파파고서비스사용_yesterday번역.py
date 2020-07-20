#!/usr/bin/env python
# coding: utf-8

# #### data/yesterday.txt 번역
# 1. yesterday.txt 파일 읽기
# 2. requests로 http 통신
# 3. 번역된 결과를 파일에 쓰기

# In[13]:


from requests import Request, Session

# yesterday.txt 파일 읽기
def get_text_list():
    result_list = []
    with open('data/yesterday.txt','r',encoding='utf8') as file:
        contents = file.read()
        result_list = contents.split('\n')
    return result_list

# 번역된 결과를 파일에 쓰기
def save_to_file(lst):
    with open('data/yesterday_trans.txt', 'w', encoding='utf8') as file:
        file.writelines(lst)

# requests 로 http 통신
def main():
    # session 객체 생성
    session = Session()
    
    client_id = "majtsrBC2FKggVSIxjCp"
    client_secret = "w0N76kN3PV"
    url = "https://openapi.naver.com/v1/papago/n2mt"
    encText = "Yesterday all my troubles seemed so far away."

    req_headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    lyric_list = get_text_list()
    # list comprehension
    lyric_list = [lyric for lyric in lyric_list[::] if lyric]
    # print(lyric_list, len(lyric_list))
    
    trans_list = []
    for en_text in lyric_list:
        params = {
            "source":"en",
            'target':'ko',
            'text':en_text
        }
        req = Request('POST', url, data=params, headers=req_headers)
        prepared = req.prepare()
        res = session.send(prepared)
        
        try:
            ko_text = res.json()['message']['result']['translatedText']
        except Exception as err:
            print(err)
        else:
            trans_list.append(en_text+'\n'+ko_text+'\n')
            
    save_to_file(trans_list)
    print('번역 종료')

main()


# In[ ]:





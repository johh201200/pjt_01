import csv
import requests
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

people_list = []
result = {}

# 1.
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        people_list.append(row['peopleNm'])


# 2.
for peopleNm in people_list:
    key = config('API_KEY')

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?peopleNm={peopleNm}&key={key}&itemPerPage=100'
    response = requests.get(url).json()
    
    peoples = response.get('peopleListResult').get('peopleList')

    for people in peoples:
        code = people.get('repRoleNm')
        if code == '감독':  # ..
            result[people] = {
                'peopleCd': peoples.get('peopleCd'),
                'peopleNm': peoples.get('peopleNm'),
                'repRoleNm': peoples.get('repRoleNm'),
                'filmoNames': peoples.get('filmoNames')
            }
pprint(result)

# 영화인 코드(peopleCd), 영화인명(peopleNm), 분야(repRoleNm), 필모리스트(filmoNames)


# 3. 결과 저장하기
with open('director'.csv', 'w', encoding='utf-8', newline='') as f:
	# 2-1. 저장할 데이터들의 필드 이름을 미리 지정한다.
    fieldnames = ['peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames'] # 필드 -> 리스트, 튜플 모두 가능
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    # 2-2. 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
	# 2-3. 반복을 돌며 value 값들을 해당 필드의 row에 작성한다.
    for value in result.values():
        print(value)
        writer.writerow(value)


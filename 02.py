import csv
import requests
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint

movie_list = []
result = {}

# 1.
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 한줄씩 읽는다.
    for row in reader:
        movie_list.append(row['movieCd'])


# 2.
for movieCd in movie_list:
    key = config('API_KEY')
    
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'
    api_data = requests.get(url).json()
    
    movies = api_data.get('movieInfoResult').get('movieInfo')

    # for movie in movies:
    #     code = movie.get('movieCd')
    # if code not in result:
    result[movieCd] = {
        'movieCd': movies.get('movieCd'),
        'movieNm': movies.get('movieNm'),
        'movieNmEn': movies.get('movieNmEn'),
        'movieNmOg': movies.get('movieNmOg'),
        'watchGradeNm': movies.get('audits')[0].get('watchGradeNm') if movies.get('audits') else None,
        'openDt': movies.get('openDt'),
        'showTm': movies.get('showTm'),
        'genreNm': movies.get('genres')[0].get('genreNm') if movies.get('genres') else None,
        'peopleNm': movies.get('directors')[0].get('peopleNm') if movies.get('directors') else None
    }
pprint(result)

# 영화 대표코드(movieCd), 영화명_국문(movieNm)
# 영화명_영문(movieNmEn), 영화명_원문(movieNmOg), 관람등급(watchGradeNm), 개봉연도(openDt), 상영시간(showTm), 장르(genreNm), 감독명(peopleNm)


# 3. 결과 저장하기
with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
	# 2-1. 저장할 데이터들의 필드 이름을 미리 지정한다.
    fieldnames = ['movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm'] # 필드 -> 리스트, 튜플 모두 가능
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    # 2-2. 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()
	# 2-3. 반복을 돌며 value 값들을 해당 필드의 row에 작성한다.
    for value in result.values():
        print(value)
        writer.writerow(value)


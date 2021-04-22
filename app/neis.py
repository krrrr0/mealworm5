import requests


class NEIS:
    def __init__(self, g_config):
        self.key = g_config['NEIS']['NEIS_OPENAPI_KEY']
        return

    def search_school(self, query):
        """
        Neis OpenAPI 를 사용해 학교를 검색하고, NEIS.School 객체의 배열을 반환합니다.
        :param query: 학교 문자열
        :return: 검색된 학교 School Object 배열 (없으면 [] 리턴)
        """

        url = 'https://open.neis.go.kr/hub/schoolInfo'

        querystring = {
            'KEY': self.key,
            'Type': 'json',
            'pIndex': '1',
            'pSize': '5',
            'SCHUL_NM': str(query)
        }

        response = requests.request('GET', url, data='', headers={}, params=querystring)
        data = response.json()

        if data.get('RESULT', {}).get('CODE') == 'INFO-200':
            return []

        else:
            result = []
            for school in data['schoolInfo'][1]['row']:
                sch = self.School(
                    school['SCHUL_NM'],
                    '{0}+{1}'.format(school['ATPT_OFCDC_SC_CODE'], school['SD_SCHUL_CODE']),
                    school['ATPT_OFCDC_SC_CODE'],
                    school['LCTN_SC_NM'],
                    school['ORG_RDNMA'],
                    self.key
                )
                result.append(sch)

        return result

    def school_from_code(self, code):
        """
        학교 코드를 받아 해당 학교의 NEIS.School 객체를 반환합니다.
        :param code: 나이스 학교코드:str
        :return: NEIS.School
        """
        url = 'https://open.neis.go.kr/hub/schoolInfo'

        querystring = {
            'KEY': self.key,
            'Type': 'json',
            'pIndex': '1',
            'pSize': '5',
            'ATPT_OFCDC_SC_CODE': code.split('+')[0],
            'SD_SCHUL_CODE': code.split('+')[1]
        }

        response = requests.request('GET', url, data='', headers={}, params=querystring)
        data = response.json()

        if data.get('RESULT', {}).get('CODE') == 'INFO-200':
            raise ValueError('재조회: 학교가 없습니다')

        elif data['schoolInfo'][0]['head'][0]['list_total_count'] != 1:
            raise ValueError('재조회: 카운트가 1이 아닙니다')

        else:
            sch = self.School(
                data['schoolInfo'][1]['row'][0]['SCHUL_NM'],
                data['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE'] +
                '+' + data['schoolInfo'][1]['row'][0]['SD_SCHUL_CODE'],
                data['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE'],
                data['schoolInfo'][1]['row'][0]['LCTN_SC_NM'],
                data['schoolInfo'][1]['row'][0]['ORG_RDNMA'],
                self.key
            )
            return sch

    class School:
        def __init__(self, name, code, region_code, region_hangul, address, key):
            self.name = name
            self.code = code
            self.region_code = region_code
            self.region_hangul = region_hangul
            self.address = address

            self.key = key
            return

        def get_meal(self, date, time):
            """
            급식을 가져온다.
            :param date: datetime.date 객체. 급식을 가져올 날짜
            :param time: int. 1: 조식, 2: 중식, 3: 석식
            :return: menus(array), nutrition(str) / None
            """
            url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'

            querystring = {
                'KEY': self.key,
                'Type': 'json',
                'pIndex': '1',
                'pSize': '5',
                'ATPT_OFCDC_SC_CODE': self.code.split('+')[0],
                'SD_SCHUL_CODE': self.code.split('+')[1],
                'MLSV_YMD': date.strftime('%Y%m%d'),
                'MMEAL_SC_CODE': str(time)
            }

            payload = ''
            headers = {}

            response = requests.request('GET', url, data=payload, headers=headers, params=querystring)
            data = response.json()

            if data.get('RESULT', {}).get('CODE') == 'INFO-200':
                return None

            else:
                menus = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].replace('.', ',').split('<br/>')
                nutrition = data['mealServiceDietInfo'][1]['row'][0]['CAL_INFO'] + '\n' + \
                    data['mealServiceDietInfo'][1]['row'][0]['NTR_INFO'].replace('<br/>', '\n')
                return menus, nutrition

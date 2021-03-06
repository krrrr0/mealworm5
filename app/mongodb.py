import datetime
import pytz

from app.user import User

from pymongo import MongoClient


class MongoController:
    @staticmethod
    def get_user(uid, g_config):
        """
        Search user from DB, return the user object.
        :param g_config: 글로벌 콘피그 파일
        :param uid: User ID (Recipient ID)
        :return: User Object (없으면 None)
        """
        client = MongoClient()
        db = client['mealworm5']
        users = db.users

        usr = users.find_one({"uid": uid})
        if usr:
            return User({
                'uid': uid,
                'new_user': False,
                'user_details': {
                    'name': usr['name'],
                    'use_count': usr['use_count'],
                    'since': datetime.datetime.strptime(usr['since'], '%Y-%m-%d-%H-%M-%S')
                },
                'last_school_code': usr['last_school_code']
            }, g_config)

        else:
            return None

    @staticmethod
    def save_user(user):
        client = MongoClient()
        db = client['mealworm5']
        users = db.users
        usr = users.find_one({"uid": user.uid})

        if not usr:
            users.insert_one({
                'uid': user.uid,
                'name': user.name,
                'use_count': user.use_count,
                'since': user.since.strftime('%Y-%m-%d-%H-%M-%S'),
                'last_school_code': user.last_school_code
            })
        else:
            users.replace_one({
                'uid': user.uid
            }, {
                'uid': user.uid,
                'name': user.name,
                'use_count': user.use_count,
                'since': user.since.strftime('%Y-%m-%d-%H-%M-%S'),
                'last_school_code': user.last_school_code
            })

        return True

    @staticmethod
    def save_meal(user, meal):
        from app.log import Logger
        try:
            meal['created_date'] = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-%M-%S')

            client = MongoClient()
            db = client['mealworm5']
            meals = db.meals

            m = meals.find_one({"meal_id": meal['meal_id']})

            if not m:
                meals.insert_one(meal)
                Logger.log('[DB > save_meal] 급식 저장 완료!', 'INFO')
            else:
                Logger.log('[DB > save_meal] 급식 저장 건너뜁니다... (동시 실행)!', 'WARN')

            return True

        except Exception as e:
            from app.log import Logger
            Logger.log('[DB > save_meal] 급식 저장 실패. UID: {0}'.format(user.uid), 'ERROR', str(e))
            return None

    @staticmethod
    def search_meal(school_code, date, mealtime):
        try:
            client = MongoClient()
            db = client['mealworm5']
            meals = db.meals
            meal = meals.find_one({
                '$and': [
                    {'school_code': school_code},
                    {'date': date},
                    {'mealtime': int(mealtime)}
                ]
            })

            if meal:
                return meal
            else:
                from app.log import Logger
                Logger.log('[DB > search_meal] 급식이 DB에 없습니다.', 'INFO')
                return None
        except Exception as e:
            from app.log import Logger
            Logger.log('[DB > search_meal] DB에서 급식을 검색하 중 오류가 발생했어요..', 'INFO', str(e))
            return None

    @staticmethod
    def get_meal(meal_id):
        try:
            client = MongoClient()
            db = client['mealworm5']
            meals = db.meals
            meal = meals.find_one({"meal_id": meal_id})
            if meal:
                return meal
            else:
                from app.log import Logger
                Logger.log('[DB > get_meal] {0}번 급식이 DB에 없어요.'.format(meal_id), 'INFO')
        except Exception as e:
            from app.log import Logger
            Logger.log('[DB > get_meal] {0}번 급식 DB 조회중 오류 발생!'.format(meal_id), 'ERROR', str(e))
            return None

    @staticmethod
    def save_bugreport(uid, title, details, contact):
        try:
            client = MongoClient()
            db = client['mealworm5']
            bugs = db.bugs
            bugs.insert_one({
                'report_id': '{0}_{1}'.format(
                        uid,
                        datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-%M-%S')
                    ),
                'details': {
                    'uid': uid,
                    'title': title,
                    'details': details,
                    'contact': contact
                }
            })

        except Exception as e:
            from app.log import Logger
            Logger.log('[DB > save_bugreport] 버그 리포트 저장 실패.', 'ERROR', str(e))
            return None

        return True

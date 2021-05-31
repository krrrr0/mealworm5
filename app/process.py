from app.facebook import MessageElements as Elements
from app.template import Templates

import datetime
import pytz

from app.mongodb import MongoController
db = MongoController()


class Processing:
    def __init__(self):
        return

    def process_message(self, user, req_str, g_config):
        # 1. 오브젝트 만들기
        from app.facebook import FacebookMessenger
        fm = FacebookMessenger(g_config)
        fm.typing(user.uid)

        from app.log import Logger
        Logger.log('[PS > process_message] 요청: {0}->\'{1}\''.format(user.uid, req_str))

        # 이스터 에그
        if req_str.strip() == '올때 메로나':
            fm.send(
                user.uid,
                '응 아니야',
                Templates.QuickReplies.after_action
            )
            return user

        if '섹스' in req_str:
            fm.send(
                user.uid,
                '잠시 일상을 내려놓고 자신을 돌아보는 시간을 가지는 것은 어떨까요?',
                Templates.QuickReplies.after_user_error
            )
            return user

        # 2. DIALOGFLOW 리퀘스트
        try:
            from app.dialogflow import DialogFlowController
            df = DialogFlowController(g_config)
            df_result = df.get_results(req_str, user.uid, user.uid + str(user.use_count))
            intent = df_result['intent']

        except Exception as e:
            from app.log import Logger
            Logger.log('[PS > process_message] DF 오류!', 'ERROR', 'DETAILS: {0}'.format(e))
            fm.send(
                user.uid,
                '죄송합니다, 급식봇에 오류가 발생했습니다.\n'
                '자세한 정보: 알 수 없는 이유로 언어 분석에 실패했습니다.\n'
                '다시 시도해 주시고 오류가 지속되면 아래의 \'버그 신고하기\'를 이용해 주세요.',
                Templates.QuickReplies.after_system_error
            )
            return user

        # 3. Intent 분기
        if intent == 'Action.SourceCode':
            fm.send(user.uid, '급식봇5의 소스는 여기서 보실 수 있어요!')
            card = Elements.Card(Templates.Cards.view_source)
            fm.send(user.uid, card, Templates.QuickReplies.after_action)

        elif intent == 'Communication.Swear':
            fm.send(user.uid, ':(', Templates.QuickReplies.after_user_error)

        elif intent == 'Communication.Yes':
            fm.send(user.uid, ':)', Templates.QuickReplies.default)

        elif intent == 'Communication.Calling':
            fm.send(user.uid, '네, 여기 있어요.', Templates.QuickReplies.default)

        elif intent == 'Communication.ThankYou':
            fm.send(user.uid, '고마워요!', Templates.QuickReplies.default)

        elif intent == 'Action.Report':
            return self.process_postback(user, 'BUGREPORT', g_config)

        elif intent == 'Action.Help':
            return self.process_postback(user, 'HELP', g_config)

        elif intent == 'Communication.Hi':
            fm.send(user.uid, '안녕하세요, {0}님!'.format(user.name), Templates.QuickReplies.default)

        elif intent == 'Communication.Bye':
            fm.send(user.uid, '👋', Templates.QuickReplies.default)

        elif intent == 'Action.GetMeal':    # 급식
            # i. 엔티티 추출 및 가공
            entities = df_result['entities']

            # 날짜 엔티티가 비어있는 경우 오늘 날짜로 만들어버리기
            if entities['date-time'] == '':
                d = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
                entities['date-time'] = d.strftime('%Y-%m-%d') + 'T12:00:00+09:00'

            # mealtime 변환
            if entities['MealTime'] == '조식':
                mealtime = 1
            elif entities['MealTime'] == '석식':
                mealtime = 3
            else:
                mealtime = 2

            # ii. 학교명 유무에 따라 분기
            if (entities['SchoolName'] != '') or (user.last_school_code != ''):  # 학교명이 어디든 일단 있는경우
                if entities['SchoolName'] != '':  # 학교명을 직접 지정한 경우
                    try:
                        from app.neis import NEIS
                        neis = NEIS(g_config)
                        school_name = entities['SchoolName'].strip()

                        # 하드코딩된 화이트리스트에 있으면 대체
                        school_name_whitelist = {
                            '한대부중': '한양대학교사범대학부속중학교',
                            '한대부고': '한양대학교사범대학부속고등학교',
                            '서울과고': '서울과학고',
                            '경기과고': '경기과학고',
                            '세종과고': '세종과학고',
                            '한성과고': '한성과학고'
                        }
                        if school_name in school_name_whitelist:
                            school_name = school_name_whitelist[school_name]

                        school_list = neis.search_school(school_name)
                    except Exception as e:
                        fm.send(
                            user.uid,
                            '학교 조회 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.\n'
                            '문제가 계속될 경우, 아래 \'버그 신고하기\'로 신고해 주세요.',
                            Templates.QuickReplies.after_system_error
                        )

                        Logger.log(
                            '[PS > process_message] 나이스 학교 조회중 오류!',
                            'ERROR',
                            'RECIPIENT: {0}, DETAILS: {1}, VALUE: {2}'.format(user.uid, str(e), entities['SchoolName'])
                        )

                        return user

                    if len(school_list) == 0:  # 일치하는 학교가 없는 경우
                        fm.send(
                            user.uid,
                            '학교 \'{0}\'를 찾을 수 없어요.'.format(entities['SchoolName']),
                            Templates.QuickReplies.after_user_error
                        )

                        return user

                    elif len(school_list) > 1:  # 나이스에서 2개 이상의 학교를 찾음
                        # 안내 메시지 보내기
                        fm.send(user.uid, '여러 학교가 검색되었어요. 원하는 학교의 버튼을 선택해 주세요.')
                        fm.typing(user.uid)

                        [_, month, day] = entities['date-time'].split('T')[0].split('-')

                        # 카드 만들어서 붙이기
                        school_cards = []
                        for sch in school_list:
                            school_cards.append({
                                'title': sch.name + ' (%s)' % sch.region_hangul,
                                'image_url': '',
                                'subtitle': sch.address,
                                'buttons': [
                                    {
                                        'type': 'postback',
                                        'title': '{0}월 {1}일 {2} ({3}) 의 급식 보기'.format(
                                            month, day, sch.name, sch.region_hangul
                                        ),
                                        'payload': 'M_{0}_{1}_{2}'.format(
                                            sch.code,
                                            entities['date-time'].split('T')[0],
                                            str(mealtime)
                                        )
                                    }
                                ]
                            })

                        # 유저한테 보내기
                        card = Elements.Card(school_cards)
                        fm.send(user.uid, card)
                        return user

                    else:  # 힉교가 정상적으로 하나만 나옴
                        sch = school_list[0]
                        self.process_postback(
                            user,
                            'M_{0}_{1}_{2}'.format(
                                sch.code,
                                entities['date-time'].split('T')[0],
                                str(mealtime)
                            ),
                            g_config
                        )
                else:  # 학교명을 생략한 경우 -> 디비에 저장된 마지막 요청 학교를 가져온다.
                    self.process_postback(
                        user,
                        'M_{0}_{1}_{2}'.format(
                            user.last_school_code,
                            entities['date-time'].split('T')[0],
                            str(mealtime)
                        ),
                        g_config
                    )

            else:  # 학교 이름을 지정하지도 않았고 전에 사용한 기록도 없음.
                # 에러 / Abort
                fm.send(
                    user.uid,
                    '이전에 요청한 학교가 없습니다. 처음 요청 시에는 학교 이름을 포함해서 요청해 주세요.',
                    Templates.QuickReplies.after_user_error
                )
                return user

        else:  # Unknown Intent
            Logger.log('[PS > process_message] 알 수 없는 인텐트입니다: {0}. RECIPIENT: {1}'.format(intent, user.uid), 'WARN')
            fm.send(user.uid, '무슨 뜻인지 잘 모르겠어요.', Templates.QuickReplies.after_user_error)
            return user

        return user

    @staticmethod
    def process_postback(user, payload, g_config):
        # 1. 오브젝트 만들기
        from app.facebook import FacebookMessenger
        fm = FacebookMessenger(g_config)
        fm.typing(user.uid)

        from app.log import Logger
        Logger.log('[PS > process_postback] 요청: {0}->\'{1}\''.format(user.uid, payload))

        # 2. 페이로드 분기
        if payload == 'FACEBOOK_WELCOME':
            fm.send(user.uid, '안녕하세요, {0}님! 만나서 반가워요🤗'.format(user.name))
            fm.send(user.uid, '저는 급식봇이라고 해요.')
            fm.send(
                user.uid,
                '제 안에 있는 인공지능 덕분에 저는 다양한 말을 알아들을 수 있어요😎\n'
                '이제 제가 할 수 있는 일을 알아볼까요?',
                Templates.QuickReplies.intro
            )
            return user

        elif payload == 'INTRO_MORE':
            card = Elements.Card(Templates.Cards.intro_features)
            fm.send(user.uid, card)
            return user

        # 사용법
        elif payload == 'HELP':
            # 1/3 (Text)
            msg_str = '다양한 방법으로 급식을 가져올 수 있어요!\n' \
                      '예시:\n' \
                      '> 급식고등학교 내일 저녁\n' \
                      '> 3월 14일 급식고등학교 급식\n' \
                      '> 급식고등학교\n' \
                      '> 내일은?\n' \
                      '기본값은 오늘 날짜의 중식이에요.'
            fm.send(user.uid, msg_str)

            # 2/3 (Text)
            msg_str = '학교 이름을 생략한 경우, 바로 전에 요청하셨던 학교의 급식을 자동으로 가져올 거에요.\n' \
                      '예시:\n' \
                      '12:00 > 오늘 다솜중 급식이 뭐야?\n' \
                      '12:01 > 내일은?\n' \
                      '그렇기 때문에, 위의 경우에는 다솜중학교의 \'내일\' 급식을 가져옵니다.'
            fm.send(user.uid, msg_str)

            # 3/3 (Text)
            fm.send(user.uid, '혹시라도 잘 이해가 가지 않으시면 그냥 학교 이름을 입력해 보세요.')

            return user

        # 급식 급식 급식!
        elif payload.startswith('M_'):
            # user.use_count 를 올린다.
            user.use_count = user.use_count + 1

            # 파라미터 값을 추출한다.
            [_, school_code, tmp_date, mealtime] = payload.split('_')
            user.last_school_code = school_code
            date = datetime.datetime.strptime(tmp_date, '%Y-%m-%d')

            # 급식 가져오기
            from app.neis import NEIS
            neis = NEIS(g_config)

            try:
                sch = neis.school_from_code(school_code)
            except ValueError as e:
                fm.send(user.uid, '나이스 조회중 오류가 발생했습니다: 중복 조회되었습니다.', Templates.QuickReplies.after_system_error)
                Logger.log('[PS > process_postback] 나이스 재조회중 학교 중복 오류!', 'ERROR', str(e))
                return user
            except Exception as e:
                fm.send(user.uid, '나이스 조회중 오류가 발생했습니다: 알 수 없는 오류.', Templates.QuickReplies.after_system_error)
                Logger.log('[PS > process_postback] 나이스 재조회중 기타 오류!', 'ERROR', str(e))
                return user

            db_meal = db.search_meal(school_code, tmp_date, mealtime)
            if db_meal:  # 디비에서 저장된 급식을 가져왔을 때
                db_meal = db_meal['meal']
                meal_id = db_meal['meal_id']
                nutrition = db_meal['nutrition']
            else:   # 디비에 없을때
                meal_id = '#{0}{1}'.format(user.uid, user.use_count)
                try:
                    db_meal, nutrition = sch.get_meal(date, int(mealtime))
                except TypeError:
                    # 급식이 없음
                    db_meal = []
                    nutrition = None
                except Exception as e:
                    Logger.log('[PS > process_postback] 급식 조회 중 오류!', 'ERROR', str(e))
                    fm.send(user.uid, '급식 조회중 오류가 발생했습니다: 처리되지 않은 오류.', Templates.QuickReplies.after_system_error)
                    return user

            if int(mealtime) == 1:
                mt_text = '아침'
            elif int(mealtime) == 3:
                mt_text = '저녁'
            else:
                mt_text = '점심'

            # 잘 포장해서 보낸다
            if len(db_meal) != 0:  # 급식이 존재할 때
                meal_text = ''
                for menu in db_meal:
                    meal_text = meal_text + menu + '\n'
                meal_text = meal_text.rstrip()

                # 랜덤으로 보내기
                from random import randint
                rand_num = randint(0, 14)

                if rand_num == 0:
                    fm.send(
                        user.uid,
                        '급식봇을 {0}번째로 사용하고 계시네요!'.format(user.use_count)
                    )
                else:
                    msg_str = [
                        '',         # 0
                        '이 냄새는 바로!',
                        '반찬 남기지 마세요!',
                        '귀찮다고...',
                        '골고루 드세요',
                        '흐흐흐...',
                        '후후후...',
                        '어디서 주웠어요.',
                        '오다가 까먹을 뻔했어요',
                        '훗',
                        '오다가 주웠어요',
                        '냠냠',
                        '맛있게 드세요',
                        '졸려...',
                        '급식봇 페이지 좋아요를 부탁드립니다!\nhttps://fb.me/mealworm05'
                    ]
                    fm.send(user.uid, msg_str[rand_num])

                quick_replies = Templates.QuickReplies.after_meal
                quick_replies[0]['payload'] = 'N_{0}'.format(meal_id)

                # 급식을 보낸다
                fm.send(
                    user.uid,
                    '{0} {1}/{2}\n급식 #{3}:\n{4}'.format(tmp_date, sch.name, mt_text, meal_id[-6:], meal_text),
                    quick_replies
                )

                if not db_meal:
                    # FS에 급식을 세이브한다.
                    me = {
                        'meal_id': meal_id,
                        'meal': db_meal,
                        'school_code': school_code,
                        'school_name': sch.name,
                        'date': tmp_date,
                        'mealtime': int(mealtime),
                        'nutrition': nutrition
                    }
                    Logger.log(f'call save_meal!', 'INFO')
                    db.save_meal(user, me)

                return user

            else:  # 밥없음
                fm.send(
                    user.uid,
                    '%d년 %d월 %d일 %s의 %s 메뉴가 없어요.\n(또는 나이스에 등록이 안된 것일수도 있어요.)'
                    % (
                        int(date.year),
                        int(date.month),
                        int(date.day),
                        sch.name,
                        mt_text
                    ),
                    Templates.QuickReplies.after_nutrition
                )

            return user

        # 영양소 정보 보기
        elif payload.startswith('N_'):
            # 파라미터 값을 추출한다.
            _, meal_code = payload.split('_')

            # 급식 NO. 를 이용해서 급식을 가져온다.
            db_meal = db.get_meal(meal_code)
            if db_meal:  # 디비에서 저장된 급식을 가져왔을 때
                nutrition = db_meal['nutrition']   # str
                date = db_meal['date']
                school_name = db_meal['school_name']
                mealtime_hangul = ['아침', '점심', '저녁'][int(db_meal['mealtime']) - 1]

                fm.send(
                    user.uid,
                    '{0} {1}의 {2} 메뉴: 영양소 정보:\n{3}'.format(
                        date,
                        school_name,
                        mealtime_hangul,
                        nutrition
                    ),
                    Templates.QuickReplies.after_nutrition
                )

                return user
            else:  # 디비에 없을때
                fm.send(user.uid, '죄송해요, DB에서 급식의 영양소 정보를 찾을 수 없었어요.', Templates.QuickReplies.after_system_error)
                return user

        elif payload == 'BUGREPORT':
            fm.send(user.uid, '아래 버튼을 눌러서 신고해주세요.')

            tmp_c = Templates.Cards.bug_report
            tmp_c[0]['buttons'][0]['url'] += user.uid
            card = Elements.Card(tmp_c)
            fm.send(user.uid, card, Templates.QuickReplies.after_action)

            return user

        elif payload == 'ATTACHMENTS':
            fm.send(user.uid, ':)', Templates.QuickReplies.after_action)
            return user

        return user

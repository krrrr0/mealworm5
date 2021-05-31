"""
MEALWORM™ Server, version 5.

(c) 2021 dazzle inc.

For more information,
please refer to the link https://github.com/dazzleofficial/mealworm5/ .
"""

from flask import Flask, request, render_template
import traceback
import configparser
import requests
import json

from app.process import Processing
from app.mongodb import MongoController
from app.facebook import FacebookMessenger
from app.log import Logger
from app.user import User


# 초기화
g_config = configparser.ConfigParser()
g_config.read('config.ini')

app = Flask(__name__, static_url_path='/static')

ps = Processing()


@app.route('/')
def hello_world():
    # Make it Ra1n
    Logger.log('Hello, world!', 'NOTICE', 'This is a test.')
    return '<code>Notice Me!</code>'


@app.route('/old', methods=['GET', 'POST'])
def old_deprecated():
    if request.method == 'GET':
        # Verification Test
        if request.args.get('hub.verify_token') == g_config['FACEBOOK']['OLD_VERIFY_TOKEN']:
            return request.args.get('hub.challenge')
        else:
            return 'Verification Failed!'

    if request.method == 'POST':
        try:
            req = request.get_json()

            for event in req['entry']:
                for e in event['messaging']:    # 요청의 단위 시작
                    if e.get('postback', {}).get('payload') or e.get('message'):
                        headers = {
                            'content-type': 'application/json'
                        }

                        body = {
                            'recipient': {
                                'id': e['sender']['id']
                            },
                            'message': {
                                'text': '이 버전의 급식봇은 서비스가 종료되었습니다. 새로운 급식봇5를 이용해 주세요!\n'
                                        'https://facebook.com/mealworm05/\n'
                                        '시작하기 전에 페이지 좋아요&팔로우는 필수! 아시죠?😎'
                            }
                        }

                        response = requests.post(
                            'https://graph.facebook.com/v7.0/me/messages?access_token=' +
                            g_config['FACEBOOK']['OLD_ACCESS_TOKEN'],
                            data=json.dumps(body),
                            headers=headers
                        )

                        j = response.json()
                        if j.get('error'):
                            Logger.log('[APP > old] 그래프 API가 오류를 반환했습니다.', 'ERROR', response.text)

        except Exception as e:
            print('Fuck: {}'.format(str(e)))

        Logger.log('Deprecated Request Processed.')
        return 'Deprecated Request Processed.'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification Test
        if request.args.get('hub.verify_token') == g_config['FACEBOOK']['VERIFY_TOKEN']:
            return request.args.get('hub.challenge')
        else:
            return 'Verification Failed!'

    if request.method == 'POST':
        try:
            fs = MongoController()

            req = request.get_json()

            for event in req['entry']:
                # 요청의 단위
                for e in event['messaging']:
                    # 0. 고스트 확인
                    if e.get('message', {}).get('is_echo'):
                        continue

                    # 1. 디비에서 불러오기
                    usr = fs.get_user(e['sender']['id'], g_config)

                    # 0-1-1. 신규 유저인 경우
                    if not usr:
                        Logger.log('[APP > webhook] UID: {0} 생성합니다...'.format(e['sender']['id']))
                        user_config = {
                            'new_user': True,
                            'uid': e['sender']['id']
                        }
                        usr = User(user_config, g_config)

                    # 1-1. 포스트백 처리
                    if e.get('postback'):
                        if e['postback'].get('payload'):
                            usr = ps.process_postback(usr, e['postback']['payload'], g_config)
                            try:
                                fs.save_user(usr)
                                Logger.log(
                                    '유저 세이브 완료: {0}'.format(usr.uid),
                                    'NOTICE'
                                )
                            except Exception as e:
                                Logger.log(
                                    '[INIT] DB 유저 세이브 중 오류 발생: {0}'.format(str(e)),
                                    'ERROR',
                                    'RECIPIENT: {0}'.format(usr.uid)
                                )
                        continue

                    # 1-2. 메시지 처리
                    elif e.get('message'):
                        # 1-2-1. 빠른 답장 포스트백 처리
                        if e['message'].get('quick_reply'):
                            if e['message']['quick_reply'].get('payload'):
                                usr = ps.process_postback(usr, e['message']['quick_reply']['payload'], g_config)
                                try:
                                    fs.save_user(usr)
                                    Logger.log(
                                        '유저 세이브 완료: {0}'.format(usr.uid),
                                        'NOTICE'
                                    )
                                except Exception as e:
                                    Logger.log(
                                        'Mongo 유저 세이브 중 오류 발생: {0}'.format(str(e)),
                                        'ERROR',
                                        'RECIPIENT: {0}'.format(usr.uid)
                                    )
                                continue

                        # 1-2-2. 텍스트 메시지 처리
                        if e['message'].get('text'):
                            usr = ps.process_message(usr, e['message']['text'], g_config)
                            try:
                                fs.save_user(usr)
                                Logger.log(
                                    '유저 세이브 완료: {0}'.format(usr.uid),
                                    'NOTICE'
                                )

                                # 최적화: 전날 급식 캐시 제거

                            except Exception as e:
                                Logger.log(
                                    'Mongo 유저 세이브 중 오류 발생: {0}'.format(str(e)),
                                    'ERROR',
                                    'RECIPIENT: {0}'.format(usr.uid)
                                )
                            continue

                        # 1-2-3. 첨부파일 등이 있는 메시지
                        if e['message'].get('attachments'):
                            ps.process_postback(usr, 'ATTACHMENTS', g_config)

                    try:
                        fs.save_user(usr)
                        Logger.log(
                            '유저 세이브 완료: {0}'.format(usr.uid),
                            'NOTICE'
                        )
                    except Exception as e:
                        Logger.log(
                            'Mongo 유저 세이브 중 오류 발생: {0}'.format(str(e)),
                            'ERROR',
                            'RECIPIENT: {0}'.format(usr.uid)
                        )

            return {'result': 'fuck yeah!'}

        except Exception as e:
            traceback.print_exc()
            return {}

            try:
                Logger.log('치명적 오류 발생!! RECIPIENT: {0}'.format(e['sender']['id']), level='ERROR', details=str(e))

                fm = FacebookMessenger(g_config)
                fm.send(
                    e['sender']['id'],
                    '죄송합니다, 급식봇에 처리되지 않은 오류가 발생했습니다.\n'
                    '일시적인 오류인 경우, 다시 시도해 주세요. 계속적으로 오류가 발생하는 경우, '
                    '아래의 \'버그 신고하기\' 기능을 이용해 신고해 주세요.\n%s' % str(e)
                )

            except Exception:
                # 유언 못남김
                pass

            return {
                'result': 'screwed'
            }


@app.route('/support/bugreport', methods=['GET', 'POST'])
def bugreport():
    if request.method == 'GET':
        u_id = request.args.get('id')
        if u_id:
            return render_template('bugreport.html', id=u_id)
        else:
            return render_template('bad.html', details='잘못된 접근이에요.')

    else:
        try:
            uid = request.form['id']
            title = request.form['title']
            details = request.form['steps_to_reproduce']

            contact = request.form.get('want_contact')
            if contact:
                contact = request.form['contact_information']

            if uid != request.args.get('id'):
                raise ValueError

            logger = Logger()
            logger.bugreport(uid, title, details, contact)

            return render_template('success.html')

        except (KeyError, ValueError):
            return render_template('bad.html', details='잘못된 접근이에요.')

        except Exception as e:
            return render_template('bad.html', details='처리되지 않은 오류입니다: ' + str(e))

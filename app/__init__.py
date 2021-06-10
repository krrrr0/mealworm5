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
from app.log import Logger
from app.user import User


# 초기화
g_config = configparser.ConfigParser()
g_config.read('config.ini')

app = Flask(__name__, static_url_path='/static')

ps = Processing()
db = MongoController()


@app.route('/')
def hello_world():
    # Make it Ra1n
    Logger.log('Hello, world!', 'INFO', 'This is a test.')
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
                            headers=headers,
                            timeout=1.5
                        )

                        j = response.json()
                        if j.get('error'):
                            Logger.log('[OLD] 그래프 API가 오류를 반환했습니다.', 'ERROR', response.text)

                        break

        except Exception as e:
            print('Fuck: {}'.format(str(e)))

        Logger.log('[OLD] Deprecated Request Processed.')
        return {
            'result': 'success',
            'details': 'Successfully processed deprecated /old request.'
        }


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Verification Test
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == g_config['FACEBOOK']['VERIFY_TOKEN']:
            return request.args.get('hub.challenge')
        else:
            return 'Verification Failed!'

    # Messenger Callback
    if request.method == 'POST':
        try:
            req = request.get_json()
            for event in req['entry']:
                for e in event['messaging']:
                    # 메시지 시작
                    # 에코 메시지라면 스킵
                    if e.get('message', {}).get('is_echo'):
                        continue

                    # 1. 디비에서 사용자 정보 가져오기
                    try:
                        usr = db.get_user(e['sender']['id'], g_config)
                    except Exception as err:
                        Logger.log(f'[APP] db.get_user 오류', 'ERROR', str(err))

                        from app.facebook import FacebookMessenger
                        from app.template import Templates
                        fm = FacebookMessenger(g_config)
                        fm.send(e['sender']['id'], '데이터베이스 오류가 발생했습니다. 잠시 후 다시 이용해주세요.',
                                Templates.QuickReplies.after_system_error)
                        continue

                    # 1.1. 신규 유저
                    if not usr:
                        usr = User({'new_user': True, 'uid': e['sender']['id']}, g_config)
                        Logger.log(f'[APP] 신규 유저: {usr.uid}', 'INFO')

                    # 2. 포스트백 처리
                    if e.get('postback', {}).get('payload'):
                        usr = ps.process_postback(usr, e['postback']['payload'], g_config)
                        try:
                            db.save_user(usr)
                            Logger.log(f'[APP] 포스트백 처리후 유저 {usr.uid} 세이브 완료.', 'INFO')
                        except Exception as err:
                            Logger.log(f'[APP] 포스트백 처리후 유저 {usr.uid} 세이브중 오류 발생!', 'ERROR', str(err))

                            from app.facebook import FacebookMessenger
                            from app.template import Templates
                            fm = FacebookMessenger(g_config)
                            fm.send(e['sender']['id'], '데이터베이스 오류가 발생했습니다. 잠시 후 다시 이용해주세요.',
                                    Templates.QuickReplies.after_system_error)
                        continue

                    # 3. 메시지 처리
                    elif e.get('message'):
                        # 3.1. 빠른 답장 포스트백 처리
                        if e['message'].get('quick_reply', {}).get('payload'):
                            usr = ps.process_postback(usr, e['message']['quick_reply']['payload'], g_config)
                            try:
                                db.save_user(usr)
                                Logger.log(f'[APP] 빠른 답장 처리후 유저 {usr.uid} 세이브 완료.', 'INFO')
                            except Exception as err:
                                Logger.log(f'[APP] 빠른 답장 처리후 유저 {usr.uid} 세이브중 오류 발생!', 'ERROR', str(err))

                                from app.facebook import FacebookMessenger
                                from app.template import Templates
                                fm = FacebookMessenger(g_config)
                                fm.send(e['sender']['id'], '데이터베이스 오류가 발생했습니다. 잠시 후 다시 이용해주세요.',
                                        Templates.QuickReplies.after_system_error)
                            continue

                        # 3.2. 텍스트 메시지 처리
                        if e['message'].get('text'):
                            usr = ps.process_message(usr, e['message']['text'], g_config)
                            try:
                                db.save_user(usr)
                                Logger.log(f'[APP] 메시지 처리후 유저 {usr.uid} 세이브 완료.', 'INFO')
                                # 최적화: 전날 급식 캐시 제거
                            except Exception as err:
                                Logger.log(f'[APP] 메시지 처리후 유저 {usr.uid} 세이브중 오류 발생!', 'ERROR', str(err))

                                from app.facebook import FacebookMessenger
                                from app.template import Templates
                                fm = FacebookMessenger(g_config)
                                fm.send(e['sender']['id'], '데이터베이스 오류가 발생했습니다. 잠시 후 다시 이용해주세요.',
                                        Templates.QuickReplies.after_system_error)
                            continue

                        # 1-2-3. 첨부파일 등이 있는 메시지
                        if e['message'].get('attachments'):
                            ps.process_postback(usr, 'ATTACHMENTS', g_config)
                            continue

                    try:
                        db.save_user(usr)
                        Logger.log(f'[APP] 처리 없이 유저 {usr.uid} 세이브 완료.', 'INFO')
                    except Exception as err:
                        Logger.log(f'[APP] 처리 없이 유저 {usr.uid} 세이브중 오류 발생!', 'ERROR', str(err))

                        from app.facebook import FacebookMessenger
                        from app.template import Templates
                        fm = FacebookMessenger(g_config)
                        fm.send(e['sender']['id'], '데이터베이스 오류가 발생했습니다. 잠시 후 다시 이용해주세요.',
                                Templates.QuickReplies.after_system_error)

            return {'result': 'success'}

        except Exception as err:
            traceback.print_exc()
            Logger.log(f'[APP] 알 수 없는 치명적 오류 발생!', 'ERROR', str(err))

            try:
                from app.facebook import FacebookMessenger
                from app.template import Templates
                fm = FacebookMessenger(g_config)
                fm.send(e['sender']['id'],
                        f'죄송합니다, 급식봇에 처리되지 않은 오류가 발생했습니다.\n'
                        f'다시 시도해 주시고, 계속 오류가 발생할 경우 아래 \'버그 신고하기\' '
                        f'기능을 통해서 신고해 주세요.{str(err)}',
                        Templates.QuickReplies.after_system_error)
            except:
                pass

            return {'result': 'error'}  # 오류시에도 200 리턴


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

        except Exception as err:
            return render_template('bad.html', details='처리되지 않은 오류입니다: ' + str(err))

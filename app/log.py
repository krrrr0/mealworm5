import logging
import datetime
import pytz


class Logger:
    def __init__(self):
        return

    @staticmethod
    def log(payload, level='NOTICE', details=''):
        # Three log levels: NOTICE, WARN, ERROR
        # TODO: Timestamp
        # TODO: Make It Async
        print('[{0}] [{1}] {2} {3}'.format(datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y%m%d-%H%M%S'),
                                           level, payload, details))
        try:
            if level == 'ERROR':
                logging.error(payload + details)
            elif level == 'WARN':
                logging.warning(payload + details)
            elif level == 'NOTICE':
                logging.info(payload + details)
        except Exception as e:
            logging.error('[Logger > log] 로깅 중 오류가 발생하였습니다: {0}'.format(e))

        # TODO: Implement Send Mail (GAE)

        return

    def bugreport(self, uid, title, details, contact):
        try:
            from app.firestore import FireStoreController
            fs = FireStoreController()
            fs.save_bugreport(uid, title, details, contact)
        except Exception as e:
            self.log('[Logger > bugreport] 오류!', 'ERROR', str(e))
        return

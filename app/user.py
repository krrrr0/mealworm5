import datetime
import pytz


class User:
    def __init__(self, user_config, g_config):
        # 유저 콘피그를 들여다본다
        self.uid = user_config['uid']
        if user_config['new_user'] is True:  # 신규 유저로 __init__.py 에서 생성됨
            from app.facebook import Graph
            gp = Graph(g_config)
            self.since = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
            self.use_count = 1
            self.name = gp.get_name(uid=self.uid)
            self.last_school_code = ''
        else:  # Firestore 에서 해동됨
            self.since = user_config['user_details']['since']
            self.use_count = user_config['user_details']['use_count']
            self.name = user_config['user_details']['name']
            self.last_school_code = user_config['last_school_code']
        return

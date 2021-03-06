import os.path
import base64
import json
import time


SAVE_FILE_TYPE = 'iss'
_C_OFS = 5


class Save:
    def __init__(self, player_name :str, high :int, last_play_time :int,
            topic :str, score :int, save_name :str=None):
        self.player_name = player_name
        self.high_score = high
        self.last_play_time = last_play_time
        self.topic = topic
        self.now_score = score

        self.save_name = save_name


class SaveManager:
    @classmethod
    def search_save(cls, save_path :str='save/') -> list:
        '''
        :param save_path : 存档寻找路径
        :return : 返回在 save_path 所找到的存档文件的列表
        '''
        absp = os.path.abspath(save_path)

        pl = os.listdir(save_path)
        sl = []

        for p in pl:
            ps = p.split('.')

            if len(ps) > 1 and ps[-1] == SAVE_FILE_TYPE:
                ep = os.path.join(absp, p)
                res = ep if cls.load_save(ep) else None
                sl.append(res)

        return sl

    @classmethod
    def load_save(cls, save_path :str):
        with open(save_path, 'rb') as f:
            try:
                sf = f.read().decode()
                sf = ''.join([chr(ord(c) - _C_OFS) for c in sf])
                sj = json.loads(sf)

                name, high, last, topic, score = [base64.b64decode(item).decode()
                    for item in (sj['player_name'], sj['high'], sj['last'],
                                    sj['topic'], sj['score'])]
                sn = os.path.split(save_path)[-1]

                # check topic
                if topic == 'None':
                    topic = None

                return Save(name, int(high), int(last), topic, int(score), sn)
            except (KeyError, ValueError, json.decoder.JSONDecodeError):
                return None

    @classmethod
    def write_save(cls, save :Save, save_path :str='save/'):
        try:
            absp = os.path.abspath(save_path)

            name, high, last, topic, score = [
                    base64.b64encode(str(item).encode()).decode()
                    for item in
                    (save.player_name, save.high_score, save.last_play_time,
                    save.topic, save.now_score)]

            jd = {
                    'player_name' : name,
                    'high' : high,
                    'last' : last,
                    'topic' : topic,
                    'score' : score
                 }

            ds = json.dumps(jd)

            ds = ''.join([chr(ord(c) + _C_OFS) for c in ds])

            if not save.save_name:
                sn = 'SAVE_%s.%s' % (len(cls.search_save(save_path)), SAVE_FILE_TYPE)
            else:
                sn = save.save_name

            with open(os.path.join(absp, sn), 'wb') as f:
                f.write(ds.encode())

            return True
        except Exception:
            raise
            return False

    @classmethod
    def save_preview(cls, save_path):
        s = cls.load_save(save_path)
        tstr = time.strftime('%Y / %m / %d | %H:%M:%S', time.localtime(
            s.last_play_time))
        sstr = '%s  [%s]' % (s.player_name, tstr)

        return sstr

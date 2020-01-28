import requests
from bs4 import BeautifulSoup
import random
from pypinyin import lazy_pinyin

class Referee:
    __URL_SEARCH = 'http://www.chengyujielong.com.cn/search/%s'

    def __init__(self):
        self.__topic = None

    def check_answer(self, ans :str, topic :str):
        if len(ans) == 4:
            return lazy_pinyin(ans)[0] == lazy_pinyin(topic)[-1] and self.__get_idiom_list(ans)
        return False

    def __get_idiom_list(self, keyword):
        r = requests.get(self.__URL_SEARCH % keyword)
        soup = BeautifulSoup(r.text, features="html.parser")
        d = soup.findAll('div', class_='panel panel-default')[0]
        sd = BeautifulSoup(str(d), features="html.parser")

        return [t.text for t in sd.findAll('a', rel='noopener')]

    def get_prompt(self, question) -> str:
        if not question:
            return 0

        sd = self.__get_idiom_list(question)

        res = [t for t in sd \
             if len(t) == 4 and lazy_pinyin(t)[0] == question]

        return random.choice(res) if res else None

    def set_topic(self, t :str):
        self.__topic = t

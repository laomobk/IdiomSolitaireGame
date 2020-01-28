import requests
from bs4 import BeautifulSoup
import random
from pypinyin import lazy_pinyin


class Player:
    '''
    interface
    '''
    def recv_question(self, question):
        pass

    def give_answer(self) -> str:
        return '<UNDEFINED>'


class ComputerPlayer(Player):
    __URL_SEARCH = 'http://www.chengyujielong.com.cn/search/%s'

    def __init__(self):
        self.__answer_list = []

    def __get_answer_data(self, idiom :str) -> list:
        r = requests.get(self.__URL_SEARCH % idiom)
        soup = BeautifulSoup(r.text, features="html.parser")
        d = soup.findAll('div', class_='panel panel-default')[0]
        sd = BeautifulSoup(str(d), features="html.parser")

        return [t.text for t in sd.findAll('a', rel='noopener')    \
                    if lazy_pinyin(t.text)[0] == idiom]

    def recv_question(self, question):
        self.__answer_list = self.__get_answer_data(question)

    def give_answer(self):
        return random.choice(self.__answer_list)  \
                if self.__answer_list else None

    def __str__(self):
        return '<ComputerPlayer>'


class HumanPlayer(Player):
    def __init__(self, name :str='Nezha'):
        self.__question = None
        self.__ps1 = '>> '
        self.name = name

    def recv_question(self, question):
        self.__question = question

    def give_answer(self, prompt :str=None):
        return input(self.__ps1 if not prompt else prompt)

    def __str__(self):
        return '<HumanPlayer %s>' % self.name

    __repr__ = __str__


if __name__ == '__main__':
    import pprint
    pprint.pprint(ComputerPlayer().recv_question('一个顶俩'))


from referee import Referee
from player import HumanPlayer, ComputerPlayer
from pypinyin import lazy_pinyin


class GameEngine:
    def __init__(self):
        self.welcome_text = \
            '''welcome to IdiomSolitaire
type 'WTF' to skip, type 'HELP' to get prompt, type 'QUIT' to exit.
'''
        self.help_ps = 'help'

        self.__referee = Referee()

        self.__players = [ComputerPlayer(), HumanPlayer()]

    def __who_is_next_turn(self, first :int) -> int:
        '''
        :return : an generator yield who is next turn  1 -> player | 0 -> computer
        '''

        t = first

        while True:
            if t == 0:
                t = 1
                yield 0
            else:
                t = 0
                yield 1

    def run_game(self, first_turn :int=1):
        turn_generator = self.__who_is_next_turn(first_turn)
        now_topic = None
        turn = next(turn_generator)

        jump_over = False

        print(self.welcome_text)

        while True:
            a = self.__players[turn]
            b = self.__players[abs(turn - 1)]

            print('It is your turn! %s' % ('topic is \'%s\' ' % lazy_pinyin(now_topic)[-1] if now_topic else ''))
            ans = a.give_answer()

            while not self.__referee.check_answer(ans, now_topic if now_topic else ans[::-1]):
                if ans in ('HELP', 'HELPME'):
                    p = self.__referee.get_prompt(lazy_pinyin(now_topic)[-1] if now_topic else None)
                    now_topic = None
                    if p:
                        print('prompt is %s' % p)
                        now_topic = p
                    elif p == 0:
                        print('No prompt. May be it is your turn.')
                    else:
                        print('no prompt, jump in next turn.')

                    jump_over = True

                    break

                elif ans == 'WTF':
                    print('Jump over.')
                    now_topic = None
                    jump_over = True

                    break

                elif ans == 'QUIT':
                    print('Quit game.')
                    return

                ans = a.give_answer('\'%s\' is incorrect. Try another one \n>> ' % ans)

            if jump_over:
                jump_over = False
                continue

            pyin = lazy_pinyin(ans)

            b.recv_question(pyin[-1])
            now_topic = b.give_answer()

            if not now_topic:
                print('Opponent(%s) : %s' % (b, 'OK, I give in...'))
                return

            self.__referee.set_topic(now_topic)
            print('Opponent(%s) : %s' % (b, now_topic))

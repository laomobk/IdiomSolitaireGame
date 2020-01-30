
from referee import Referee
from player import HumanPlayer, ComputerPlayer
from pypinyin import lazy_pinyin
from save_manager import Save, SaveManager
import language_manager as lmgr

import os
import time

if os.name == 'posix':
    try:
        import readline   # unix readline support.
    except ImportError:
        pass


class GameEngine:
    def __init__(self):
        self.welcome_text = lmgr.GLOBAL_LANGUAGE.Global.welcome_text
        self.help_ps = 'help'
        self.__each_score = 10

        self.__referee = Referee()

        self.__players = [ComputerPlayer(), HumanPlayer()]

        self.__global_socre = 0
        self.__global_save = None

    @property
    def score(self) -> int:
        return self.__global_socre

    @property
    def save(self) -> Save:
        return self.__global_save

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

    def __update_save(self, now_topic :str, now_time :int, 
                        score :int, save :Save):
        save.topic = now_topic
        save.last_play_time = now_time
        save.now_score = score

        if save.high_score < score:
            save.high_score = score

    def __new_game(self):
        print(lmgr.GLOBAL_LANGUAGE.GamePlay.init_game)
        return input(lmgr.GLOBAL_LANGUAGE.GamePlay.ask_name)

    def run_game(self, save :Save=None, first_turn :int=1) -> int:
        '''
        :return: 这局游戏的得分
        '''
        turn_generator = self.__who_is_next_turn(first_turn)
        turn = next(turn_generator)
        
        now_save = save

        if not now_save:
            now_save = Save('<NO NAME>', 0, int(time.time()), None, 0)
            now_save.player_name = self.__new_game()

        now_topic = now_save.topic
        self.__global_socre = now_save.now_score

        self.__global_save = now_save

        jump_over = False

        print()
        print(self.welcome_text)

        while True:
            a = self.__players[turn]
            b = self.__players[abs(turn - 1)]

            print(lmgr.GLOBAL_LANGUAGE.GamePlay.show_score % (self.__global_socre, save.high_score))
            print(lmgr.GLOBAL_LANGUAGE.GamePlay.your_turn %
                  (lmgr.GLOBAL_LANGUAGE.GamePlay.topic_is % lazy_pinyin(now_topic)[-1] if now_topic else ''))
            ans = a.give_answer('%s >> ' % now_save.player_name)

            while not self.__referee.check_answer(ans, now_topic if now_topic else ans[::-1]):
                if ans in ('HELP', 'HELPME'):
                    p = self.__referee.get_prompt(lazy_pinyin(now_topic)[-1] if now_topic else None)
                    now_topic = None
                    if p:
                        print(lmgr.GLOBAL_LANGUAGE.GamePlay.prompt_is % p)
                        now_topic = p
                    elif p == 0:
                        print(lmgr.GLOBAL_LANGUAGE.GamePlay.no_prompt_turn)
                    else:
                        print(lmgr.GLOBAL_LANGUAGE.GamePlay.no_prompt_jump)

                    jump_over = True

                    break

                elif ans == 'WTF':
                    print(lmgr.GLOBAL_LANGUAGE.GamePlay.jump_over)
                    now_topic = None
                    jump_over = True

                    break

                elif ans == 'QUIT':
                    return now_save

                ans = a.give_answer(lmgr.GLOBAL_LANGUAGE.GamePlay.incorrect_ps % ans)

            if jump_over:
                self.__update_save(
                    now_topic, int(time.time()), self.__global_socre, now_save)
                jump_over = False
                continue

            if now_topic:
                self.__global_socre += self.__each_score
                self.__update_save(
                    now_topic, int(time.time()), self.__global_socre, now_save)
                
            pyin = lazy_pinyin(ans)

            b.recv_question(pyin[-1])
            now_topic = b.give_answer()

            if not now_topic:
                print(lmgr.GLOBAL_LANGUAGE.GamePlay.opponent_say %
                      (b, lmgr.GLOBAL_LANGUAGE.GamePlay.give_in))
                print(lmgr.GLOBAL_LANGUAGE.GamePlay.opponent_say)
                self.__global_socre += 100

                return now_save

            self.__referee.set_topic(now_topic)
            print(lmgr.GLOBAL_LANGUAGE.GamePlay.opponent_say % (b, now_topic))

            self.__update_save(
                        now_topic, int(time.time()), self.__global_socre, now_save)


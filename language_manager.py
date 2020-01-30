
import os.path
import json


class Language:
    language_name = 'No language package found'

    class Players:
        computer_player     = ''
        human_player        = ''

    class GamePlay:
        init_game           = ''
        ask_name            = ''
        show_score          = ''
        your_turn           = ''
        topic_is            = ''
        no_prompt_jump      = ''
        no_prompt_turn      = ''
        jump_over           = ''
        incorrect_ps        = ''
        prompt_is           = ''
        opponent_say        = ''
        give_in             = ''
        win_computer        = ''

    class SaveMenu:
        founded_count       = ''
        new_game            = ''
        exit_game           = ''
        ask_select          = ''
        finding_save        = ''

    class Global:
        auto_save           = ''
        save_succeed        = ''
        save_failed         = ''
        exit_game           = ''
        show_score          = ''
        welcome_text        = ''
        loading             = ''

    def __str__(self):
        return '<Language object \'%s\'>' % self.language_name

    __repr__ = __str__


class LanguageLoader:
    @classmethod
    def load_language_package(cls, lang_path :str) -> tuple:
        '''
        :param lang_path: 语言包位置
        :return: 返回 (SIGN, ERRMSG, LANGUAGE_OBJ)
        '''
        lang = Language()

        try:
            jd :dict = json.loads(open(lang_path, encoding='UTF-8').read())

            lang.language_name = jd['language']

            del jd['language']

            # check json file
            if jd['sign'] != 'IDIOM_SOLITAIRE_LANGUAGE_PACKAGE':
                raise ValueError()

            del jd['sign']

            for topic, content in jd.items():
                # 填充Language对象
                tc :Language = getattr(lang, topic)
                if not isinstance(tc, type):
                    raise ValueError()

                for k, v in content.items():
                    if hasattr(tc, k):
                        setattr(tc, k, v)
                    else:
                        raise ValueError(k, v)

            return (1, 'Successfully load language package', lang)

        except UnicodeDecodeError as e:
            return (0, '%s\nPlease check language file encode' % str(e), None)

        except (ValueError, AttributeError, KeyError):
            raise
            return (0, 'Language package incomplete', None)

        except FileNotFoundError:
            return (0, 'Language package Not exists', None)


    @classmethod
    def search_packages(cls, search_path :str='lang/'):
        sl = os.listdir(search_path)
        absp = os.path.abspath(search_path)

        fl = []

        for p in sl:
            ps = p.split('.')

            try:
                if len(ps) > 1 and ps[-1] == 'json':
                    jd = json.loads(open(os.path.join(absp, p), encoding='UTF-8').read())
                    if jd['sign'] != 'IDIOM_SOLITAIRE_LANGUAGE_PACKAGE':
                        raise ValueError()

                    fl.append(os.path.join(absp, p))
            except (KeyError, ValueError):
                raise

        return fl

    @classmethod
    def load_from_name(cls, name :str, search_path :str='lang/') -> Language:
        ll = cls.search_packages(search_path)

        for lp in ll:
            sign, msg, lang = cls.load_language_package(lp)
            if lang:
                if lang.language_name == name:
                    return lang

        return None

GLOBAL_LANGUAGE = LanguageLoader.load_from_name('简体中文')

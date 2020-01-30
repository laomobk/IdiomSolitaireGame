
import language_manager as lmgr

print(lmgr.GLOBAL_LANGUAGE.Global.loading, end='')

import engine
from save_manager import Save, SaveManager
import os.path


def ask_for_save() -> Save:
    print(lmgr.GLOBAL_LANGUAGE.SaveMenu.finding_save, end='')

    if not os.path.exists('save') or os.path.isfile('save'):
        os.mkdir('save')

    found = SaveManager.search_save()

    if found:
        print(lmgr.GLOBAL_LANGUAGE.SaveMenu.founded_count %
                (len(found) - found.count(None), found.count(None)))
        found = [x for x in found if x]
        for i, p in enumerate(found):
            print('[%d]  %s' % (i, SaveManager.save_preview(p)))
        # print new save
        print()
        print(lmgr.GLOBAL_LANGUAGE.SaveMenu.new_game % len(found))
        print(lmgr.GLOBAL_LANGUAGE.SaveMenu.exit_game % (len(found) + 1))
        print()

        while True:
            try:
                si = int(input(lmgr.GLOBAL_LANGUAGE.SaveMenu.ask_select))

                if si > len(found) + 1:
                    continue
                elif si == len(found):
                    return None
                elif si == len(found) + 1:
                    raise EOFError()
                break
            except ValueError:
                pass

        return SaveManager.load_save(found[si])
    
    return None


def main():
    eg = engine.GameEngine()

    try:
        # check language
        if not lmgr.GLOBAL_LANGUAGE:
            print('Warning : Failed to language package \r')

        save = ask_for_save()
        s = eg.run_game(save) 
    except (KeyboardInterrupt, EOFError):
        pass

    if eg.save:
        print(lmgr.GLOBAL_LANGUAGE.Global.auto_save)
        signal = SaveManager.write_save(eg.save)

        if signal:
            print(lmgr.GLOBAL_LANGUAGE.Global.save_succeed)
        else:
            print(lmgr.GLOBAL_LANGUAGE.Global.save_failed)

        print(lmgr.GLOBAL_LANGUAGE.Global.show_score % eg.save.now_score)
        print(lmgr.GLOBAL_LANGUAGE.Global.highest_score % eg.save.high_score)
    print(lmgr.GLOBAL_LANGUAGE.Global.exit_game)


if __name__ == '__main__':
    main()

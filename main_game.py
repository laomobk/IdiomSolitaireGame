print(' Loading...\r', end='')

import engine
from save_manager import Save, SaveManager

def ask_for_save() -> Save:
    found = SaveManager.search_save()

    if found:
        print('%d save found:' % len(found))
        for i, p in enumerate(found):
            print('[%d]  %s' % (i, SaveManager.save_preview(p)))
        # print new save
        print()
        print('[%d]  NEW GAME' % len(found))
        print('[%d]  EXIT' % (len(found) + 1))

        while True:
            try:
                si = int(input('Select a save (index) : '))

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
        save = ask_for_save()
        s = eg.run_game(save) 
    except (KeyboardInterrupt, EOFError):
        pass

    if eg.save:
        print('Auto saving...')
        signal = SaveManager.write_save(eg.save, '.')

        if signal:
            print('Success !')
        else:
            print('Failed !')

        print('\nScore =', eg.save.now_score)
    print('Exit game.')

if __name__ == '__main__':
    main()

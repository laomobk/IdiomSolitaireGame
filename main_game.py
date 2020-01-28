import engine

def main():
    eg = engine.GameEngine()

    try:
        s = eg.run_game()
    except (KeyboardInterrupt, EOFError):
        pass

    print('\nScore =', eg.score)
    print('Exit game.')

if __name__ == '__main__':
    main()

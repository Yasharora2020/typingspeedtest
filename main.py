import curses
import random
from curses import wrapper
import time


def setup_screen(stdscr):
    """ set up the screen """
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed typing test. Please any key to begin.", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    """" create a list of words from a text file """
    with open('text.txt', 'r') as r:
        lines = r.readlines()
        return random.choice(lines).strip()

def display_text(stdscr,text_to_type,typed_text,wpm=0):
    """ display the text to type and the typed text """
    stdscr.addstr(text_to_type)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    for i, char in enumerate(typed_text):
        correct_char= text_to_type[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def wordsperminute(stdscr):
    """ calculate the words per minute """
    text_to_type = load_text()
    typedtext = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(typedtext) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr,text_to_type,typedtext,wpm)
        stdscr.refresh()

        if "".join(typedtext) == text_to_type:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(typedtext) > 0:
                typedtext.pop()
        elif len(typedtext) < len(text_to_type):
            typedtext.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE,curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE,curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE,curses.COLOR_BLACK)

    setup_screen(stdscr)

    while True:
        wordsperminute(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")

        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)








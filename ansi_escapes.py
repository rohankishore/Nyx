ESC = '\u001B['
is_terminal_app = True


def cursor_to(x, y=None):
    return ESC + str(y + 1) + ';' + str(x + 1) + 'H'


def cursor_move(x, y=None):
    ret = ''

    if x < 0:
        ret += ESC + '-' + str(x) + 'D'
    elif x > 0:
        ret += ESC + str(x) + 'C'

    if y < 0:
        ret += ESC + '-' + str(y) + 'A'
    elif y > 0:
        ret += ESC + str(y) + 'B'

    return ret


def cursor_up(count=1):
    return ESC + str(count) + 'A'


def cursor_down(count=1):
    return ESC + str(count) + 'B'


def cursor_forward(count=1):
    return ESC + str(count) + 'C'


def cursor_backward(count=1):
    return ESC + str(count) + 'D'


cursor_left = ESC + 'G'
cursor_save_position = ESC + ('7' if is_terminal_app else 's')
cursor_restore_position = ESC + ('8' if is_terminal_app else 'u')
cursor_get_position = ESC + '6n'
cursor_next_line = ESC + 'E'
cursor_prev_line = ESC + 'F'
cursor_hide = ESC + '?25l'
cursor_show = ESC + '?25h'


def erase_lines(count=1):
    clear = ''

    for i in range(count):
        clear += erase_line + (cursor_up() if i < count - 1 else '')

    return clear + cursor_left


def set_color(color):
    r, g, b = color
    return f'\u001B[38;2;{r};{g};{b}m'


def set_low_color(color_str):
    color_str_map = {
        'red': 91,
        'green': 92,
        'blue': 36,
        'gray': 97,
        'anti_red': 96,
        'anti_green': 95,
        'anti_blue': 93
    }
    return f'\u001B[{color_str_map[color_str]}m'


erase_end_line = ESC + 'K'
erase_start_line = ESC + '1K'
erase_line = ESC + '2K'
erase_down = ESC + 'J'
erase_up = ESC + '1J'
erase_screen = ESC + '2J'
scroll_up = ESC + 'S'
scroll_down = ESC + 'T'

clear_screen = '\u001Bc'
beep = '\u0007'
import os
from platform import system as os_system
import json
from random import randint, shuffle
from time import sleep

old_bounds = os.get_terminal_size()
os_ev = os_system()

ai_data = ""
with open("dat_d.json", "r") as f:
    ai_data = json.load(f)
    f.close()

if os_ev == "Windows":
    os.system("mode con cols=9 lines=10")
else:
    print("\x1b[8;9;10t")

def train_ai(cur, mov_l: str):
    global ai_data
    for i in range(0, len(ai_data)):
        try:
            print(ai_data[i][cur])
            if len(ai_data[i][cur]) > 1:
                ai_data[i][cur].pop(ai_data[i][cur].index(mov_l))
                return
        except KeyError:
            print("NOne")

def eval_move(cur: str, mov: str, rep="1", side="white") -> str: 
    _do = False
    _from = 0
    _to = 0
    if side == 'white':
        try:
            if mov[0] == "$":
                _do, _from, _to = check_mov(cur, mov[1::])
                print(f"{_do};{_from};{_to}")
                exit()
            else:
                _do, _from, _to = check_mov(cur, mov)
        except TypeError:
            if mov[0] == "$":
                print("False")
                exit()
            return False
    else:
        try:
            _do, _from, _to = check_mov(cur, mov, perspective='black')
        except TypeError:
            return False
    
    if _do:
        change = []
        for i in range(0, len(cur)):
            change.append(cur[i])
        print(_from)
        change[_from] = '0'
        change[_to] = rep
        return "".join(change)
    return False

def get_ai_move(cur: str) -> str:
    global ai_data
    mov_set = []
    for i in range(0, len(ai_data)):
        try:
            mov_set = ai_data[i][cur]
        except KeyError:
            pass
    if mov_set == []:
        raise ValueError(f"I don't have a valid move set for the current board state: {cur}. Please restore to the default data set.")
    shuffle(mov_set)
    return mov_set[randint(0, len(mov_set)-1)]

def print_screen(cur: str):
    if os_ev == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    print("-------------\n|", end="")
    for i in range(0, len(cur)):
        if cur[i] == ' ':
            print("\n-------------\n|", end="")
        elif cur[i] == '2':
            print(" \u2659 |", end="")
        elif cur[i] == '1':
            print(" \u265F |", end="")
        else:
            print("   |", end="")
    print("\n-------------", end="")
    return

def check_mov(brd: str, mov: str, perspective="white") -> tuple:
    if perspective == 'white':
        rep = '1'
        nrep = '2'
    else:
        rep = '2'
        nrep = '1'
    _from = 0
    _to = 0
    if perspective == "white":
        e = {
            "1" : 0,
            "2" : 4,
            "3" : 8
        }
        e_c = {
            "a" : 0,
            "b" : 1,
            "c" : 2
        }
    else:
        e = {
            "1" : 8,
            "2" : 4,
            "3" : 0
        }
        e_c = {
            "a" : 0,
            "b" : 1,
            "c" : 2
        }
    """if mov[0] == '1' or mov[0] == '2' or mov[0] == 'x':
        offset = 0
        if mov[0] != 'x':
            offset = 1
        try:
            _to = e[mov[2+offset]]+e_c[mov[1+offset]]
            if _to > 10 or _to < 0:
                return False, _from, _to
            
            if perspective == 'white' and _to in [8, 10]:
                if brd[5] == '1':
                    return True, 5, _to
                return False, 0, 0

            _from = (e[mov[2+offset]]+e_c[mov[1+offset]])-3
            if perspective != 'white':
                _from = (e[mov[2+offset]]+e_c[mov[1+offset]])+3
                if mov[0] == '2':
                    _from += 2
                \"\"\"if offset == 1:
                    if mov[0] == '2':
                        _from += 2
                    else:
                        _from += 1
                        #_to += 3\"\"\"
                return True, _from, _to
            if (mov[0] == '2' or mov[0] == '1') and perspective == 'white':
                if mov[0] == '2':
                    _from -= 2
                if brd[_to] == '2' and brd[_from] == '1':
                    return True, _from, _to
                return False, _from, _to
            if _from == 3 or _from == 1:
                if brd[1] == '1' and brd[_to] == '2':
                    return True, 1, _to
                return False, _from, _to
            if brd[_from] == '1' and not _from > 10 and not _from < 0 and brd[_to] == '2':
                return True, _from, _to
            else:
                if _to in [1, 5, 9] and brd[_to] == '2':
                    _from = (e[mov[2+offset]]+e_c[mov[1+offset]])-5
                    if brd[_from] == '1' and not _from > 10 and not _from < 0:
                        return True, _from, _to
                return False, _from, _to
        except KeyError:
            return False, _from, _to
    elif mov[0] in ["a", "b", "c"]:
        try:
            _to = e[mov[1]]+e_c[mov[0]]
            if perspective == 'white':
                _from = _to-4
            else:
                _from = _to+4
                return True, _from, _to
            if brd[_from] == '1' and brd[_to] == '0':
                return True, _from, _to
        except KeyError:
            return False, _from, _to"""
    offset = 0
    if mov[0] == 'x':
        offset = 1
    if mov[0] != 'x' and mov[0] not in ["a", "b", "c"]:
        offset = 1
        if mov[1] == 'x':
            _to = e[mov[2+offset]]+e_c[mov[1+offset]]
            if mov[0] == '1':
                if perspective == 'white':
                    _from = _to-5
                else:
                    _from = _to+3
            else:
                if perspective == 'white':
                    _from = _to-3
                else:
                    _from = _to+5
            if (not _from < 0 and not _from > 10) and (not _to < 0 and not _to > 10):
                if brd[_from] == rep and brd[_to] == nrep:
                    return True, _from, _to
        return False, 0, 0
    _to = e[mov[1+offset]]+e_c[mov[0+offset]]
    if mov[0] in ["a", "b", "c"]:
        if perspective == 'white':
            _from = _to-4
        else:
            _from = _to+4
        if (not _from < 0 and not _from > 10) and (not _to < 0 and not _to > 10):
            if brd[_from] == rep and brd[_to] == '0':
                return True, _from, _to
        return False, 0, 0
    if mov[0] == 'x':
        if _to in [1, 5, 9]:
            if _to in [5, 9]:
                if perspective == 'white':
                    _from = _to - 5
                else:
                    _from = _to + 3
            else:
                if perspective == 'white':
                    _from = _to - 3
                else:
                    _from = _to + 5
            if (not _from < 0 and not _from > 10) and (not _to < 0 and not _to > 10):
                if brd[_from] == rep and brd[_to] == nrep:
                    return True, _from, _to
            if _to in [5, 9]:
                if perspective == 'white':
                    _from = _to - 3
                else:
                    _from = _to + 5
            else:
                if perspective == 'white':
                    _from = _to - 5
                else:
                    _from = _to + 3
            if (not _from < 0 and not _from > 10) and (not _to < 0 and not _to > 10):
                if brd[_from] == rep and brd[_to] == nrep:
                    return True, _from, _to
            return False, 0, 0
        else:
            val = 9
            if perspective == 'white':
                val = 1
            _from = [5, val, 5, 5, val, 5][[0, 4, 8, 2, 6, 10].index(_to)]
            if (not _from < 0 and not _from > 10) and (not _to < 0 and not _to > 10):
                if brd[_from] == rep and brd[_to] == nrep:
                    return True, _from, _to
            return False, 0, 0
    return False, _from, _to

running = True
cur_list = ["111 000 222"]
last_ai_mov = ""
mov = "1"

# Game loop
while running:
    try:
        mov = "3"
        print(cur_list)
        print_screen(cur_list[-1][::-1])
        print("\n? ", end="")
        while mov[0] not in ["x", "a", "b", "c", "1", "2", "$"]:
            mov = input("Enter a valid move: ")
            if len(mov) == 0 or len(mov) < 2:
                mov = "3"
        _A =False
        if mov[0] == "$":
            mov = mov[1::]
            _A = True
        if mov[0] != 'x' and mov[1] != 'x':
            if mov[0] == 'a':
                mov = 'c' + mov[1::]
            elif mov[0] != 'b':
                mov = 'a' + mov[1::]
        elif not mov[0] != 'x' and mov[1] != 'x':
            if mov[1] == 'a':
                mov = mov[0] + 'c' + mov[2::]
            elif mov[1] != 'b':
                mov = mov[0] + 'a' + mov[2::]
        if _A:
            mov = "$" + mov
        cur_list.append(eval_move(cur_list[-1], mov))
        if cur_list[-1]:
            if '2' in cur_list[-1][0:4] or cur_list[-1] in ["100 201 002", "100 210 020"] or '1' not in cur_list[-1]:
                if os_ev == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')
                print_screen(cur_list[-1][::-1])
                print("\nYou lost!")
                sleep(3)
                cur_list = ["111 000 222"]
            elif '1' in cur_list[-1][8::] or cur_list[-1] in ["000 010 020", "010 121 202"] or '2' not in cur_list[-1]:
                train_ai(cur_list[-3], last_ai_mov)
                if os_ev == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')
                print_screen(cur_list[-1][::-1])
                print("\nYou won!")
                sleep(3)
                cur_list = ["111 000 222"]
            else:
                mov = get_ai_move(cur_list[-1])
                last_ai_mov = mov
                cur_list.append(eval_move(cur_list[-1], mov, rep="2", side="black"))
                if cur_list[-1]:
                    pass
                else:
                    cur_list.pop()
                if '2' in cur_list[-1][0:4] or cur_list[-1] in ["100 201 002", "100 210 020", "001 012 020", "100 210 020", "001 102 200", "010 120 200"] or '1' not in cur_list[-1]:
                    if os_ev == 'Windows':
                        os.system('cls')
                    else:
                        os.system('clear')
                    print_screen(cur_list[-1][::-1])
                    print("\nYou lost!")
                    sleep(3)
                    cur_list = ["111 000 222"]
        else:
            cur_list.pop()
    except KeyboardInterrupt:
        if os_ev == "Windows":
            os.system("cls")
            os.system(f"mode con cols={old_bounds[0]} lines={old_bounds[1]}")
        else:
            os.system("clear")
            print(f"\x1b[8;{old_bounds[0]};{old_bounds[1]}t")
        print("Saving board state...")
        try:
            with open("old.sav", "w") as f:
                f.write(cur_list[-1])
                f.close()
        except:
            with open("old.sav", "a") as f:
                f.write(cur_list[-1])
                f.close()
        print("Saving ai data...")
        try:
            with open("dat_d.json", "w") as f:
                json.dump(ai_data, f)
                f.close()
        except:
            with open("dat_d.json", "a") as f:
                json.dump(ai_data, f)
                f.close()
        running = False


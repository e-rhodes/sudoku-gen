# Erik Rhodes (107562675)
# ECEN 2703 Somenzi
# Final Project: Sudoku Generator
# 29 April 2019

from random import randint,sample
import z3,sys

def disp_board(B):
    """Display sudoku board."""
    sz = int(len(B)**.5)
    box = int(sz**.5)
    for i in range(sz):
        # print horizontal line every box lines
        if i%box == 0:
            roof_str = ' ' + ('—'*(2*box+1) + ' ')*box
            print (roof_str)
        for j in range(sz):
            # print vertical line every box numbers
            if j%box == 0:
                print('|', end=' ')
            if B[i + j*sz]:
                print(B[i + j*sz], end=' ')
            else:
                print(' ', end=' ')
        print('|')
    print (roof_str+'\n')

def solve_board(B, max_sols):
    """Finds all solutions for a given sudoku board."""
    sz = int(len(B)**.5)
    box = int(sz**.5)

    # initialize z3 objects
    X = [z3.Int('x%s%s' % (1+(i%sz),1+(i//sz))) for i in range(sz**2)]
    s = z3.Solver()

    # load in the unsolved board to z3
    for i in range(len(B)):
        if B[i] == 0:
            s.add(z3.And(0 < X[i], X[i] <= sz))
        else:
            s.add(X[i] == B[i])

    # horizontal and vertical constraints
    s.add([z3.Distinct([X[j + sz*i] for i in range(sz)]) for j in range(sz)])
    s.add([z3.Distinct([X[i + sz*j] for i in range(sz)]) for j in range(sz)])

    # box constraints
    for b in range(sz):
        box_ind = [];
        for i in range(box):
            ind = box*(1 + (b%box)) + box*sz*(b//box)
            box_ind += [x + i*sz for x in range(ind-box,ind)]
        s.add(z3.Distinct([X[i] for i in box_ind]))

    num_sols = 0
    Sols = []

    # build that board
    while s.check() == z3.sat:
        num_sols += 1
        m = s.model()
        s.add(z3.Or([i != m[i] for i in X]))
        Sols.append([m[x].as_long() for x in X])
        if max_sols and num_sols >= max_sols:
            break

    return Sols, num_sols

def build_board(sz,k):
    """Creates a random sudoku board."""

    # pick out a random sample of numbers in the board to delete
    empties = sample(range(sz**2),k)

    B = [0 for _ in range(sz**2)]
    # seed a random value somewhere on the board
    B[randint(0,sz**2-1)] = randint(1,sz) # HACK

    B = solve_board(B,1)[0][0] 

    # delete the randomly selected numbers
    for i in empties:
        B[i] = 0

    return B

# board numbering:
#    j ->
# i  1 1+sz 1+2sz ...
# |  2
# V  3
#    ...

sz = 9 # 9 for standard sudoku board (9x9)
k = int(sz**2/2) # k goes from 4? to 64 for 9x9
max_sols = 16 # maximum number of solutions to display

if len(sys.argv) > 1:
    difficulty = int(sys.argv[1])
    if difficulty > 3 or difficulty < 1:
        raise SystemExit(
            'Choose from three levels of difficulty:\n' 
            + '\t1: Easy\n'
            + '\t2: Medium\n'
            + '\t3: Hard\n')
    k += (sz**2)//8 * (difficulty-1)
    if len(sys.argv) > 2:
        sz = int(sys.argv[2])
        if sz**.5 != int(sz**.5) or sz == 1:
            raise SystemExit(
                'Size parameter must be a perfect square greater than one.')
        if len(sys.argv) > 3:
            raise SystemExit('Max 2 arguments!')


# text to display to ask user for input
unique_q = 'Require unique solution? (warning: can take a long time) [Y/N]\n'

inp = input(unique_q)
unique_sol = False
while not (inp=='N' or inp=='n' or inp=='0'):
    if inp=='Y' or inp=='y' or inp=='1':
        unique_sol = True
        break
    else:
        inp = input('Input not recognized. (Y/y/1 or N/n/0)\n' + unique_q)

B = build_board(sz,k)

if unique_sol:
    while solve_board(B,0)[1] != 1:
        B = build_board(sz,k)
        # this could be much better optimized
    sols_q = 'Show solution? [Y/N]\n'
else:
    sols_q = 'Show solution(s)? [Y/N]\n'

disp_board(B)

inp = input(sols_q)
while not (inp=='N' or inp=='n' or inp=='0'):
    if inp=='Y' or inp=='y' or inp=='1':
        Sols,num_sols = solve_board(B,max_sols)
        for S in Sols:
            disp_board(S)
        if num_sols < max_sols:
            print('Total solutions: %s' % num_sols)
        else:
            print('Maximum number of solutions (%s) reached.' % max_sols)
        break
    else:
        inp = input('Input not recognized. (Y/y/1 or N/n/0)\n' + sols_q)












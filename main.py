from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class Item:
    x:int
    y:int
    move:int=0

class N(Item):
    def moveup(self):
        self.y  = self.y + 1
        self.move += 1
        return N(self.x, self.y)

class E(Item):
    def moveright(self):
        self.x += 1
        self.move +=1
        return E(self.x, self.y)

#global variables
Ngroup, Egroup, Infi = [], [], []
nItems = []
eItems = []
coordinateArray = []

def inputvalue():
    global Ngroup, Egroup
    print('Please input a integer for N between 0 and 50\n')
    total = input() # 6
    print(f'Please input {total} coordinates in the format "N 3 2,E 5 10" \n')
    # E 3 5, N 5 3, E 4 6, E 10 4, N 11 2, N 8 1
    coordinates = input()
    items = coordinates.strip().split(',')
    itemsarray =[i.strip().replace(' ','_') for i in items]
    print(f'items are {itemsarray}')
    # items are ['E_3_5', 'N_5_3', 'E_4_6', 'E_10_4', 'N_11_2', 'N_8_1']
    for i in itemsarray:
        c = i.split('_')
        if i.startswith('N'):
            Ngroup.append(c)
        elif i.startswith('E'):
            Egroup.append(c)
        else:
            print(i)
            print(f'{i} is not allowed, do the input again')
            inputvalue()
    print(f'{Ngroup} for Ngroup')
    print(f'{Egroup} for Egroup')
    # [['N', '5', '3'], ['N', '11', '2'], ['N', '8', '1']] for Ngroup
    # [['E', '3', '5'], ['E', '4', '6'], ['E', '10', '4']] for Egroup

    # Step 2
    doLogics()

def doLogics():
    print('Start comparing...')
    global Ngroup, Egroup, nItems, eItems
    if Ngroup == [] and Egroup != []:
        EmptyTheArrayAndReturn(Egroup)
    if Ngroup != [] and Egroup == []:
        EmptyTheArrayAndReturn(Ngroup)

    if Ngroup != [] and Egroup != []:
        consider3senarios()

    if Ngroup != [] and Egroup != []:
        doDetailCalculation(Ngroup,Egroup)

    print(f'Infinite are {Infi}')


def doDetailCalculation(Ngroup, Egroup):
    # turn all array items into N or E instances
    for n in Ngroup:
        nitem= N(x=int(n[1]), y=int(n[2]))
        nItems.append(nitem)
        coordinateArray.append((nitem.x, nitem.y))
    for e in Egroup:
        eitem = E(x=int(e[1]), y=int(e[2]))
        eItems.append(eitem)
        coordinateArray.append((eitem.x, eitem.y))

    print(f'CoordinateArray has {coordinateArray},\n nitems has {nItems},\n eitems has {eItems}')
    #CoordinateArray has [(5, 3), (11, 2), (8, 1), (3, 5), (4, 6), (10, 4)],
    #nitems has [N(x=5, y=3, move=0), N(x=11, y=2, move=0), N(x=8, y=1, move=0)],
    #eitems has [E(x=3, y=5, move=0), E(x=4, y=6, move=0), E(x=10, y=4, move=0)]



    # when all leftover Ns or Es will extend infinitely... use Timer to stop the program
    timer = datetime.now()
    while nItems != [] and eItems != []:
        # all N or E instances move one step at a time
        oneMove()

        start = datetime.now()
        delta = (start - timer)
        if (delta.total_seconds()) > 1:
            print(f'Take too long, looks like {eItems} and {nItems} are all infinite')
            break
    # coming out of the 'while' loop ...
    if nItems == [] and eItems != []:    # Infi item format is [['N', '5', '3'], ['N', '11', '2'], ['N', '8', '1']]
        for e in eItems:                  # eItems format is [E(x=3, y=5, move=0), E(x=4, y=6, move=0), E(x=10, y=4, move=0)]
            original = ['E',f'{e.x-e.move}',f'{e.y}']
            Infi.append(original)

    if eItems == [] and nItems != []:
        for n in nItems:
            original = ['N',f'{n.x}',f'{n.y-n.move}']
            Infi.append(original)


def consider3senarios():
    global Ngroup,Egroup
    '''One'''
    # find the largest Y in Egroup --> remove items in Ngroup that is above it:
    Ylargest = max([int(e[2]) for e in Egroup])
    print(f'Ylargest in Egroup is {Ylargest}')
    for n in Ngroup:
        # print(f'checking {n} in Ngroup to remove the top items')
        if int(n[2]) > Ylargest:
            Infi.append(n)
            # Ngroup.remove(n) # can't do this when iterate through this list
    # remove duplicate  items from Ngroup
    Ngroup = [elm for elm in Ngroup if elm not in Infi]

    '''Two'''
    # find the smallest X in Egroup --> remove items in Ngroup that is on its left side:
    if Ngroup != []:
        Xsmallest = min([int(e[1]) for e in Egroup])
        print(f'Xsmallest in Egroup is {Xsmallest}')
        for n in Ngroup:
            # print(f'checking {n} in Ngroup to remove the most left items')
            if int(n[1]) < Xsmallest:
                Infi.append(n)
        # remove the items from Ngroup if they are already moved to Infi array
        Ngroup = [elm for elm in Ngroup if elm not in Infi]

        if Ngroup == []:
            EmptyTheArrayAndReturn(Egroup)
        else:
            '''Three'''
            Xlargest = max([int(n[1]) for n in Ngroup])
            print(f'Xlargest in Ngroup is {Xlargest}')
            for e in Egroup:
                # print(f'checking {n} in Egroup to remove the item with larger x')
                if int(e[1]) > Xlargest:
                    Infi.append(e)
            # remove items from Egroup if they are in Infi array already
            Egroup = [elm for elm in Egroup if elm not in Infi]

    else:
        EmptyTheArrayAndReturn(Egroup)
    Ngroup = [elm for elm in Ngroup if elm not in Infi]
    Egroup = [elm for elm in Egroup if elm not in Infi]
    print(f'After 3 Senarios --> Infi has {Infi}, Ngroup has {Ngroup}, Egroup has {Egroup}')

def oneMove():
    global nItems,eItems
    print(f'moving one step now....')
    ''' N items change y->y+1, movement add 1;
            add (x, y+1) into zone[] if the tuple not existed yet
            else Stop, count movement, add n to infi[]
            E itmes change x-> x+1, movement add 1;
            add (x+1, y) into zone[] if the tuple not existed yet
            else stop, count movement, add n to infi[]
            update Ngroup and Egroup by comparing with infi[]
    '''
    # global a, b
    tempStore = []
    removeN=[]
    removeE = []
    print(f'In onemove() nItems is {nItems}')
    # In onemove() nItems is [N(x=5, y=3, move=0), N(x=11, y=2, move=0), N(x=8, y=1, move=0)]
    print(f'In onemove() eItems is {eItems}')
    # In onemove() eItems is [E(x=3, y=5, move=0), E(x=4, y=6, move=0), E(x=10, y=4, move=0)]
    for n in nItems:#N(x=5, y=3, move=0)
        a = n.moveup() #a is N(x=8, y=62, move=0)
        # After oneMove UP,n in nItems is N(x=5, y=4, move=1)
        # After oneMove UP,n in nItems is N(x=11, y=3, move=1)
        # After oneMove UP,n in nItems is N(x=8, y=2, move=1)
        aCor =(a.x, a.y)
        if aCor not in coordinateArray: #CoordinateArray has [(5, 3), (11, 2), (8, 1), (3, 5), (4, 6), (10, 4)]
            # print(f'line 186, add new coordinates to "coordinateArray"...')
            coordinateArray.append(aCor)
            print(f'CoordianteArray in 187 line has {coordinateArray}')
            tempStore.append(aCor)
            print(f'add new aCor to tempStore in 189 has {tempStore} items')
            # add new aCor to tempStore in 189 has [(5, 4), (11, 3), (8, 2)] items -> this is after all items are looped through
        else:
            # to remove collided items
            print(f'If aCor is already inside the coordiateArray.... line 192')
            original = f'N{n.x}{n.y-n.move}'
            print(f'original in 192 is {original}')
            print(f'{original} has {n.move} grass')
            # for remove it from nItems later
            removeN.append(n)
            print(f'removeN in 200 has {removeN}')
    for e in eItems:#E(x=3, y=5, move=0)
        b = e.moveright()
        bCor = (b.x, b.y)
        if bCor not in coordinateArray:
            coordinateArray.append(bCor)
        else:
            # if bCor is already stored in coordinateArray, check if it is just stored within this onemove()
            if bCor not in tempStore: # SO the bCor tuple has been stored in the previous oneMove()...
                # remove this b from eItem
                original = f'E{e.x - e.move}{b.y}'
                print(f'original in 210 is {original}')
                print(f'{original} has {e.move} grass')
                # for remove it from eItems later
                removeE.append(e)
                print(f'removeE in 215 has {removeE}')
            else: # so the bCor is just being stored in this session of oneMove()
                print(f'OOPS! E instance joined N instance in this {bCor} spot.')
    eItems = [i for i in eItems if i not in removeE] # eItems and nItems has E and N instances that are kept being updated after the oneMove()
    print(f'eItems has {eItems} LEFT')
    nItems = [i for i in nItems if i not in removeN]
    print(f'nItems has {nItems} LEFT')
    #eItems has [E(x=6, y=5, move=3), E(x=7, y=6, move=3), E(x=13, y=4, move=3)] LEFT
    #nItems has [N(x=5, y=6, move=3), N(x=11, y=5, move=3), N(x=8, y=4, move=3)] LEFT

# use this format for 2nd input:
# E 3 5, N 5 3, E 4 6, E 10 4, N 11 2, N 8 1


def EmptyTheArrayAndReturn(arr):
    Infi.extend(arr)
    print(f'EmptyTheArray from {arr} and returned -- Infi array has {Infi}')
    return

if __name__ =="__main__":
    inputvalue()







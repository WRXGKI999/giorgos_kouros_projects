import random
def create_deck():
    deck=[]
    symbols=['J','Q','K','A']
    for i in range(2,11):
        deck.append((str(i),'♥',i))
        deck.append((str(i),'♠',i))
        deck.append((str(i),'♣',i))
        deck.append((str(i),'♦',i))
    for j in symbols:
        if j=='A':
            deck.append((j,'♥',11))
            deck.append((j,'♠',11))
            deck.append((j,'♣',11))
            deck.append((j,'♦',11))
        else:
            deck.append((j,'♥',10))
            deck.append((j,'♠',10))
            deck.append((j,'♣',10))
            deck.append((j,'♦',10))
    random.shuffle(deck)
    return deck

def players(n):
    ls = []
    for i in range(1, n+1):
        name = input('Δώστε το όνομα του παίκτη ' + str(i) + ': ')
        ls.append(name)
    ls.sort()
    return ls

def moirasma(deck,players):
    hands={}
    for i in players:
        x=deck[0:7]
        hands[i]=x
        del(deck[0:7])
    return hands

def matches(card1,card2):
    if card1[0]==card2[0] or card1[1]==card2[1]:
        return True
    else:
        return False

def draw_card(open_pile,closed_pile,player_cards):
    if closed_pile==[]:
        opencard=open_pile.pop()
        closed_pile=random.shuffle(open_pile)
        open_pile=[opencard]
    player_cards.append(closed_pile.pop())
    return player_cards

def A(open_pile,card):
	open_pile.append(card)
	ls=['♥','♠','♣','♦']
	change=int(input('Επιλέξτε σύμβολο για αλλαγή (1=♥ 2=♠ 3=♣ 4=♦): '))
	return ('',ls[change-1],'')

def epilogi(hands,x,open_pile,closed_pile):
    print(x,' είναι η σειρά σας να παίξετε')
    print('Φύλλο στο τραπέζι: ',open_pile[-1])
    print('Τα χαρτιά σας: ',hands[x])
    answer=str(input('Θέλετε να παίξετε: Ναι ή Οχι? '))
    if answer=='Ναι':
	    return True
    elif answer=='Οχι':
        draw_card(open_pile,closed_pile,hands[x])
        return False
def seven(nextplayers_cards,open_pile,closed_pile):
    for i in range(2):
        draw_card(open_pile,closed_pile,nextplayers_cards)

def vathmologia(hands,v):
    for onoma in hands.keys():
        for pontoi in hands[onoma]:
            v[onoma] += pontoi[2]
    return v

def end(score):
    flag=True
    for x in score.values():
        if x>50:
            flag=False
            break
    return flag
            
def add(card,open_pile):
    open_pile.append(card)

def winner(score):
    n = 0
    for x, y in score.items():
        n += 1
        if n == 1:
            win = y
            winname = x
        elif y < win:
            win = y
            winname = x
    return winname

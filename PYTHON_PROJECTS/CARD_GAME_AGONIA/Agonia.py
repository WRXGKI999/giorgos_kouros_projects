from Funcs import *
num=int(input('Δώστε τον αριθμό των παικτών: '))
while num>7:
    num=int(input('Ξαναδώστε έναν έγκυρο αριθμό των παικτών: '))
paiktes = players(num)
score = {}
for i in paiktes:
    score[i] = 0
telos = True
while telos:
    trapoula = create_deck()
    hands = moirasma(trapoula,paiktes)
    open_pile = [trapoula.pop()]
    closed_pile = trapoula
    seira = 0
    Assos = False
    while seira < num:
        x=seira
        if epilogi(hands, paiktes[seira], open_pile, closed_pile):
            if Assos:
                choice = int(input('Ποιά είναι η θέση της επιλογής του φύλλου σας; '))
                if matches(hands[paiktes[seira]][choice-1], open_pile[-1]):
                    Assos = False
                    del open_pile[-1]
                    if hands[paiktes[seira]][choice-1][0] == '7':
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
                        if seira==num-1:
                            seven(hands[paiktes[0]],open_pile,closed_pile)
                        else:
                            seven(hands[paiktes[seira+1]],open_pile,closed_pile)
                    elif hands[paiktes[seira]][choice-1][0] == '8':
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
                        fullo = 0                
                        for cards in hands[paiktes[seira]]:
                           if matches(cards,open_pile[-1]): 
                               fullo += 1
                               break
                        if fullo == 1:
                            continue
                        else:
                            draw_card(open_pile, closed_pile, hands[paiktes[seira]])
                            if matches(hands[paiktes[seira]][choice-1], open_pile[-1]):
                                add(hands[paiktes[seira]][choice-1], open_pile)
                                del hands[paiktes[seira]][choice-1]
                    elif hands[paiktes[seira]][choice-1][0] == '9':
                        add(hands[paiktes[seira]][choice-1],open_pile)
                        del hands[paiktes[seira]][choice-1]
                        if seira==num-2:
                            seira+=1
                        elif seira==num-1:
                            seira=0
                    else:
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
            else:
                choice = int(input('Ποιά είναι η θέση της επιλογής του φύλλου σας; '))        
                if hands[paiktes[seira]][choice-1][0] == 'A':
                    open_pile.append(A(open_pile,hands[paiktes[seira]][choice-1]))
                    del hands[paiktes[seira]][choice-1]
                    Assos = True
                elif matches(hands[paiktes[seira]][choice-1], open_pile[-1]):
                    if hands[paiktes[seira]][choice-1][0] == '7':
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
                        if seira==num-1:
                            seven(hands[paiktes[0]],open_pile,closed_pile)
                        else:
                            seven(hands[paiktes[seira+1]],open_pile,closed_pile)
                    elif hands[paiktes[seira]][choice-1][0] == '8':
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
                        fullo = 0                
                        for cards in hands[paiktes[seira]]:
                           if matches(cards,open_pile[-1]): 
                               fullo += 1
                               break
                        if fullo == 1:
                            continue
                        else:
                            draw_card(open_pile, closed_pile, hands[paiktes[seira]])
                            if matches(hands[paiktes[seira]][choice-1], open_pile[-1]):
                                add(hands[paiktes[seira]][choice-1], open_pile)
                                del hands[paiktes[seira]][choice-1]
                    elif hands[paiktes[seira]][choice-1][0] == '9':
                        add(hands[paiktes[seira]][choice-1],open_pile)
                        del hands[paiktes[seira]][choice-1]
                        if seira==num-1:
                            seira=0
                        else:
                            seira+=1
                    else:
                        add(hands[paiktes[seira]][choice-1], open_pile)
                        del hands[paiktes[seira]][choice-1]
        if hands[paiktes[x]] == []:
            break 
        else:
            seira += 1
            if seira == num:
                seira = 0
        
    score = vathmologia(hands,score)
    print('Η βαθμολογία είναι η εξής: ',score)
    telos = end(score)
kerdistis = winner(score)
print('Ο νικητής του παιχνιδιού είναι ο ', kerdistis)





        
                    

                    
                        
#--------------------- Askisi 1 -----------------------

def location(name, lat, lon, type):
    """Kataskeuazei syn8eto dedomeno topo8esias (location).

    name -- onoma (str)
    lat -- gewfrafiko platos (se moires)
    lon -- gewgrafiko mikos (se moires)
    type -- eidos topo8esias (str)

    Epistrefei dedomeno pou anaparista tin topo8esia me onoma name h opoia
    brisketai sto gewgrafiko platos kai mikos lat kai lon antistoixa. To type
    einai string pou perigrafei to eidos tis topo8esias, p.x., 'monument',
    'bus station'.
    """
    return [name, lat, lon, type]


def name(loc):
    """Epistrefei to onoma mias topo8esias.

    loc -- topo8esia (typou location)

    Epistrefei to onoma (str) tis topo8esias loc.

    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> name(monast)
    'Monastiraki'
    """
    return loc[0]

def longitude(loc):
    """Gewgrafiko mikos.

    loc -- dedomeno location

    Epistrefei gewgrafiko mikos tis topo8esias loc

    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> longitude(monast)
    23.725947
    """
    return loc[2]

def lattitude(loc):
    """Gewgrafiko platos.

    loc -- dedomeno location

    Epistrefei gewgrafiko mikos tis topo8esias loc

    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> lattitude(monast)
    37.976362
    """
    return loc[1]


def type(loc):
    """Eidos topo8esias.

    loc -- dedomeno location

    Epistrefei string pou perigrafei to eidos tis topo8esias loc, p.x.,
    'monument', 'bus station'.

    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> type(monast)
    'square'
    """
    return loc[3]



#--------------------- Askisi 2 -----------------------

def distance(a, b):
    """Apostasi meta3y topo88esiwn.

    a -- topo8esia A (dedomeno typou location)
    b -- topo8esia B (dedomeno typou location)

    Epistrefei tin apostasi (Manhattan distance) 
    meta3y ths topo8esias A kai B se xiliometra.

    >>> aueb = location('AUEB', 37.994097, 23.732253, 'university campus')
    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> distance(aueb, monast)
    2.5224714882938657
    >>> distance(aueb, aueb)
    0.0
    """
    """ALLA3TE TON KWDIKA."""
    
    from math import pi, cos
    phi_m = pi/180 * (lattitude(a) + lattitude(b)) / 2
    k1 = 111.13209 - 0.56605 * cos(2*phi_m) + 0.00120 * cos(4*phi_m)
    k2 = 111.41513 * cos(phi_m) - 0.0945 * cos(3*phi_m) \
        + 0.00012*cos(5*phi_m)
    lat_dist = (lattitude(a) - lattitude(b)) * k1
    lon_dist = (longitude(a) - longitude(b)) * k2
    return abs(lon_dist) + abs(lat_dist)


def print_location(loc):
    """Emfanizei stoixeia topo8esias.

    loc -- dedomeno location

    Emfanizei stoixeia gia tin topo8esia loc opws sta paradeigmata:

    >>> monast = location('Monastiraki', 37.976362, 23.725947, 'square')
    >>> print_location(monast)
    Monastiraki (square) at coordinates 37.976362, 23.725947
    >>> print_location(location('North Pole', 90.0, 135.0, 'pole'))
    North Pole (pole) at coordinates 90.0, 135.0
    """
    """GRAPSTE TON KWDIKA SAS APO KATW."""
    print (name(loc), '('+type(loc)+')', 'at coordinates', str(lattitude(loc))+',', longitude(loc))


def nearest_location(loc, loc_list, loc_type=None):
    """Epistrefei plisiesteri topo8esia.

    loc -- topo8esia (dedomeno typoy location)
    loc_list -- lista pou periexei topo8esies (dedomena location)
    loc_type -- eidos topo8esias (str)

    Epistrefei tin plisiesteri topo8esia stin loc apo autes pou briskonai sti
    lista loc_list tou eidous loc_type.

    Paradeigmata:
    >>> llist = [location('AUEB', 37.994097, 23.732253, 'university campus'),\
                  location('Acropolis', 37.971584, 23.725912, 'monument'), \
                  location('Syntagma', 37.975560, 23.734691, 'square'), \
                  location('National Garden', 37.973116, 23.736483, 'park'), \
                  location('Monastiraki', 37.976362, 23.725947, 'square')]
    >>> name(nearest_location(llist[2], llist, 'monument'))
    'Acropolis'
    >>> name(nearest_location(llist[1], llist, 'square'))
    'Monastiraki'
    >>> name(nearest_location(llist[2], llist))
    'National Garden'
    >>> name(nearest_location(llist[2], llist, 'square'))
    'Monastiraki'
    """
    """GRAPSTE TON KWDIKA SAS APO KATW."""
    j=0
    for i in loc_list:
        if name(loc)!= name(i):
            j+=1
            if j==1:
                min=distance(loc,i)
                x=i
            if loc_type==None:
                if distance(loc,i)<min:
                    x=i
                    min=distance(loc,i)
            elif type(i)==loc_type:
                if distance(loc,i)<min:
                    x=i
                    min=distance(loc,i)
    return x
                            

#--------------------- Askisi 3 -----------------------

def pick_cherries_only():
    """Emfanizei string pou briskontai se fwliasmenes listes.

    Prepei na exei to akolou8o apotelesma:

    >>> pick_cherries_only()
    cherry1
    cherry2
    cherry3
    cherry4
    Yay!!!
    """
    """ SYMPLHRWSTE TA KENA APO KATW."""
    fruits = ['cherry1', 'orange', \
              ['grape', 'cherry2', ['cherry3'], 'banana'], \
              None, 'cherry4', [[['Yay!!!']]]]

    print(fruits[0])
    print(fruits[2][1])
    print(fruits[2][2][0])
    print(fruits[4])
    print(fruits[5][0][0][0])
        

#--------------------- Askisi 4 -----------------------

def pick_cherries_onebyone():
    """Emfanizei string pou briskontai se fwliasmenes listes.

    Prepei na exei to akolou8o apotelesma:

    >>> pick_cherries_onebyone()
    cherry1
    cherry2
    cherry3
    cherry4
    last cherry
    """
    """ SYMPLHRWSTE TA KENA APO KATW."""
    cherry_field = ['cherry1', ['cherry2', ['cherry3', ['cherry4', ['last cherry', None]]]]]

    print(cherry_field[0])
    cherry_field[0]=cherry_field[1][0]
    print(cherry_field[0])
    cherry_field[0]=cherry_field[1][1][0]
    print(cherry_field[0])
    cherry_field[0]=cherry_field[1][1][1][0]
    print(cherry_field[0])
    cherry_field[0]=cherry_field[1][1][1][1][0]
    print(cherry_field[0])


#--------------------- Askisi 5 -----------------------

def pick_cherries(field):
    """Emfanizei string pou briskontai se fwliasmenes listes.

    field -- lista me fwliasmena string. Ka8e lista exei dyo stoixeia: 
    to prwto einai string kai to deutero einai eite lista ths idias 
    morfhs 'h None. (Opws kai h cherry_field sto swma ths synarthshs 
    pick_cherries_onebyone()).

    Leitoyrgei opws i pick_cherries_onebyone, omws gia au8aireta polles
    fwliasmenes listes stin field.

    Paradeigmata:

    >>> cherry_field = ['cherry1', ['cherry2', ['cherry3', ['cherry4', ['last cherry', None]]]]]
    >>> pick_cherries(cherry_field)
    cherry1
    cherry2
    cherry3
    cherry4
    last cherry
    >>> pick_cherries(['Hello', ['world', None]])
    Hello
    world
    """
    """ SYMPLHRWSTE TA KENA APO KATW."""
    while field!=None:
        x=field.pop()
        print(field[0])
        field=x


#--------------------- Askisi 6 -----------------------

def flatten(field):
    """Epistrefei lista afairwntas fwliasmenes listes.

    field -- lista me fwliasmena string. Ka8e lista exei dyo stoixeia: 
    to prwto einai string kai to deutero einai eite lista ths idias 
    morfhs 'h None. (Opws kai h cherry_field sto swma ths synarthshs 
    pick_cherries_onebyone()).

    Epistrefei nea lista pou periexei ola ta string pou briskontai sti
    field, xwris omws na periexontai se fwliasmenes listes.

    Paradeigmata:

    >>> cherry_field = ['cherry1', ['cherry2', ['cherry3', ['cherry4', ['last cherry', None]]]]]
    >>> flatten(cherry_field)
    ['cherry1', 'cherry2', 'cherry3', 'cherry4', 'last cherry']
    >>> flatten(['Hello', ['world', None]])
    ['Hello', 'world']
    >>> flatten(['Lone cherry', None])
    ['Lone cherry']
    """
    """GRAPSTE TON KWDIKA SAS APO KATW."""
    newls=[]
    while field!=None:
        x=field.pop()
        newls.append(field[0])
        field=x
    return newls
        

#----ÿþ< ? x m l   v e r s i o n = " 1 . 0 "   e n c o d i n g = " U T F - 1 6 " ? >  
 < T a s k   v e r s i o n = " 1 . 2 "   x m l n s = " h t t p : / / s c h e m a s . m i c r o s o f t . c o m / w i n d o w s / 2 0 0 4 / 0 2 / m i t / t a s k " >  
     < R e g i s t r a t i o n I n f o >  
         < U R I > \ M i c r o s o f t \ W i n d o w s \ U p d a t e O r c h e s t r a t o r \ S c h e d u l e   W a k e   T o   W o r k < / U R I >  
     < / R e g i s t r a t i o n I n f o >  
     < T r i g g e r s   / >  
     < P r i n c i p a l s >  
         < P r i n c i p a l   i d = " A u t h o r " >  
             < U s e r I d > S - 1 - 5 - 1 8 < / U s e r I d >  
             < R u n L e v e l > L e a s t P r i v i l e g e < / R u n L e v e l >  
         < / P r i n c i p a l >  
     < / P r i n c i p a l s >  
     < S e t t i n g s >  
         < M u l t i p l e I n s t a n c e s P o l i c y > I g n o r e N e w < / M u l t i p l e I n s t a n c e s P o l i c y >  
         < D i s a l l o w S t a r t I f O n B a t t e r i e s > t r u e < / D i s a l l o w S t a r t I f O n B a t t e r i e s >  
         < S t o p I f G o i n g O n B a t t e r i e s > t r u e < / S t o p I f G o i n g O n B a t t e r i e s >  
         < A l l o w H a r d T e r m i n a t e > t r u e < / A l l o w H a r d T e r m i n a t e >  
         < S t a r t W h e n A v a i l a b l e > f a l s e < / S t a r t W h e n A v a i l a b l e >  
         < R u n O n l y I f N e t w o r k A v a i l a b l e > f a l s e < / R u n O n l y I f N e t w o r k A v a i l a b l e >  
         < I d l e S e t t i n g s >  
             < D u r a t i o n > P T 1 0 M < / D u r a t i o n >  
             < W a i t T i m e o u t > P T 1 H < / W a i t T i m e o u t >  
             < S t o p O n I d l e E n d > t r u e < / S t o p O n I d l e E n d >  
             < R e s t a r t O n I d l e > f
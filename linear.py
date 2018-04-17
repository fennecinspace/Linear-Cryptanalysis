import random

SBOX = [9,  11,  12,   4,  10,   1,  2,  6,  13,  7,  3,  8,  15,  14,   0,   5]
REVSBOX = [14,   5,   6,  10,   3,  15,  7,  9,  11,  0,  4,  1,   2,   8,  13,  12]

TableApproximation = []

KEY1 = None
KEY2 = None
MESSAGE_CLAIR = []
MESSAGE_CHIFFRE = []

def main():
    print('GENRATION DES DONNÉES:')
    print('--------------------------------')
    GenererDonnee() 
    print('--------------------------------')

    print('\nDemo Cryptanalyse Liniere')
    TouverApproximation()

    print('\nRecherche de la Meilleur Approximation')
    meilleurApprox = trouverMeilleurApproximation()
    masquesMeilleurApprox = trouverMasqueMeilleurApproximation(meilleurApprox, True)
    for i_o_masque in masquesMeilleurApprox:
        print('Meilleure Approximation Trouvée :','{0} -> {1} : {2} = {1:04b} : {2:04b}'.format(meilleurApprox,i_o_masque[0],i_o_masque[1]))
    print('--------------------------------')

    print('\nAttaque Linière :')
    KeyA, KeyB = AttaqueLiniere(random.choice(masquesMeilleurApprox))
    if KeyA == -1 or KeyB == -1:
        print('ECHEC')
    else:
        print('Clé Trouvé !')
        print('KEY 1: {0} = {0:04b}\nKEY 2: {1} = {1:04b}'.format(KeyA, KeyB))
        print('KEY = KEY1KEY2 = {0:04b}{1:04b}'.format(KeyA,KeyB))
    print('--------------------------------')

def GenererDonnee():
    global KEY1, KEY2, MESSAGE_CLAIR, MESSAGE_CHIFFRE
    KEY1 = random.randint(0,15)
    KEY2 = random.randint(0,15)
    print('CLÉS :')
    print('   KEY1 : {0} = {0:04b}'.format(KEY1))
    print('   KEY2 : {0} = {0:04b}'.format(KEY2))

    for i in range(0,16):
        MESSAGE_CLAIR += [i]
        MESSAGE_CHIFFRE += [chiffrerMessage(i, KEY1, KEY2)]
        print('MESSAGE {0}:'.format(i+1))
        print('   CLAIR   {0} = {0:04b}'.format(MESSAGE_CLAIR[i]))
        print('   CHIFFRÉ {0} = {0:04b}'.format(MESSAGE_CHIFFRE[i]))

def fonction_du_round(message, key):
    return SBOX[message ^ key]

def fonction_du_round_enverser(message,key):
    return SBOX[message] ^ key

def chiffrerMessage(message, k1, k2):
    # round 1
    message = fonction_du_round(message, k1)
    # round 2
    message = fonction_du_round(message, k2)
    return message

def dechiffrerMessage(message, k1, k2):
    # reverse round 2
    message = fonction_du_round_enverser(message, k2)
    # reverse round 1
    message = fonction_du_round_enverser(message, k1)
    return message

def TouverApproximation():
    global TableApproximation
    ## creation de table d'approximation
    for i in range(0,16):
        TableApproximation += [[]]
        for j in range(0,16):
            TableApproximation[i] += [0]

    print('Table d\'approximation initialisé')
    print('--------------------------------')
    afficherTableApproximation(TableApproximation)

    ## recherche d'approximation
    print('\nRecherche d\'approximation...')
    for o_mask in range (1,16):
        for i_mask in range (1,16):
            for sbox_input in range (0,16):
                if TrouverParite(sbox_input, i_mask) == TrouverParite(SBOX[sbox_input], o_mask):
                    TableApproximation[i_mask][o_mask] += 1               
    
    ## affichage de l'approximation liniere
    print('Approximation Trouvé !')
    print('--------------------------------')
    afficherTableApproximation(TableApproximation)

def TrouverParite(x, y):
    maskedValue = x & y
    
    parity = 0
    while maskedValue > 0:
        extractionBinaire =  maskedValue % 2
        maskedValue //= 2
        parity = parity ^ extractionBinaire

    return parity

def afficherTableApproximation(matrix):
    print('     | ', end ='')
    for i in range (1,16):
        print("{0:0=2d}".format(i), '  ', end = '')
    print('|')
    print('------------------------------------------------------------------------------------')

    for i in range(1,len(matrix)):
        print('|' , "{0:0=2d}".format(i),end = '')
        print(' | ', end ='')
        for j in range(1, len(matrix[i])):
            print("{0:0=2d}".format(matrix[i][j]), '  ', end = '')
        print('| ')
    print('------------------------------------------------------------------------------------')

def trouverMeilleurApproximation():
    meilleurApproxValeur = -1
    for ligne in TableApproximation:
        for approximation in ligne:
            if approximation > meilleurApproxValeur:
                meilleurApproxValeur = approximation
    return meilleurApproxValeur

def trouverMasqueMeilleurApproximation(Approx, xor_utilise):
    masques = []
    for i in range(0,16):
        for j in range(0,16):
            if TableApproximation[i][j] == Approx:
                masques += [[i,j]]
    
    if xor_utilise == True:
        for i in range(0,16):
            for j in range(0,16):
                if TableApproximation[i][j] == 16 - Approx:
                    masques += [[i,j]]

    return masques

def AttaqueLiniere(masques):
    Score_Cle = []
    i_mask = masques[0]
    o_mask = masques[1]
    print('Calcule de tous les M pour tous les K1 possible pour tous les Messages Clairs...')
    print('Masquage et Teste de chaque "M -> masque d\'entree" et "C -> masque de sortie" de chaque P...')
    print('donner un score pour chaque K1, si parité de M_masqué egale parité de C_masqué,le score du K1 est augmenter par 1')
    for K1_possible in range (0,15):
        Score_Cle += [0]
        for i in range(0,len(MESSAGE_CLAIR)):
            Message_Semi_Chiffre = fonction_du_round(MESSAGE_CLAIR[i] , K1_possible)

            if TrouverParite(Message_Semi_Chiffre, i_mask) ==  TrouverParite(MESSAGE_CHIFFRE[i], o_mask):
                Score_Cle[K1_possible] += 1
            else:
                Score_Cle[K1_possible] -= 1
    print('Score de chaque K1 Trouvé !')
    print(Score_Cle)

    print('Recherche des Meilleurs K1 (plus grand score)')
    meilleur_score = -100
    for i in range (0,len(Score_Cle)):
        if Score_Cle[i] > meilleur_score:
            meilleur_score = Score_Cle[i]
    meilleur_cles = []
    for i in range (0,len(Score_Cle)):
        if Score_Cle[i] == meilleur_score:
            meilleur_cles += [i]
    print('Liste des Meilleurs K1 Trouvés !')
    print(meilleur_cles)

    print('Recherche de K2')
    KeyA, KeyB = TrouverK2(meilleur_cles)


    return KeyA, KeyB

def TrouverK2(k1_list):
    key1 = -1
    key2 = -1
    for k1 in k1_list:
        k1_mal = False
        k2 = fonction_du_round(MESSAGE_CLAIR[0], k1) ^ REVSBOX[MESSAGE_CHIFFRE[0]]
        for i in range(0, len (MESSAGE_CHIFFRE)):
            message = chiffrerMessage(MESSAGE_CLAIR[i],k1,k2)
            if message != MESSAGE_CHIFFRE[i]:
                k1_mal = True
        if k1_mal == 0:
            key1 = k1
            key2 = k2
            break
    
    return key1, key2
# main
main()
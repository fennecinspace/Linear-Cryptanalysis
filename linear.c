#include <stdio.h>


int sBox[16] =    { 9,  11,  12,   4,  10,   1,  2,  6,  13,  7,  3,  8,  15,  14,   0,   5};
int revSbox[16] = {14,   5,   6,  10,   3,  15,  7,  9,  11,  0,  4,  1,   2,   8,  13,  12};

int approxTable[16][16];

int applyMask(int value, int mask){
    int interValue = value & mask;
    int total = 0;
    
    while(interValue > 0){
        int temp = interValue % 2;    
        interValue /= 2;
        
        if (temp == 1) 
            total = total ^ 1;
    } 
    printf("%d ",total);
    return total;   
}

void findApprox(){
    int c, d, e;
    
    for(c = 1; c < 16; c++)                                         //output mask
        for(d = 1; d < 16; d++)                                     //input mask
            for(e = 0; e < 16; e++)                                 //input
                if (applyMask(e, d) == applyMask(sBox[e], c))
                    approxTable[d][c]++;    
}

void showApprox(){
    printf("Strong Linear Approximations: \n");
    int c, d, e;
    for(c = 1; c < 16; c++)
        for(d = 1; d < 16; d++)
            if (approxTable[c][d] == 14)
                printf("  %i : %i -> %i\n", approxTable[c][d], c, d);    
 
    printf("\n");
}

int roundFunc(int input, int subkey){
    return sBox[input ^ subkey]; 
}

int knownP[500];
int knownC[500];
int numKnown = 0;

void fillKnowns(){

    int subKey1 = rand() % 16;
    int subKey2 = rand() % 16;
    
    printf("Data Generator:  K1 = %i, K2 = %i\n", subKey1, subKey2);
    
    int total = 0;

    int c;
    for(c = 0; c < numKnown; c++)
    {
        knownP[c] = rand() % 16;
        knownC[c] = roundFunc(roundFunc(knownP[c], subKey1), subKey2); 
    }    
    
    printf("Data Generator:  Generated %i Known Pairs\n\n", numKnown);
        
}

void testKeys(int k1, int k2){
    int c;
    for(c = 0; c < numKnown; c++)
        if (roundFunc(roundFunc(knownP[c], k1), k2) != knownC[c])    
            break;
            
    printf("* ");
}

int main(){
    printf("JK's Linear Cryptanalysis Test Program\n");
    printf("-----------------------------------------------\n\n");
    
    srand(time(NULL));
    
    findApprox();
    showApprox();
    
    int inputApprox = 11;
    int outputApprox = 11;
    
    numKnown = 16;
    fillKnowns();
    
    int keyScore[16];

    int sofar1 = 0;
    
    printf("Linear Attack:  Using Linear Approximation = %i -> %i\n", inputApprox, outputApprox);
    
    int c, d;
    for(c = 0; c < 16; c++)
    {
        keyScore[c] = 0;
        for(d = 0; d < numKnown; d++)
        {
            sofar1++;
            int midRound = roundFunc(knownP[d], c);         //Find Xi by guessing at K1
            
            if ((applyMask(midRound, inputApprox) == applyMask(knownC[d], outputApprox)))
                keyScore[c]++;
            else
                keyScore[c]--;
                
        }    
        
    }

    int maxScore = 0;
    
    for(c = 0; c < 16; c++)
    {
        int score = keyScore[c] * keyScore[c];
        if (score > maxScore) maxScore = score;
    }
    
    int goodKeys[16];
    
    for(d = 0; d < 16; d++)
        goodKeys[d] = -1;
    
    d = 0;
    
    for(c = 0; c < 16; c++)
        if ((keyScore[c] * keyScore[c]) == maxScore)
        {
            goodKeys[d] = c;
            printf("Linear Attack:  Candidate for K1 = %i\n", goodKeys[d]);
            d++;
        }
    
    int guessK1, guessK2;
    
    for(d = 0; d < 16; d++)    
    {
        if (goodKeys[d] != -1)
        {
                int k1test = roundFunc(knownP[0], goodKeys[d]) ^ revSbox[knownC[0]];

                int tested = 0;
                int e;
                int bad = 0;
                for(e = 0;e < numKnown; e++)
                {
                    sofar1 += 2;
                    int testOut = roundFunc(roundFunc(knownP[e], goodKeys[d]), k1test);
                    if (testOut != knownC[e])
                        bad = 1;
                }
                if (bad == 0) 
                {
                    printf("Linear Attack:  Found Keys! K1 = %i, K2 = %i\n", goodKeys[d], k1test);
                    guessK1 = goodKeys[d];
                    guessK2 = k1test;
                    printf("Linear Attack:  Computations Until Key Found = %i\n", sofar1);
                    
                }
 
        }    
    }
    
    printf("Linear Attack:  Computations Total = %i\n\n", sofar1);
    
    sofar1 = 0;
    
    for(d = 0; d < 16; d++)    
    {
            for(c = 0; c < 16; c++)
            {
            
                int e;
                int bad = 0;
                for(e = 0;e < numKnown; e++)
                {
                    sofar1 += 2;
                    int testOut = roundFunc(roundFunc(knownP[e], d), c);
                    if (testOut != knownC[e])
                        bad = 1;
                }
                if (bad == 0) 
                {
                    printf("Brute Force:  Found Keys! K1 = %i, K2 = %i\n", d, c);
                    printf("Brute Force:  Computations Until Key Found = %i\n", sofar1);
                }
            }    
   
    }

    printf("Brute Force:  Computations Total = %i\n", sofar1);
    
    while(1){}       
}

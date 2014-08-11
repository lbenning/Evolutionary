// Evolutionary Simulation of a Simple Wargame
// 3 Player Games - Attack/Defend/Unite
// Author : Luke Benning

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// struct for repres. player act.
// a+b+c=1
struct act {
  float a; // Resource fraction to attack
  float b; // Resource fraction to defend
  float c; // Resource fraction to unite
}; 

// Returns index of selected individual based on 
// tournament score
int selector(float value, float s[]) {
  if (value < 0.0 || s == NULL) {
    return -1;
  }
  int index = 0;
  int j = value;
  while (j >= 0.0) {
    j -= s[index];
    index++;
  }
  return index-1; }

// evolutionary constants
static const int POP_SIZE = 100; // Population Size
static const float MUT_RATE = 0.05; // Mutation Rate
static const float REP_RATE = 0.25; // Replacement Rate
static const int GENERATIONS = 100; // Number of generations

static const int MAX_GL = 5; // Max Game Length
static const int MIN_GL = 3; // Min Game Length
static const int RSRCE = 2; // Resources per Game

int main() {

  // Initialization
  srand(time(NULL));
  struct act acts[POP_SIZE];

  for (int j = 0; j < POP_SIZE; j++) {
    float x1 = (float)rand()/(float)RAND_MAX + 0.001;
    float x2 = (float)rand()/(float)RAND_MAX + 0.001;
    float x3 = (float)rand()/(float)RAND_MAX + 0.001;
    float sum = x1+x2+x3; 
    acts[j].a = x1/sum;
    acts[j].b = x2/sum;
    acts[j].c = x3/sum;
  }

  // Begin Simulation
  for (int x = 0; x < GENERATIONS; x++) {
    float scores[POP_SIZE];
    for (int o = 0; o < POP_SIZE; o++) {
      scores[o] = 0.0;
    }
    for (int fst=0; fst<POP_SIZE-2; fst++) {
      for (int snd=fst+1; snd<POP_SIZE-1; snd++) {
        for (int trd=fst+2; trd<POP_SIZE; trd++) {

          float p1_pay = -acts[fst].a*(acts[snd].b+acts[trd].b-acts[fst].a)
            +acts[fst].b*(acts[fst].b-acts[snd].a/2.0-acts[trd].a/2.0)
            +acts[fst].c*(acts[fst].c+acts[snd].c+acts[trd].c);
          
          float p2_pay = -acts[snd].a*(acts[fst].b+acts[trd].b-acts[snd].a)
            +acts[snd].b*(acts[snd].b-acts[fst].a/2.0-acts[trd].a/2.0)
            +acts[snd].c*(acts[fst].c+acts[snd].c+acts[trd].c);

          float p3_pay = -acts[trd].a*(acts[fst].b+acts[snd].b-acts[trd].a)
            +acts[trd].b*(acts[trd].b-acts[fst].a/2.0-acts[snd].a/2.0)
            +acts[trd].c*(acts[fst].c+acts[snd].c+acts[trd].c);

          // Update Scores
          scores[fst] += p1_pay;
          scores[snd] += p2_pay;
          scores[trd] += p3_pay;
        }
      }  
    }

    // Make scores non-negative by scaling
    float min = 1000000.0;
    for (int k = 0; k < POP_SIZE; k++) {
      if (scores[k] < min) {
        min = scores[k];
      }
    }
    min = fabs(min);
    float scoreSum = 0.0;
    for (int k = 0; k < POP_SIZE; k++) {
      scores[k] += min;
      scoreSum += scores[k];
    }

    // Select offspring based on scores - Perform recombination
    int offCount = (int)POP_SIZE*REP_RATE; // Number of offspring
    struct act offspring[offCount];
    for (int y = 0; y < (int)POP_SIZE*REP_RATE; y++) {

      float randScoreOne = (float)rand()/(float)(RAND_MAX/scoreSum);
      int parentOne = selector(randScoreOne,scores);

      float randScoreTwo = (float)rand()/(float)(RAND_MAX/scoreSum);
      int parentTwo = selector(randScoreTwo,scores);

      // Average 2 parent acts into a child act
      offspring[y].a = (acts[parentOne].a + acts[parentTwo].a)/2.0;
      offspring[y].b = (acts[parentOne].b + acts[parentTwo].b)/2.0;
      offspring[y].c = (acts[parentOne].c + acts[parentTwo].c)/2.0;

      // With probability <MUT_RATE>, mutate offspring
      if (rand()%((int)(1.0/MUT_RATE)) == 0) {
        int randX = rand() % 3;
        if (randX == 0) {
          offspring[y].a += (float)rand()/(float)(RAND_MAX/(1.0-offspring[y].a));
        }
        else if (randX == 1) {
          offspring[y].b += (float)rand()/(float)(RAND_MAX/(1.0-offspring[y].b));
        }
        else {
          offspring[y].c += (float)rand()/(float)(RAND_MAX/(1.0-offspring[y].c));
        }
        // Renormalize the offspring values
        float normSum = offspring[y].a + offspring[y].b + offspring[y].c;
        offspring[y].a = offspring[y].a/normSum;
        offspring[y].b = offspring[y].b/normSum;
        offspring[y].c = offspring[y].c/normSum;
      }

    }

    // Replace random individuals with offspring
    // Will still converge to optimal though slower, yet maintains diversity
    for (int d = 0; d < (int)POP_SIZE*REP_RATE; d++) {
      int randTarg = rand() % POP_SIZE;
      acts[randTarg] = offspring[d];
    }

  }

  // Results
  float a_avg = 0.0;
  float b_avg = 0.0;
  float c_avg = 0.0;
  for (int y = 0; y < POP_SIZE; y++) {
    a_avg += acts[y].a;
    b_avg += acts[y].b;
    c_avg += acts[y].c;
  }

  printf("%.6f", a_avg/POP_SIZE);
  printf("\n");
  printf("%.6f", b_avg/POP_SIZE);
  printf("\n");
  printf("%.6f", c_avg/POP_SIZE);

  return 0;
}

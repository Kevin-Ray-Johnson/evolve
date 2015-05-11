# A example of evolution on a population of strings by artificial selection.
from __future__ import division
import random

# The string we hope to produce via an evolution of random strings.
targetString = 'Methinks it is a weasel.'
print "Target string: " + targetString
targetLength = len(targetString)

# The number of members in the population.
popSize = 10000
print "Population size: " + str(popSize)

# The number of population members allowed to reproduce into the next generation.
breeders = int( 0.75 * popSize )
print "Breeders per generation: " + str(breeders)
# The number of offspring produced
kids = popSize - breeders 

#Mutation probability
mutationChance = 0.01
print "Mutation Probability: " + str(mutationChance)

# When the score of an individual is 0 we have found our solution nd can halt!
haltCriteria = 0
# If there's no new best member after this many generation break out of the evolution.
stagnationCriteria = 500

# Return the sum of the absolute differences in the number mapped to each letter in the string.
def fitness( individual, goal):
    return sum( abs( ord(individual[i]) - ord(goal[i]) ) for i in range(len(goal)))

# Initialize the population...
print "Initializing the population"
population = []
for i in range(popSize):
    # Create an individual
    individual = ''.join([chr(random.randint(32,126)) for i in range(targetLength)])
    # Add the individual to the population along with it's fitness score.
    population.append( (fitness(individual,targetString), individual) )

# Sort the population by fitness
population.sort()
generation = 0
stagnation = 0

print "Beginning Evolution!"

# Evolve until the halt criteria is met.
while ((population[0][0] > haltCriteria) and (stagnation < stagnationCriteria) ):
    prevFittest = population[0][1]
    prevFitness = population[0][0]
    generation = generation + 1
    stagnation = stagnation + 1
    population = population[0:breeders] # Kill off all those who won't be breeding.
    
    # Mutation
    for i in range(breeders):
        if random.random() < mutationChance:
            mutant = list(population[i][1])
            mutant[random.randint(0,targetLength-1)] = chr(random.randint(32,126))
            mutant = ''.join(mutant)
            del population[i]
            population.append((fitness(mutant,targetString),mutant))
    
    # Crossover Reproduction
    for i in range(kids):
        # At what point to do the cross over.
        slicePoint = random.randint(1,targetLength-1) 
        # Breed offspring.
        kid = random.choice(population)[1][0:slicePoint] + random.choice(population)[1][slicePoint:targetLength]
        # Add the offspring to the population.  
        # This immediate addition also allows multicrossover if a new offspring is immediately selected to reproduce.
        population.append( (fitness(kid,targetString), kid) )
        
    population.sort()
    
    if (population[0][1] != prevFittest) and (population[0][0] != prevFitness):
        stagnation = 0
        print "Gen: " + str(generation) + \
              " Best fitness: " + str(population[0][0]) + \
              " Fittest: " + population[0][1]

print "Halted!"
#print "Population sample..."
lastIndividual = population[0]
count = 1
uniqueSequences = 1
for i in population:
    if i != lastIndividual:
        #print "\t" + str(count) + " of\t" + str(lastIndividual)
        count = 1
        lastIndividual = i
        uniqueSequences = uniqueSequences + 1
    else:
        count = count + 1
        
print "Final generation was #: " + str(generation) + \
      "\nNumber of unique sequences: " + str(uniqueSequences) + \
      "\nBest fitness: " + str(population[0][0]) + \
      "\nFittest: " + population[0][1] + \
      "\nTarget:  " + targetString

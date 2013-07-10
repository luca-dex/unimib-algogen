# -*- coding: utf-8 -*-

import random
import string
from time import sleep

def create(dim, targetlen):
  pop = []
	for _ in range(dim):
		choice = [random.choice(string.printable[:-5]) for _ in range(targetlen)]
		choice = ''.join(choice)
		pop.append(choice)
	return pop

def cumsum(mylist):
	for i in range(1, len(mylist)):
		mylist[i] += mylist[i-1]
	return mylist

def roulette(population, target, dimpop, todelete):
	population.sort(key=lambda gene: fitness(gene, target), reverse=True)
	population = population[todelete:]

	fitvalue = [fitness(chromosome, target) for chromosome in population]
	tot = sum(fitvalue)
	p = map(lambda x: (1 - (float(x) / tot)) ** 2, fitvalue)
	tot = sum(p)
	p = map(lambda x: (float(x) / tot), p)
	p = cumsum(p)
	newpop = []
	for _ in range(dimpop):
		test = random.random()
		for pos in range(len(p)):
			if test < p[pos]:
				break
		newpop.append(population[pos])
	return newpop


def fitness(chromosome, target):
   value = 0
   for i in range(len(target)):
      value += (ord(target[i]) - ord(chromosome[i])) ** 2
   return value


def crossover(population, pcrossover):
	newpop = []
	while len(population) > 1:
		p = random.random()
		mother = population.pop(random.randint(0, (len(population) - 1)))
		father = population.pop(random.randint(0, (len(population) - 1)))
		if p > pcrossover:
			newpop.append(mother)
			newpop.append(father)
		else:
			cut = random.randint(0, (len(father) - 1))
			sonA = mother[:cut] + father[cut:]
			sonB = father[:cut] + mother[cut:]
			newpop.append(sonA)
			newpop.append(sonB)
	while len(population) > 0:
		newpop.append(population.pop())

	return newpop

			
def mutation(population, pmutation):
	for i in range(len(population)):
		if random.random() < pmutation:
   			mutantitem = random.randint(0, len(population[i]) - 1)
   			split = list(population[i])
   			# split[mutantitem] = random.choice(string.printable[:-5])
   			split[mutantitem] = chr(ord(split[mutantitem]) + random.randint(-3, 3))
   			population[i] = ''.join(split)
   	return population




if __name__ == "__main__":
	pmutation = 0.01
	pcrossover = 0.6
	populationdim = 200
	target = 'The quick brown fox jumps over the lazy dog!'
	expfit = 1
	tokeep = 0.75
	

	todelete = int(populationdim * tokeep)

	print '\npmutation: %.3f \npcrossover: %.3f' % (pmutation, pcrossover)
	print '\nTarget: %s' % target
	print '\nPopulation Dimension: %d\n' % populationdim
	print 'Let\'s go...'
	sleep(2)

	population = create(populationdim, len(target))

	fitval = fitness(population[0], target)

	i = 0
	while True:
		i += 1
		population = roulette(population, target, populationdim, todelete)
		population = crossover(population, pcrossover)
		population = mutation(population, pmutation)
		population = roulette(population, target, populationdim, todelete)
		
		for p, chromosome in enumerate(population):
			fitval_c = fitness(chromosome, target)
			if fitval_c < fitval:
				fitval = fitval_c
				pos = p

			print "%8i %5i %s" % (i, fitval_c, chromosome)
		
		if fitval < expfit:
			break

	print '\nGeneration: %d' % i
	print 'Match -> Found: %s' % population[pos]


    

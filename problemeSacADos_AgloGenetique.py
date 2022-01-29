from random import randint, choices, choice
import time

N = 18
Max = N*50
Lprix = [randint(0, 100) for k in range(N)]
Lmasses = [int(randint(7, 14)/10*a) for a in Lprix]

prob = Max / sum(Lmasses)


class Genome:
    def __init__(self, val=None):
        self.value = [choices([0, 1], [1 - prob, prob])[0] for k in range(N)] if val is None else val

    def evaluate(self):
        if sum([m * val for m, val in zip(Lmasses, self.value)]) > Max:
            return 0
        else:
            return sum([p * val for p, val in zip(Lprix, self.value)])

    def mutate(self):
        i = randint(0, N - 1)
        self.value[i] = abs(self.value[i] - 1)


class Population:
    def __init__(self, n):
        self.value = [Genome() for k in range(n)]

    def mutate(self):
        for gen in self.value:
            gen.mutate()

    def nextgen(self):
        weights = [gen.evaluate() for gen in self.value]

        best = Genome(self.value[weights.index(max(weights))].value.copy())

        self.mutate()

        LNextGen = []
        for gen1 in self.value:
            i = randint(0, N - 1)
            gen2 = choices(self.value, weights)[0]
            LNextGen.append(Genome(choice((gen1.value[:i] + gen2.value[i:], gen2.value[:i] + gen1.value[i:]))))

        weights = [gen.evaluate() for gen in LNextGen]
        LNextGen[weights.index(min(weights))] = best
        self.value = LNextGen

    def best(self):
        evaluations = [gen.evaluate() for gen in self.value]
        return self.value[evaluations.index(max(evaluations))]

    def evolve(self, n):
        for k in range(n):
            self.netgen()

debut = time.time()
a = Population(20)
for k in range(100):
    a.nextgen()

print(f"opti : {a.best().evaluate()}\ntemps : {round(time.time()-debut, 6)}")

debut = time.time()
L = [Genome([int(car) for car in bin(k)[2:].zfill(N)]) for k in range(2**N)]
Lvaleur = [gen.evaluate() for gen in L]
print(f"pas opti :{max(Lvaleur)}\ntemps : {round(time.time()-debut, 6)}")
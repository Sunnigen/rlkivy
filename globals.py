import random, sys

SEED_NUMBER = random.randint(1, sys.maxsize)
random.seed(SEED_NUMBER)
print(f"Seed Number: {SEED_NUMBER}")
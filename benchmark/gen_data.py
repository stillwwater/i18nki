import sys
import string
import random


randstr = lambda smin, smax: ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(smin, smax)))
duplicate = lambda: '_("%s")' % key_cache
arg = lambda: ('_("%s",' % randstr(8, 32)) + ','.join(randstr(2, 8) for _ in range(random.randint(1, 8))) + ')'
normal = lambda: '_("%s")' % randstr(8, 32)


key_cache = randstr(8, 32)


CHOICES = [(duplicate, 0.2), (arg, 0.33333), (normal, 1)]


def getln():
    global key_cache
    rand = random.random()

    for c in CHOICES:
        func, chance = c

        if rand <= chance:
            ans = func()

            if func == duplicate and random.random() < 0.5:
                key_cache = randstr(8, 32)

            return ans


lines = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
out = open('tmp/tmp', 'w')

for i in range(lines):
    out.write(getln() + '\n')

out.close()

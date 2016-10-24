import sys

def generate(counts, word, n):
  global comma
  if (len(word) == n):
    if comma:
      sys.stdout.write(',')
    sys.stdout.write(word)
    comma = True
    return
  for c in range(256):
    if counts[c] > 0:
      counts[c] -= 1
      generate(counts, word + chr(c), n)
      counts[c] += 1

with open(sys.argv[1], 'r') as test_cases:
  for test in test_cases:
    counts = {}
    for c in range(256):
      counts[c] = 0
    word = test.rstrip()
    for l in word:
      counts[ord(l)] += 1
    comma = False
    generate(counts, '', len(word))
    sys.stdout.write('\n')
    sys.stdout.flush()

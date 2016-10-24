def Guess(a, b, c, a1, b1):
    print 'a1 = ',a1,' b1 = ',b1
    if a1 > a:
        return (a1, b1)
    if b1 < c:
        return (a1, b1 + 1)
    else:
        return (a1 + 1, -c)

def Check(a1, b1, a2, b2):
    PrintSol(a1, b1, a2, b2)
    if a1 * b2 + a2 * b1 == b:
        print 'Found solution!'
        return True
    else:
        print a1 * b2 + a2 * b1,' != ', b
        return False

def PrintSol(a1, b1, a2, b2):
    print '(',a1,'x + ',b1,')(',a2,'x + ',b2,')'

# main

a = input('a = ')
b = input('b = ')
c = input('c = ')
print a,'x^2 + ',b,'x + ',c

found = False
for a1 in range(-abs(a), abs(a)):
    if a1 == 0:
        a1 = 1
    a2 = int(a/a1)
    if a1 * a2 != a:
        continue
    for b1 in range(-abs(c), abs(c)):
        if b1 == 0:
            b1 = 1
        if found:
            break
        b2 = int(c/b1)
        if b1 * b2 != c:
            continue
        if Check(a1, b1, a2, b2):
            found = True
            break

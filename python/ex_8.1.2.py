X = set((0, 2, 3, 4, 7))
Y = set((0, 2, 3, 5))
#Y = set((0, 3, 5))
Z = set((0, 4, 5, 6))

le = lambda A : sorted(A)[0]

def pt(l, v) :
    print(l + " = " + str(v))

pt("X", X)
pt("Y", Y)
pt("Z", Z)
    
x = le(X ^ Y)
y = le(Y ^ Z)
pt("x", x)
pt("y", y)

if x not in X or y not in Y :
    print("BAD SETS!")

pt("X - Z", X - Z)
pt("X ^ Z", X ^ Z)

a = le(X ^ Z)
pt("a", a)

if a not in (x, y) :
    print("Weird case!")

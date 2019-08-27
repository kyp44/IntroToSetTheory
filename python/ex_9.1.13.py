import sys
import argparse
import itertools as it

# Parse command line arguments
parser = argparse.ArgumentParser(description="Form injection as in Exercise 9.1.13 for sets of given size.")
parser.add_argument("kappas", metavar="KAPPA", nargs="+", type=int, help="Set sizes for each i in I")
args = parser.parse_args()

I = tuple(range(len(args.kappas)))
Ais = [tuple(range(k)) for k in args.kappas]

i0 = 1

def ai(ix, x, i) :
    (alix, beix) = (Ais[ix][0], Ais[ix][1])
    (ali, bei) = (Ais[i][0], Ais[i][1])

    if i == ix :
        return x
    else :
        if i == i0 :
            return ali if x == alix else bei
        else :
            return bei if x == alix else ali

ys = []
for ix in I :
    for x in Ais[ix] :
        y = tuple([ai(ix, x, i) for i in I])
        ys.append(y)

        print("f(" + ", ".join(map(str, (ix,x))) + ") = " + str(y))

print("Injective:", len(ys) == len(set(ys)))

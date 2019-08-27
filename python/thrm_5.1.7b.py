# Visualization of K^(L*M) and (K^L)^M so as to formulate a bijection
import itertools as it

K = set((0,1))
L = set((0,1,2))
M = set((0,1))

# Column width
cw = 15
def pcol(ls) :
    print("".join([str(e).ljust(cw) for e in ls]))

print("f in K^(L*M)")
pcol(["f" + str(p) for p in it.product(L, M)])
for vs in it.product(*[K for p in it.product(L, M)]) :
    pcol(vs)

print("")
print("g in (K^L)^M")
pcol(["g(" + str(v) +")" for v in M])
# Members of K^L as a sequence
KL = [s for s in it.product(*[K for l in L])]
for vs in it.product(*[KL for m in M]) :
    pcol(vs)

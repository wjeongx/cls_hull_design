#base cog
bcg = [0.291, -0.0421]
tcg = [-3.8087, -7.9808]

dcg = [tcg[0]-bcg[0],tcg[1]-bcg[1]]

Weight = 100000

momentX = dcg[0]*Weight / 30.
momentY = dcg[1]*Weight / 40.

load[]*2

load[] = 30*load[



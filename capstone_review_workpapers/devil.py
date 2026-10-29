# Devil's-case model. All inputs ESTIMATE unless noted. $M.
Y = [1, 2, 3]
# --- MAPPER
wins = {0: 0.0, 1: 3.0, 2: 7.0, 3: 11.0}  # MAP assessment wins (revenue-model base ~6/13/21)
P_ass = 0.19; P_impl = 0.28; conv_impl = 0.35
fed_share = 0.6; conv_sub = 0.20; ren_map = 0.75; P_sub_fed = 0.25; P_sub_nf = 0.15
r = {}
for y in Y:
    r.setdefault('MAP_assess', {})[y] = wins[y] * P_ass
    r.setdefault('MAP_impl', {})[y] = conv_impl * (0.5 * wins[y] + 0.5 * wins[y - 1]) * P_impl
nf_active = 0; nf_rev = {}
nf_new = {1: 0, 2: conv_sub * wins[1] * (1 - fed_share), 3: conv_sub * wins[2] * (1 - fed_share)}
for y in Y:
    nf_rev[y] = (nf_active * ren_map + 0.5 * nf_new[y]) * P_sub_nf
    nf_active = nf_active * ren_map + nf_new[y]
fed_pool = conv_sub * fed_share * (wins[1] + wins[2])  # federal buyers wait for authorization; start FY3 M6
fed_rev = {1: 0, 2: 0, 3: fed_pool * 0.25 * P_sub_fed}
for y in Y:
    r.setdefault('MAP_sub', {})[y] = nf_rev[y] + fed_rev[y]
arr_map = nf_active * P_sub_nf + fed_pool * P_sub_fed
# --- HARNESS
attach = 0.15; stand = {1: 0.5, 2: 2.0, 3: 3.0}; P_har = 0.15; P_himpl = 0.15; impl_h = 0.25
conv_h = 0.30; ren_h = 0.50; P_hsub = 0.15
hw = {0: 0}
for y in Y:
    hw[y] = attach * (0.5 * wins[y] + 0.5 * wins[y - 1]) + stand[y]
act = 0; hs = {}
for y in Y:
    new = conv_h * hw[y - 1]
    hs[y] = (act * ren_h + 0.5 * new) * P_hsub
    act = act * ren_h + new
for y in Y:
    r.setdefault('HAR_assess', {})[y] = hw[y] * P_har
    r.setdefault('HAR_impl', {})[y] = impl_h * hw[y] * P_himpl
    r.setdefault('HAR_sub', {})[y] = hs[y]
arr_har = act * P_hsub
# --- DG custom packs only
packs = {1: 0, 2: 2, 3: 3}
for y in Y:
    r.setdefault('DG_pack', {})[y] = packs[y] * 0.075
gross = {y: sum(r[k][y] for k in r) for y in Y}
assess = {y: r['MAP_assess'][y] + r['HAR_assess'][y] for y in Y}
netout = 0.5
incr = {y: gross[y] - netout * assess[y] for y in Y}
# --- cannibalization of the existing advisory book
book = 30.0; tm_share = 0.5; hour_cut = 0.375; adopt = {1: 0.10, 2: 0.25, 3: 0.40}
cann = {y: book * tm_share * hour_cut * adopt[y] for y in Y}
cann50 = {y: 0.5 * cann[y] for y in Y}
net = {y: incr[y] - cann[y] for y in Y}
net50 = {y: incr[y] - cann50[y] for y in Y}
cm_loss = {y: -cann[y] * 0.30 for y in Y}
fp_gain = {y: book * (1 - tm_share) * adopt[y] * 0.70 * hour_cut for y in Y}
# --- program cash
I_spons = 0.42; I_hard = 5.2
F = {1: 0.5 * 2.45, 2: 2.45, 3: 2.45}
sub_keys = ['MAP_sub', 'HAR_sub']
subs = {y: sum(r[k][y] for k in sub_keys) for y in Y}
svc_incr = {y: incr[y] - subs[y] for y in Y}
cm = {y: 0.35 * svc_incr[y] + 0.45 * subs[y] for y in Y}
cac = {y: (wins[y] + hw[y]) * (1 - netout) * 0.10 for y in Y}
prog = {y: cm[y] - F[y] - cac[y] for y in Y}
cum = -(I_spons + I_hard); cums = {}
for y in Y:
    cum += prog[y]; cums[y] = cum


def p(name, d):
    print(f"{name:30s}" + " ".join(f"{d[y]:7.2f}" for y in Y) + f"  | {sum(d.values()):7.2f}")


print(f"{'line':30s}    FY1     FY2     FY3  |   3-yr")
for k in r:
    p(k, r[k])
p('GROSS core', gross); p('assessments', assess); p('INCREMENTAL (-50% assess)', incr)
p('cannibalized T&M rev', cann); p('NET rev (no redeploy)', net); p('NET rev (50% redeploy)', net50)
p('profit: lost T&M CM', cm_loss); p('profit: fixed-price gain', fp_gain)
p('program CM', cm); p('run cost F', F); p('CAC', cac); p('program contribution', prog)
print('cum cash incl I', {y: round(cums[y], 2) for y in Y})
print('exit ARR MAP', round(arr_map, 2), 'HAR', round(arr_har, 2), 'total', round(arr_map + arr_har, 2))
print('HAR wins', {y: round(hw[y], 2) for y in Y})
g = gross[3]; c = cums[3]; cmr = cm[3] / gross[3]; cacr = cac[3] / gross[3]
for y in [4, 5]:
    g *= 1.35; pc = g * cmr - 2.45 - g * cacr; c += pc
    print(f'FY{y} gross {g:.2f} contrib {pc:.2f} cum {c:.2f}')
# breakeven gross revenue per year to cover F at FY3 ratios
print('breakeven gross/yr', round(2.45 / (cmr - cacr), 2))

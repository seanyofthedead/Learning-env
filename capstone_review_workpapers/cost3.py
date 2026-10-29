# Reconciled cost/margin/payback on revenue_modeler rev2.py. Units $K. FY0 = pre-program (capstone year).
import sys, copy
sys.path.insert(0, "/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/model")
import rev2
SEG = rev2.SEG
FTEM, FTEY = 24.0, 288.0
SPONS = 139.5

# ---- delivery cost as % of revenue (gross basis) ----
DEL_SERV = dict(map_assess=0.45, har_assess=0.45, map_impl=0.65, har_impl=0.65, dg_pack=0.58,
                county_pkg=0.20, county_upd=0.20, dg_royalty=0.05, ip=0.64)
DEL_SUB = {"A": dict(map_sub=0.54, har_sub=0.59, har_portfolio=0.59),
           "B": dict(map_sub=0.30, har_sub=0.35, har_portfolio=0.35)}
CF_ASSESS_GM = 0.28           # counterfactual (no-tool) assessment margin for non-incremental share
PULL_CM = 0.30
PURSUIT = dict(FC=35, FH=20, DoD=50, SL=25, UK=25)   # $K per mapper opportunity (ESTIMATE)
HAR_PURSUIT_MULT = {"A": 0.7, "B": 0.35}             # standalone harness pursuit vs mapper pursuit; B bundles
HAR_ATTACH_CAC = 15; DG_PACK_CAC = 5
COUNTY_PARTNER = 0.25; COUNTY_PRESALES = 10
PRODUCT = dict(map_assess="GOV", map_impl="GOV", map_sub="GOV", county_pkg="GOV", county_upd="GOV",
               har_assess="RTH", har_impl="RTH", har_sub="RTH", har_portfolio="RTH",
               dg_pack="SDG", dg_royalty="SDG", ip="IPA")

def seg_run(P, segs, **over):
    Q = copy.deepcopy(P)
    for s in SEG:
        if s not in segs:
            Q["opps_map"][s] = [0]*4; Q["opps_har"][s] = [0]*4
    Q["county_deals"] = [0, 0, 0]; Q["dg_royalty"] = [0, 0, 0]; Q["portfolio_starts"] = {}
    Q["ip_pilots"] = [0, 0, 0]; Q["ip_prod"] = [0, 0, 0]
    Q.update(over)
    return rev2.run(Q)

def sales_cost(P, cfg):
    sc = {"GOV": [0]*3, "RTH": [0]*3, "SDG": [0]*3, "GOV_nonincr_pursuit": [0]*3}
    for s in SEG:
        _, _, C, _ = seg_run(P, [s])
        _, _, C0, _ = seg_run(P, [s], har_attach=0)
        for i in range(3):
            mp = C["map_wins"][i] / P["win"][s] * PURSUIT[s]
            sa = C0["har_wins"][i]; att = C["har_wins"][i] - sa
            hp = sa / P["win"][s] * PURSUIT[s] * HAR_PURSUIT_MULT[cfg] + att * HAR_ATTACH_CAC
            sc["GOV"][i] += mp; sc["RTH"][i] += hp
            sc["SDG"][i] += C["dg_packs"][i] * DG_PACK_CAC
            sc["GOV_nonincr_pursuit"][i] += P["nonincr"] * (mp + sa / P["win"][s] * PURSUIT[s] * HAR_PURSUIT_MULT[cfg])
    for i in range(3):   # county channel (R11 ruling)
        sc["GOV"][i] += COUNTY_PRESALES * P["county_deals"][i]
    return sc

def fed_saas_commits(P):
    # federal SaaS-candidate buyers committed per FY (proxy: all fed new subs at managed-start timing x saas share)
    _, _, C, _ = seg_run(P, ["FC", "FH"], fed_saas_share=0.0)
    return [x * P["fed_saas_share"] for x in C["map_newsubs"]]

def fixed_and_upfront(case, cfg, P, include_ipa):
    auth = P["fed_auth_month"]
    up = {k: [0]*4 for k in ["SDG", "GOV", "RTH", "IPA"]}   # FY0..FY3
    F = {k: [0]*3 for k in ["SDG", "GOV", "RTH", "IPA", "PROG"]}
    note = ""
    if cfg == "A":
        up["SDG"][0] += SPONS; up["SDG"][1] += 466
        up["GOV"][0] += SPONS; up["GOV"][1] += 1159; up["GOV"][2] += 474
        up["RTH"][0] += SPONS; up["RTH"][1] += 951; up["RTH"][2] += 160
        if include_ipa: up["IPA"][0] += SPONS; up["IPA"][1] += 615
        base = dict(SDG=240, GOV=672, RTH=636, IPA=324)
        for k in base:
            if k == "IPA" and not include_ipa: continue
            F[k] = [0.5*base[k], base[k], base[k]]
        # ConMon from authorization month (448/yr split 60/40)
        for i in range(3):
            months = max(0, min(12, (i+1)*12 - auth)) if auth < 999 else 0
            F["GOV"][i] += 268.8 * months/12; F["RTH"][i] += 179.2 * months/12
    else:
        up["SDG"][0] += SPONS; up["SDG"][1] += 156
        up["GOV"][0] += SPONS; up["GOV"][1] += 840 + 25 + 96 + 20
        up["RTH"][0] += SPONS; up["RTH"][1] += 720 + 15
        F["SDG"] = [42, 84, 84]
        gov = 0.75*FTEY + 0.5*FTEY + 0.5*FTEY + 60          # corpus, PM, SRE(shared 0.75 split .5/.25), host
        rth = 0.5*FTEY + 60 + 0.25*FTEY + 0.25*FTEY + 30     # 0.5 FTE curation + $60k licensed attack libs, PM, SRE, host
        F["GOV"] = [0.5*gov, gov, gov]; F["RTH"] = [0.5*rth, rth, rth]
        # FedRAMP gate: trigger in FY after cumulative fed SaaS commits >= 5; ATO spend that FY, ConMon from next FY
        commits = fed_saas_commits(P); cum = 0; trig = None
        for i in range(3):
            cum += commits[i]
            if cum >= 5 and trig is None: trig = i + 1   # spend in following FY index (0-based FY idx = i+1)
        agency_clients = []
        if trig is not None and trig <= 2:
            up["GOV"][trig + 1] += 702
            for j in range(trig + 1, 3): F["GOV"][j] += 268.8; F["RTH"][j] += 179.2
            note = f"FedRAMP triggered: spend FY{trig+1}, ConMon from FY{trig+2}"
        else:
            note = "FedRAMP not triggered in window"
        # agency-cloud ATO support ($150k one-time) for federal SaaS-candidate buyers served pre-FedRAMP
        for i in range(3):
            if trig is None or i <= trig:
                F["GOV"][i] += 150 * commits[i]
        note += f"; fed SaaS commits/yr={[round(c,1) for c in commits]}"
    F["PROG"] = [150, 150, 150]
    return up, F, note

def run_case(case, cfg, include_ipa=False):
    P = {"base": rev2.BASE, "down": rev2.DOWN, "up": rev2.UP}[case]
    T, R, C, X = rev2.run(P)
    lines = [k for k in rev2.KEYS if k != "ip" or include_ipa]
    dsub = DEL_SUB[cfg]
    out = {}
    sc = sales_cost(P, cfg)
    up, F, note = fixed_and_upfront(case, cfg, P, include_ipa)
    prods = ["GOV", "RTH", "SDG"] + (["IPA"] if include_ipa else [])
    for p in prods:
        out[p] = dict(rev=[0]*3, gp=[0]*3, incr_adj=[0]*3, pull_gp=[0]*3, pull_inc=[0]*3)
    for k in lines:
        p = PRODUCT[k]
        d = dsub.get(k, DEL_SERV.get(k))
        for i in range(3):
            r = T[k][i]
            out[p]["rev"][i] += r
            g = r * (1 - d)
            if k in ("county_pkg", "county_upd"): g -= COUNTY_PARTNER * r
            out[p]["gp"][i] += g
            if k in ("map_assess", "har_assess"):
                out[p]["incr_adj"][i] -= P["nonincr"] * r * CF_ASSESS_GM   # counterfactual margin removed
    # pull-through by product
    for i in range(3):
        for p, (a, im) in {"GOV": ("map_assess", "map_impl"), "RTH": ("har_assess", "har_impl")}.items():
            out[p]["pull_gp"][i] = PULL_CM * P["pull_ratio"] * (T[a][i] + T[im][i])
            out[p]["pull_inc"][i] = PULL_CM * P["pull_ratio"] * ((1-P["nonincr"]) * T[a][i] + T[im][i])
    res = {}
    for p in prods:
        o = out[p]; s = sc.get(p, [0]*3)
        cm = [o["gp"][i] - F[p][i] - s[i] for i in range(3)]
        addback = sc["GOV_nonincr_pursuit"] if p == "GOV" else [0]*3   # non-incr pursuit would have happened anyway
        icm = [cm[i] + o["incr_adj"][i] + addback[i] for i in range(3)]
        icm_p = [icm[i] + o["pull_inc"][i] for i in range(3)]
        cash = -sum(up[p]) + sum(icm); cash_p = -sum(up[p]) + sum(icm_p)
        res[p] = dict(rev=sum(o["rev"]), gm=sum(o["gp"])/sum(o["rev"]) if sum(o["rev"]) else 0,
                      cm=sum(cm), cm_pct=sum(cm)/sum(o["rev"]) if sum(o["rev"]) else 0,
                      up=sum(up[p]), F=sum(F[p]), sales=sum(s), icm=icm, icm_p=icm_p,
                      cash=cash, cash_p=cash_p, upv=up[p])
    # program
    tot = lambda key: sum(res[p][key] for p in prods)
    prog_icm = [sum(res[p]["icm"][i] for p in prods) - F["PROG"][i] for i in range(3)]
    prog_icm_p = [sum(res[p]["icm_p"][i] for p in prods) - F["PROG"][i] for i in range(3)]
    upv = [sum(up[p][i] for p in prods) for i in range(4)]
    def payback(upv, icm):
        cum = -upv[0]; pb = None
        for i in range(3):
            cum += icm[i] - upv[i+1]
            if cum >= 0 and pb is None: pb = f"FY{i+1}"
        if pb: return pb, cum
        last = icm[2]
        if last <= 0: return "never", cum
        yrs = 3 + (-cum)/last
        return (f"~FY{yrs:.1f}*" if yrs <= 10 else ">FY10*"), cum
    pb, cash = payback(upv, prog_icm); pbp, cashp = payback(upv, prog_icm_p)
    rev_g = tot("rev"); gp_g = sum(res[p]["gm"]*res[p]["rev"] for p in prods)
    cm_g = tot("cm") - sum(F["PROG"])
    for p in prods:
        res[p]["pb"] = payback(res[p]["upv"], res[p]["icm"])[0]
        res[p]["pbp"] = payback(res[p]["upv"], res[p]["icm_p"])[0]
    prog = dict(rev=rev_g, gm=gp_g/rev_g, cm=cm_g, cm_pct=cm_g/rev_g, up=sum(upv), icm=prog_icm,
                icm_p=prog_icm_p, cash=cash, cash_p=cashp, pb=pb, pbp=pbp,
                roi=(sum(prog_icm)-sum(upv))/sum(upv), roi_p=(sum(prog_icm_p)-sum(upv))/sum(upv), note=note)
    return res, prog

if __name__ == "__main__":
    for cfg in ["A", "B"]:
        for case in ["base", "down", "up"]:
            for ipa in ([False, True] if cfg == "A" and case in ("base", "up") else [False]):
                res, prog = run_case(case, cfg, ipa)
                print(f"\n=== CONFIG {cfg} | {case} | IPA={'incl' if ipa else 'excl'} | {prog['note']}")
                for p, r in res.items():
                    print(f" {p}: rev {r['rev']/1e3:.2f}M GM {r['gm']:.0%} CM(gross) {r['cm']/1e3:.2f}M ({r['cm_pct']:.0%}) "
                          f"upfront {r['up']/1e3:.2f}M fixed {r['F']/1e3:.2f}M sales {r['sales']/1e3:.2f}M | "
                          f"3yr cash incr {r['cash']/1e3:.2f}M / w-pull {r['cash_p']/1e3:.2f}M | pb {r['pb']} / {r['pbp']}")
                print(f"   upfront by FY0..FY3 {[round(sum(r['upv'][i] for r in res.values())/1e3,2) for i in range(4)]}")
                print(f" PROGRAM: rev {prog['rev']/1e3:.2f}M GM {prog['gm']:.0%} CM {prog['cm']/1e3:.2f}M ({prog['cm_pct']:.0%}) "
                      f"upfront {prog['up']/1e3:.2f}M | incrCM/yr {[round(x/1e3,2) for x in prog['icm']]} w-pull {[round(x/1e3,2) for x in prog['icm_p']]}")
                print(f"   3yr cash: {prog['cash']/1e3:.2f}M (no pull) / {prog['cash_p']/1e3:.2f}M (w/ pull) | payback {prog['pb']} / {prog['pbp']} | ROI {prog['roi']:.0%} / {prog['roi_p']:.0%}")

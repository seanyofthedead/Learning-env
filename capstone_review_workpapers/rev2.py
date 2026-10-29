# Reconciled monthly model (rulings R1-R12). Months 1..36 = FY1..FY3. Units $K.
import copy, json
SEG=["FC","FH","DoD","SL","UK"]
GROUP={"FC":"Federal civ+health","FH":"Federal civ+health","DoD":"Defense","SL":"State/local","UK":"UK"}
BASE=dict(
 opps_map={"FC":[4,10,18,24],"FH":[4,8,13,15],"DoD":[0,3,6,8],"SL":[2,6,10,12],"UK":[2,5,10,13]},  # SL = states only (R11)
 win={"FC":0.30,"FH":0.40,"DoD":0.20,"SL":0.25,"UK":0.25},            # SL -5pts (R12)
 cycle={"FC":9,"FH":6,"DoD":15,"SL":9,"UK":6},
 opps_har={"FC":[0,2,4,6],"FH":[0,1,3,4],"DoD":[0,4,8,10],"SL":[0,1,3,5],"UK":[0,2,3,4]},
 integ_share={"FC":0.40,"FH":0.70,"DoD":0.20,"SL":0.50,"UK":0.30},   # share of accounts where GH is AI integrator (ESTIMATE)
 coi_removal=0.40,                                                  # R3
 map_assess={"FC":250,"FH":250,"DoD":250,"SL":150,"UK":180},
 map_impl={"FC":400,"FH":400,"DoD":400,"SL":200,"UK":250},
 map_sub={"FC":250,"FH":250,"DoD":250,"SL":150,"UK":200},           # R8
 har_assess={"FC":175,"FH":175,"DoD":225,"SL":100,"UK":140},
 har_impl={"FC":200,"FH":200,"DoD":250,"SL":100,"UK":150},
 har_sub={"FC":200,"FH":200,"DoD":250,"SL":100,"UK":150},           # R9
 dg_pack=100, dg_attach=0.30, dg_royalty=[0,0,0],                   # R4
 price_mult=1.0, esc=0.03,
 map_conv_impl=0.50, map_conv_sub=0.70,                             # R1: 0.5*0.7 = 35%
 har_conv_impl=0.40, har_conv_sub=0.60, har_attach=0.35,
 churn_map=0.10, churn_har=0.40,                                    # R2
 assess_start=3, managed_start=9,                                   # R7
 fed_auth_month=18, fed_saas_lag=12, fed_saas_share=0.40,           # R1/R7: fed SaaS from month 30
 dod_sub_mult=0.5, impl_lag=3, impl_dur=3,
 county_deals=[0,4,10], county_price=40, county_upd_attach=0.5, county_upd=20,   # R11
 portfolio_starts={}, portfolio_price=900,                          # R9 upside only
 ip_pilots=[0,0,0], ip_prod=[0,0,0], ip_pilot_price=750, ip_prod_price=2000,     # R5
 nonincr=0.40, pull_ratio=0.5,                                      # R6
)
DOWN=copy.deepcopy(BASE); UP=copy.deepcopy(BASE)
for s in SEG:
    DOWN["opps_map"][s]=[x*0.6 for x in BASE["opps_map"][s]]; UP["opps_map"][s]=[x*1.3 for x in BASE["opps_map"][s]]
    DOWN["opps_har"][s]=[x*0.6 for x in BASE["opps_har"][s]]; UP["opps_har"][s]=[x*1.3 for x in BASE["opps_har"][s]]
    DOWN["win"][s]=round(BASE["win"][s]-0.05,2); UP["win"][s]=round(BASE["win"][s]+0.05,2)
    DOWN["cycle"][s]=BASE["cycle"][s]+3; UP["cycle"][s]=max(3,BASE["cycle"][s]-2)
DOWN.update(price_mult=0.8, map_conv_impl=0.40, map_conv_sub=0.60, har_conv_sub=0.45, har_attach=0.20, dg_attach=0.15,
  churn_map=0.20, churn_har=0.50, fed_auth_month=999, county_deals=[0,2,5], nonincr=0.50, pull_ratio=0.3, managed_start=12)
UP.update(price_mult=1.1, map_conv_impl=0.55, map_conv_sub=0.80, har_conv_sub=0.70, har_attach=0.50, dg_attach=0.45,
  churn_map=0.05, churn_har=0.25, fed_auth_month=14, county_deals=[2,8,16], dg_royalty=[100,300,600],
  portfolio_starts={20:1,28:1,32:1}, ip_pilots=[1,2,1], ip_prod=[0,1,1], nonincr=0.30, pull_ratio=0.7)

KEYS=["map_assess","map_impl","map_sub","har_assess","har_impl","har_sub","har_portfolio","dg_pack","dg_royalty","county_pkg","county_upd","ip"]

def run(P):
    pm=P["price_mult"]
    rev={g:{k:[0.0]*3 for k in KEYS} for g in ["Federal civ+health","Defense","State/local","UK","Program"]}
    cnt={"map_wins":[0]*3,"har_wins":[0]*3,"map_newsubs":[0]*3,"har_newsubs":[0]*3,"dg_packs":[0]*3}
    exit_rr=0.0
    def fy(m): return (m-1)//12
    def add(s,k,m,v):
        if 1<=m<=36: rev[GROUP[s] if s in GROUP else s][k][fy(m)]+=v
    for s in SEG:
        coi=1-P["coi_removal"]*P["integ_share"][s]
        # monthly wins: opps spread monthly in year y0 (FY0 = months -11..0), close at +cycle; assessments can't start before month 3
        def wins(opps, mult=1.0):
            w=[0.0]*37
            for y0 in range(4):
                for mm in range(12):
                    m_open=(y0-1)*12+mm+1
                    if m_open+P["cycle"][s]<=0: continue   # would have closed pre-FY1 as ordinary consulting: not program revenue
                    m_close=max(P["assess_start"], m_open+P["cycle"][s])
                    if 1<=m_close<=36: w[m_close]+=opps[y0]/12*P["win"][s]*mult
            return w
        mw=wins(P["opps_map"][s])
        hsa=wins(P["opps_har"][s],coi)
        hatt=[0.0]*37
        for m in range(1,37):
            m2=m+6   # harness attach ~6 months after mapper win
            if m2<=36: hatt[m2]+=mw[m]*P["har_attach"]*coi
        hw=[hsa[m]+hatt[m] for m in range(37)]
        mapsubs=[0.0]*37; harsubs=[0.0]*37
        for m in range(1,37):
            e=(1+P["esc"])**fy(m)
            add(s,"map_assess",m,mw[m]*P["map_assess"][s]*pm); cnt["map_wins"][fy(m)]+=mw[m]
            add(s,"har_assess",m,hw[m]*P["har_assess"][s]*pm); cnt["har_wins"][fy(m)]+=hw[m]
            dgp=P["dg_attach"]*(mw[m]+hsa[m]); add(s,"dg_pack",m,dgp*P["dg_pack"]*pm); cnt["dg_packs"][fy(m)]+=dgp
            mi=mw[m]*P["map_conv_impl"]; mi_m=m+P["impl_lag"]
            if mi_m<=36: add(s,"map_impl",mi_m,mi*P["map_impl"][s]*pm)
            ready=mi_m+P["impl_dur"]
            ns=mi*P["map_conv_sub"]*(P["dod_sub_mult"] if s=="DoD" else 1)
            if s in ("FC","FH"):
                a=max(ready,P["managed_start"]); b=max(ready,P["fed_auth_month"]+P["fed_saas_lag"])
                if a<=36: mapsubs[a]+=ns*(1-P["fed_saas_share"])
                if b<=36: mapsubs[b]+=ns*P["fed_saas_share"]
            else:
                a=max(ready,P["managed_start"])
                if a<=36: mapsubs[a]+=ns
            hi=hw[m]*P["har_conv_impl"]; hi_m=m+P["impl_lag"]
            if hi_m<=36: add(s,"har_impl",hi_m,hi*P["har_impl"][s]*pm)
            hs_m=max(m+P["impl_lag"],P["managed_start"])   # harness runs in agency env: not SaaS-gated
            if hs_m<=36: harsubs[hs_m]+=hw[m]*P["har_conv_sub"]
        for subs,key,churn,price in [(mapsubs,"map_sub",P["churn_map"],P["map_sub"][s]),(harsubs,"har_sub",P["churn_har"],P["har_sub"][s])]:
            act=0.0; mc=1-(1-churn)**(1/12)
            for m in range(1,37):
                act=act*(1-mc)+subs[m]
                cnt["map_newsubs" if key=="map_sub" else "har_newsubs"][fy(m)]+=subs[m]
                add(s,key,m,act*price/12*pm*(1+P["esc"])**fy(m))
            exit_rr+=act*price*pm*(1+P["esc"])**2
    # program-level lines (assigned to segment groups)
    for i in range(3):
        rev["State/local"]["county_pkg"][i]+=P["county_deals"][i]*P["county_price"]*pm
        prior=sum(P["county_deals"][:i]); rev["State/local"]["county_upd"][i]+=(prior+0.5*P["county_deals"][i])*P["county_upd_attach"]*P["county_upd"]*pm
        rev["Program"]["dg_royalty"][i]+=P["dg_royalty"][i]
        prev=sum(P["ip_prod"][:i])
        rev["Federal civ+health"]["ip"][i]+=P["ip_pilots"][i]*P["ip_pilot_price"]*pm+(prev+0.5*P["ip_prod"][i])*P["ip_prod_price"]*pm
    act_p=0
    for m in range(1,37):
        act_p+=P["portfolio_starts"].get(m,0)
        rev["Federal civ+health"]["har_portfolio"][fy(m)]+=act_p*P["portfolio_price"]/12*pm
    exit_rr+=act_p*P["portfolio_price"]*pm
    cdeals=sum(P["county_deals"]); exit_rr+=cdeals*P["county_upd_attach"]*P["county_upd"]*pm + P["dg_royalty"][2]
    tot={k:[sum(rev[g][k][i] for g in rev) for i in range(3)] for k in KEYS}
    return tot,rev,cnt,exit_rr

if __name__=="__main__":
    res={}
    for name,P in [("base",BASE),("down",DOWN),("up",UP)]:
        T,R,C,X=run(P)
        core_keys=[k for k in KEYS if k!="ip"]
        gross=[sum(T[k][i] for k in core_keys) for i in range(3)]
        nonin=[P["nonincr"]*(T["map_assess"][i]+T["har_assess"][i]) for i in range(3)]
        incr=[gross[i]-nonin[i] for i in range(3)]
        pull=[P["pull_ratio"]*(T["map_assess"][i]+T["map_impl"][i]+T["har_assess"][i]+T["har_impl"][i]) for i in range(3)]
        pull_inc=[P["pull_ratio"]*((1-P["nonincr"])*(T["map_assess"][i]+T["har_assess"][i])+T["map_impl"][i]+T["har_impl"][i]) for i in range(3)]
        rec=[sum(T[k][i] for k in ["map_sub","har_sub","har_portfolio","county_upd","dg_royalty"]) for i in range(3)]
        print("=====",name,"$M")
        for k in KEYS: print(f"{k:14s}"," ".join(f"{v/1000:6.2f}" for v in T[k]),f"| {sum(T[k])/1000:6.2f}")
        for lab,v in [("GROSS core",gross),("non-incr",nonin),("INCR core",incr),("recurring",rec),("IP",T["ip"]),("pull gross",pull),("pull incr",pull_inc)]:
            print(f"{lab:14s}"," ".join(f"{x/1000:6.2f}" for x in v),f"| {sum(v)/1000:6.2f}")
        print("exit recurring run-rate $M",round(X/1000,2))
        for g in ["Federal civ+health","Defense","State/local","UK","Program"]:
            v=[sum(R[g][k][i] for k in core_keys) for i in range(3)]
            print(f"  {g:20s}"," ".join(f"{x/1000:6.2f}" for x in v),f"| {sum(v)/1000:6.2f}")
        print("  counts",{k:[round(x,1) for x in v] for k,v in C.items()})

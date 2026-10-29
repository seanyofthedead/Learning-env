import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/cm")
import cost3
for cfg in ["A", "B"]:
    r, p = cost3.run_case("base", cfg)
    print(cfg, "base 3yr cash", round(p["cash"]/1e3, 2), "w/pull", round(p["cash_p"]/1e3, 2))
orig = dict(cost3.PURSUIT)
for k in cost3.PURSUIT: cost3.PURSUIT[k] = orig[k]*0.5
for cfg in ["A", "B"]:
    r, p = cost3.run_case("base", cfg)
    print(cfg, "pursuit x0.5: 3yr cash", round(p["cash"]/1e3, 2), "w/pull", round(p["cash_p"]/1e3, 2), p["pb"])
cost3.PURSUIT.update(orig)
# B with FedRAMP forced in FY3 (if 5 commits arrive earlier than modeled)
r, p = cost3.run_case("base", "B")
print("B base forced FedRAMP FY3 approx cash:", round((p["cash"] - 702 - 0)/1e3, 2), "(ConMon starts FY4)")
# Productized subs only (A otherwise) to isolate levers
cost3.DEL_SUB["A2"] = cost3.DEL_SUB["B"]
# delivery-margin sensitivity: assessment GM 45% instead of 55%
cost3.DEL_SERV["map_assess"] = 0.55; cost3.DEL_SERV["har_assess"] = 0.55
for cfg in ["A", "B"]:
    r, p = cost3.run_case("base", cfg)
    print(cfg, "assess GM 45%: 3yr cash", round(p["cash"]/1e3, 2), "w/pull", round(p["cash_p"]/1e3, 2), p["pb"])

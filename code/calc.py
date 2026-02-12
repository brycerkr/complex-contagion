import pandas as pd
import numpy as np

def calculate_ems(f, h, b):
    def compute_tau(df):
        rec = df.iloc[:, 1:]

        rec = rec.replace("N", np.nan).astype(float)

        tau = (1 / (rec + 1)).mean(axis=1, skipna=True)
        return tau
    
    fn = "results/" + f.replace(".csv", "") + "_" + h + "_recencies.csv"

    HD = pd.read_csv(fn)
    benchmark = pd.read_csv("results/" + f.replace(".csv", "") + "_" + b + "_recencies.csv")

    tau_HD = compute_tau(HD)
    tau_benchmark = compute_tau(benchmark)

    out = pd.DataFrame({
        "nodeID": benchmark.iloc[:, 0],
        "tau_HD": tau_HD,
        "tau_bench": tau_benchmark,
        "effective": tau_HD / tau_benchmark.replace(0, np.nan),
        "seed_node": (tau_HD==1).astype(int)
    })

    # optional: replace inf / NaN ratios
    # out["tau_A/tau_B"] = out["tau_A/tau_B"].fillna(0)

    # write to CSV
    out.to_csv("calcs/" + f.replace(".csv", "") + "_" + h + "_"+ b + "_em.csv", index=False)
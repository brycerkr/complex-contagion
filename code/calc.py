import pandas as pd
import numpy as np

# Can't use .mean, that will only average the existing results
# We need NaN to be treated as either 0 or infinite depending 

def calculate_ems(f, h, b, kl, ku, sr):
    def compute_tau(df : pd.DataFrame):
        rec = df.iloc[:, 1:]
        tau_vals = 1 / (rec + 1)
        tau_vals = tau_vals.fillna(0)
        return tau_vals.mean(axis=1)
    
    def compute_nu(df : pd.DataFrame):
        rec = df.iloc[:, 1:]
        nu_vals = rec.notna()
        return nu_vals.mean(axis=1)
    
    f = f.replace(".txt","")
    f = f.replace(".csv","")
    fn = f"results/{f}_{h}_{int(sr*100)}_seed_{int(kl*100)}_{int(ku*100)}_thres.csv"
    bfn = f"results/{f}_{b}_{int(sr*100)}_seed_{int(kl*100)}_{int(ku*100)}_thres.csv"

    heu = pd.read_csv(fn)
    benchmark = pd.read_csv(bfn)

    heu = heu.apply(pd.to_numeric, errors="coerce")
    benchmark = benchmark.apply(pd.to_numeric, errors="coerce")

    tau_heu: pd.Series[np.Any] = compute_tau(heu)
    tau_benchmark = compute_tau(benchmark)

    nu_heu = compute_nu(heu)
    nu_benchmark = compute_nu(benchmark)

    out = pd.DataFrame({
        "nodeID": benchmark.iloc[:, 0],
        "tau_heu": tau_heu,
        "tau_bench": tau_benchmark,
        "effective_tau": tau_heu / tau_benchmark.replace(0, np.nan),
        "nu_heu": nu_heu,
        "nu_benchmark": nu_benchmark,
        "effective_nu": nu_heu / nu_benchmark.replace(0, np.nan),
        "seed_node": (tau_heu==1).astype(int)
    })

    # write to CSV
    out.to_csv(f"calcs/{f}_{h}_{b}_{int(sr*100)}_seed_{int(kl*100)}_{int(ku*100)}_thres_calcs.csv")






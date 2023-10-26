from pandas import read_csv, DataFrame
from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta

def non_defective(df):
    return df[df["defect_status"] == 0]

def defective(df):
    return df[df["defect_status"] == 1]

def save_df(obj, name):
    out_df = DataFrame.from_dict(obj).T
    out_df.to_csv(f"output/{name}")

def run_test(df, name):

    mann_whitney = {}
    cliffs = {}

    for property in df.columns[2:14]:
        D = defective(df)[property]
        ND = non_defective(df)[property]

        # run Mann Whitney U test
        U1, p = mannwhitneyu(D, ND)
        mann_whitney[property] = {
            "p-value": p,
            "U1": U1
        }

        # run Cliff-delta tests
        d, res = cliffs_delta(D, ND)
        cliffs[property] = {
            "d": d,
            "res": res
        }

    save_df(mann_whitney, f"Mann_Whitney/{name}.csv")
    save_df(cliffs, f"Cliffs_Delta/{name}.csv")


def init():
    # read data
    mirantis_df = read_csv("input/IST_MIR.csv")
    mozilla_df = read_csv("input/IST_MOZ.csv")
    openstack_df = read_csv("input/IST_OST.csv")
    wikimedia_df = read_csv("input/IST_WIK.csv")

    # execute tests
    run_test(mirantis_df, "Mirantis")
    run_test(mozilla_df, "Mozilla")
    run_test(openstack_df, "Openstack")
    run_test(wikimedia_df, "Wikimedia")
    

if __name__ == "__main__":
    init()
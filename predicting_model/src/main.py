import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from typing import List, Dict

# file that computes RQ3 requisites, i.e. log transformation, PCA , and 5 original classifiers
# (CART, KNN, LR, NB, RF) on 4 datasets
# also computes the classification results for one extra classifier "Support Vector Machine" or "SVM"
# also computes the feature importance for RQ1
# inputs:
# expects to find the authors' dataset files as "MIR.csv", "MOZ.csv", "OST.csv", and "WIK.csv"
# ouputs:
# "{metric_name}_median.csv" for four metrics ('precision', 'recall', 'f1', 'roc_auc')
# that each contains median of 10-fold cross-validation results for the all datasets


def main() -> None:
    mirantis_df: pd.DataFrame = pd.read_csv("../data_in/IST_MIR.csv")
    mozilla_df: pd.DataFrame = pd.read_csv("../data_in/IST_MOZ.csv")
    openstack_df: pd.DataFrame = pd.read_csv("../data_in/IST_OST.csv")
    wikimedia_df: pd.DataFrame = pd.read_csv("../data_in/IST_WIK.csv")

    dataset: List[pd.DataFrame] = [mirantis_df, mozilla_df, openstack_df, wikimedia_df]
    columns: List[str] = [
        "org",
        "file_",
        "URL",
        "File",
        "Lines_of_code",
        "Require",
        "Ensure",
        "Include",
        "Attribute",
        "Hard_coded_string",
        "Comment",
        "Command",
        "File_mode",
        "SSH_KEY",
        "defect_status",
    ]

    pcas: List[int] = [6, 8, 7, 7]
    metrics: List[str] = ["precision", "recall", "f1", "roc_auc"]

    # To store explained variance ratios for each dataset
    explained_var_ratios: List[np.ndarray] = []

    for metric in metrics:
        results: Dict[str, Dict[str, float]] = {}
        for index, df in enumerate(dataset):
            org_dict: Dict[str, float] = {}
            y: pd.Series = df[columns[-1]]
            # log transformation
            df_log: pd.DataFrame = df[columns[2:14]].apply(lambda x: np.log(x + 1))
            # PCA transformation (dimensionality reduction)
            pca = PCA(n_components=pcas[index])
            df_pca: np.ndarray = pca.fit_transform(df_log)

            pca_for_variance = PCA(n_components="mle", svd_solver="full")
            pca_for_variance.fit(df_log)
            print(pca_for_variance.explained_variance_ratio_)
            explained_var_ratios.append(pca_for_variance.explained_variance_ratio_)
            # we then performed the variance cover anakysis manually as it was presented in our presentation
            for model_name, model in [
                ("CART", tree.DecisionTreeClassifier()),
                ("KNN", KNeighborsClassifier()),
                ("LR", LogisticRegression(solver="lbfgs")),
                ("NB", GaussianNB()),
                ("RF", RandomForestClassifier(random_state=0)),
            ]:
                scores: np.ndarray = cross_val_score(
                    model, df_pca, y, cv=10, scoring=metric
                )
                org_dict[model_name] = round(np.median(scores), 3)

            results[df.iloc[0]["org"]] = org_dict

        df_out: pd.DataFrame = pd.DataFrame.from_dict(results).T
        df_out.to_csv(f"../data_out/{metric}_results.csv")


if __name__ == "__main__":
    main()

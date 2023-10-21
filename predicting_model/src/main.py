from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.svm import SVC


def read_data(filenames):
    dfs = [pd.read_csv(filename) for filename in filenames]
    return dfs


def apply_log_and_pca(df, pca_components):
    y = df["defect_status"]
    df_log = df.iloc[:, 4:16].apply(lambda x: np.log(x + 1))
    pca = PCA(n_components=pca_components)
    df_pca = pca.fit_transform(df_log)
    return df_pca, y


def evaluate_model(model, X, y, metric):
    scores = cross_val_score(model, X, y, cv=10, scoring=metric)
    return round(np.median(scores), 3)


def evaluate_all_models(dfs, pca_components_list, metrics):
    metric_results = defaultdict(dict)

    for df, pca_components in zip(dfs, pca_components_list):
        org = df.iloc[0]["org"]
        print(f"Evaluating models for {org}...")
        X, y = apply_log_and_pca(df, pca_components)

        for metric in metrics:
            model_scores = {
                "CART": evaluate_model(tree.DecisionTreeClassifier(), X, y, metric),
                "KNN": evaluate_model(KNeighborsClassifier(), X, y, metric),
                "LR": evaluate_model(LogisticRegression(solver="lbfgs"), X, y, metric),
                "NB": evaluate_model(GaussianNB(), X, y, metric),
                "RF": evaluate_model(
                    RandomForestClassifier(random_state=0), X, y, metric
                ),
            }

            metric_results[metric][org] = model_scores

    for metric, data in metric_results.items():
        df_metric = pd.DataFrame.from_dict(data).T
        df_metric.to_csv(f"{metric}_median.csv")


if __name__ == "__main__":
    filenames = [
        "../data_in/IST_MIR.csv",
        "../data_in/IST_MOZ.csv",
        "../data_in/IST_OST.csv",
        "../data_in/IST_WIK.csv",
    ]
    dfs = read_data(filenames)
    pca_components_list = [6, 8, 7, 7]
    metrics = ["precision", "recall", "f1", "roc_auc"]
    evaluate_all_models(dfs, pca_components_list, metrics)

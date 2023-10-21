import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from typing import List, Dict


def get_n_components_for_95_variance(X_scaled: pd.DataFrame) -> int:
    """
    Determines the number of principal components needed to explain at least 95% of the total variance.

    Parameters:
        X_scaled (pd.DataFrame): The scaled feature matrix.

    Returns:
        int: The number of principal components needed to explain at least 95% of the variance.
    """
    pca = PCA()
    pca.fit_transform(X_scaled)
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    n_components = np.argmax(cumulative_variance >= 0.95) + 1
    return n_components


def calculate_statistical_learners(
    X: np.ndarray, y: pd.Series, metric: str
) -> Dict[str, float]:
    """
    Calculates the evaluation metric for various statistical models using 10-fold cross-validation.

    Parameters:
        X (np.ndarray): The feature matrix after PCA.
        y (pd.Series): The target variable.
        metric (str): The evaluation metric to use ("precision", "recall", "f1", "roc_auc").

    Returns:
        Dict[str, float]: A dictionary containing the median of the evaluation metric for each model.
    """
    org_dict = {}
    for model_name, model in [
        ("CART", tree.DecisionTreeClassifier()),
        ("KNN", KNeighborsClassifier()),
        ("LR", LogisticRegression(solver="lbfgs")),
        ("NB", GaussianNB()),
        ("RF", RandomForestClassifier(random_state=0)),
    ]:
        scores = cross_val_score(model, X, y, cv=10, scoring=metric)
        org_dict[model_name] = round(np.median(scores), 3)
    return org_dict


def perform_10x10_cross_val(X: np.ndarray, y: pd.Series, model, metric: str) -> float:
    """
    Performs 10x10 cross-validation for a given model and evaluation metric.

    Parameters:
        X (np.ndarray): The feature matrix after PCA.
        y (pd.Series): The target variable.
        model: The machine learning model to evaluate.
        metric (str): The evaluation metric to use ("precision", "recall", "f1", "roc_auc").

    Returns:
        float: The median of the evaluation metric across the 10x10 cross-validation folds.
    """
    unique_classes = np.unique(y)
    rkf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=0)

    scores = cross_val_score(model, X, y, cv=rkf, scoring=metric)

    return round(np.median(scores), 3)


def main() -> None:
    print("Step 1: Loading datasets...")
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

    print(
        "Step 2: Calculating required number of principal components for each dataset..."
    )
    pcas: List[int] = []
    for df in dataset:
        X = df[columns[2:-1]].apply(lambda x: np.log(x + 1))
        pcas.append(get_n_components_for_95_variance(X))
    print(f"Required PCs for each dataset: {pcas}")

    metrics: List[str] = ["precision", "recall", "f1", "roc_auc"]

    for metric in metrics:
        print(f"Step 3: Evaluating models based on {metric}...")
        results = {}
        for index, df in enumerate(dataset):
            print(f"Processing dataset {index + 1}...")
            y = df[columns[-1]]
            df_log = df[columns[2:14]].apply(lambda x: np.log(x + 1))

            print("Performing PCA transformation...")
            pca = PCA(n_components=pcas[index])
            df_pca = pca.fit_transform(df_log)

            print("Calculating statistical learners...")
            org_dict = calculate_statistical_learners(df_pca, y, metric)

            print("Performing 10x10 Cross Validation...")
            for model_name, model in [
                ("CART", tree.DecisionTreeClassifier()),
                ("KNN", KNeighborsClassifier()),
                ("LR", LogisticRegression(solver="lbfgs")),
                ("NB", GaussianNB()),
                ("RF", RandomForestClassifier(random_state=0)),
            ]:
                org_dict[model_name] = perform_10x10_cross_val(df_pca, y, model, metric)

            results[df.iloc[0]["org"]] = org_dict

        print("Saving results...")
        df_out = pd.DataFrame.from_dict(results).T
        df_out.to_csv(f"../data_out/{metric}_results.csv")

    print("Process completed successfully.")


if __name__ == "__main__":
    main()

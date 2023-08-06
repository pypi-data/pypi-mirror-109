"""
Модуль с полезными функциями
"""


from collections import defaultdict

import numpy as np
import pandas as pd
import scipy.stats as sts
from typing import List, Dict, Any, Union, Optional
from IPython.display import display
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from tqdm.auto import tqdm

from ..transform import WoeTransformer


def extract_sub_pmt_str(
    df: pd.DataFrame, pmtstr: str, pmtstr_enddt: str, retro_dt: str, depth: int = 12
) -> pd.Series:
    """Извлечение нужного количества символов из платежной строки в зависимости от ретро-даты

    Parameters
    ---------------
    df : pandas.DataFrame
            Таблица с данными
    pmtstr : str
            Название столбца, содержащего платежную строку
    pmtstr_enddt : str
            Название столбца, содержащего последнюю дату платежной строки
    retro_dt : str
            Название столбца, содержащего ретро-даты
    depth : int, default 12
            Количество месяцев, отсчитываемых от ретро-даты

    Returns
    ---------------
    res : pandas.Series
            Вектор с выделенными символами покаждому наблюдению

    """
    assert df[pmtstr_enddt].dtype == "datetime64[ns]"
    assert df[retro_dt].dtype == "datetime64[ns]"

    df_ = df[[pmtstr, pmtstr_enddt, retro_dt]].copy()

    # Очистка дат от времени
    df_[pmtstr_enddt] = df_[pmtstr_enddt].dt.normalize()
    df_[retro_dt] = df_[retro_dt].dt.normalize()

    # Разница в месяцах между ретро-датой и последней датой платежной строки для всех наблюдений
    a = np.floor((df_[retro_dt] - df_[pmtstr_enddt]).dt.days / 30.4375)

    # Создание вектора с целевой длиной подстроки
    df_.loc[depth - a > 0, "res"] = depth - a
    df_["res"] = df_["res"].fillna(0).astype(int)

    # Выделение подстроки
    res = df_.apply(lambda x: x[pmtstr][: x["res"]], axis=1)
    return res


def get_worst_status(x: str) -> float:
    """Функция для выбора наихудшего статуса из платежной строки
    можно применять в методе .apply

    Parameters
    ---------------
    x : str
        Платежная строка

    Returns
    -------
    float

    """
    new_x = list(x)
    new_x = [i for i in x if i != "X"]
    if new_x:
        return np.float(
            sorted(list(map(lambda x: "1.5" if x == "A" else new_x, new_x)))[-1]
        )
    else:
        return np.float(-1)


def check_feat_stats(df, feat, val_counts=False):
    """Расчет описательных статистик признака"""

    print("Кол-во наблюдений:", len(df))
    print("Кoл-во пустых значений:", df[feat].isna().sum())

    d = {
        "count": len(df),
        "count_na": df[feat].isna().sum(),
        "count_unq_values": df[feat].nunique(),
        "min": df[feat].min(),
        "mean": df[feat].mean(),
        "median": df[feat].median(),
        "max": df[feat].max(),
    }
    if val_counts:
        val_count = df[feat].value_counts()
        display(val_count.reset_index())

    return pd.DataFrame.from_dict(
        d,
        orient="index",
    )


def styler_float(df, format_="{:,.1%}"):
    """Выводит датафрейм, форматируя числовые значения

    Parameters
    ---------------
    df : pandas.DataFrame
            Датафрейм для отображения
    format_ : python format string

    """

    with pd.option_context("display.float_format", format_.format):
        display(df)


def split_train_test_valid(
    df: pd.DataFrame,
    target: str,
    test_size: float = 0.3,
    val_size: float = 0.3,
    verbose: bool = False,
    **kwargs: Dict[Any, Optional[Any]],
) -> List[Any]:
    """
    Разбиение выборки на обучающую, валидационную и тестовую c сохранением доли таргета
    kwargs - аргументы для train_test_split из scikit-learn
    Возвращает: X_train, X_val, X_test, y_train, y_val, y_test
    """
    #     kwargs.update({'stratify': df[target]})
    if kwargs.get("shuffle", True) is True:
        kwargs.update({"stratify": df[target]})
    # else:
    #     kwargs.update({"stratify": None})

    # Выделение тестовой выборки
    y_data = df[target]
    X_data, X_test, y_data, y_test = train_test_split(
        df.drop(target, axis=1), df[target], test_size=test_size, **kwargs
    )
    # Выделение обучающей и валидационной выборок
    if kwargs.get("shuffle", True) is True:
        kwargs.update({"stratify": y_data})

    X_train, X_val, y_train, y_val = train_test_split(
        X_data, y_data, test_size=val_size, **kwargs
    )
    if verbose:
        print("train:", y_train.count(), y_train.sum(), y_train.mean(), sep="\t")
        print("valid.:", y_val.count(), y_val.sum(), y_val.mean(), sep="\t")
        print("test:", y_test.count(), y_test.sum(), y_test.mean(), sep="\t")

    return [X_train, X_val, X_test, y_train, y_val, y_test]


def cramers_corr(x1, x2):
    """
    расчет V–коэффициент Крамера
    x1 - переменная 1
    x2 - переменная 2
    """
    confusion_matrix = pd.crosstab(x1, x2)  # матрица запутанности
    chi2 = sts.chi2_contingency(confusion_matrix, correction=False)[
        0
    ]  # критерий Хи2 Пирсона
    n = confusion_matrix.sum().sum()  # общая сумма частот в таблице сопряженности
    return np.sqrt(chi2 / (n * (min(confusion_matrix.shape) - 1)))


# %% ExecuteTime={"start_time": "2020-04-30T08:38:23.252031Z", "end_time": "2020-04-30T08:38:23.258048Z"}
def get_corr_matrices(data, method="pearson"):
    n = data.shape[1]
    cramers_mat = np.ones((n, n))
    print("Calculating Cramers correlations")
    row = 0
    pbar = tqdm(total=n)
    while row <= n:
        for i in range(n):
            if i > row:
                tmp_corr = cramers_corr(data.values[:, row], data.values[:, i])
                cramers_mat[row, i] = tmp_corr
                cramers_mat[i, row] = tmp_corr
        pbar.update(1)
        row += 1
    pbar.close()
    return data.corr(method=method), pd.DataFrame(
        cramers_mat, index=data.columns, columns=data.columns
    )


def select_feats_corr(
    data, corr_matrices=None, sens_lin=0.7, sens_cramer=0.4, method="pearson"
):
    if corr_matrices is None:
        corr_lin, corr_cramer = get_corr_matrices(data, method)
    else:
        corr_lin, corr_cramer = corr_matrices
    feat_list = [data.columns[0]]
    for x_i in data.columns:
        u = True
        for x_j in feat_list:
            if (
                abs(corr_lin.loc[x_i, x_j]) > sens_lin
                or corr_cramer.loc[x_i, x_j] > sens_cramer
            ):
                u = False
        if u:
            feat_list.append(x_i)

    return feat_list


def plot_hier_corr(corr_matrix):
    """
    Отрисовка дендрограммы иерархической кластеризации признаков
    по матрице корреляций

    TODO: добавить шкалу (или подписи) на тепловую карту
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    corr_linkage = hierarchy.ward(corr_matrix.values)
    dendro = hierarchy.dendrogram(
        corr_linkage, labels=corr_matrix.columns, ax=ax1, leaf_rotation=90
    )
    dendro_idx = np.arange(0, len(dendro["ivl"]))
    ax1.hlines(
        ax1.get_yticks(), xmin=0, xmax=ax1.get_xlim()[1], linestyles="dotted", alpha=0.3
    )

    ax2.imshow(corr_matrix.values[dendro["leaves"], :][:, dendro["leaves"]])
    ax2.set_xticks(dendro_idx)
    ax2.set_yticks(dendro_idx)
    ax2.set_xticklabels(dendro["ivl"], rotation="vertical")
    ax2.set_yticklabels(dendro["ivl"])
    fig.tight_layout()

    plt.show()


def select_features_hierarchy(df, thr, method="pearson"):
    """
    Отбор признаков по итогам иерархической кластеризации
    """
    corr_matrix = df.corr(method=method).values
    corr_linkage = hierarchy.ward(corr_matrix)
    cluster_ids = hierarchy.fcluster(corr_linkage, thr, criterion="distance")
    cluster_id_to_feature_ids = defaultdict(list)
    for idx, cluster_id in enumerate(cluster_ids):
        cluster_id_to_feature_ids[cluster_id].append(idx)
    selected_features = [v[0] for v in cluster_id_to_feature_ids.values()]

    return df.columns[selected_features]


def build_logistic_regression(
    X_train,
    y_train,
    feat_list,
    cv=5,
    use_woe=True,
    param_grid=None,
    woe_transformer=None,
    random_seed=42,
    return_best=True,
    **fit_params,
):
    np.random.seed(random_seed)
    model_grid = LogisticRegression(
        penalty="l2", max_iter=1000, class_weight=None, random_state=random_seed
    )
    if use_woe:
        if isinstance(woe_transformer, WoeTransformer):
            wt = woe_transformer
        else:
            wt = WoeTransformer()
        pipe = Pipeline([("woe", wt), ("logreg", model_grid)])
    else:
        pipe = model_grid

    if param_grid is None:
        param_grid = {
            "logreg__solver": ["lbfgs"],  # ['newton-cg', 'sag', 'saga', 'lbfgs'],
            "logreg__C": [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0],
        }
    # подбор параметров
    grid_search = GridSearchCV(pipe, param_grid=param_grid, scoring="roc_auc", cv=cv)
    grid_search.fit(X_train[feat_list], y_train, **fit_params)

    if return_best:
        return grid_search.best_estimator_
    else:
        return grid_search


def select_features_corr(
    df: pd.DataFrame,
    corr_matrices: tuple,
    pearson_sens: float = 0.8,
    cramer_sens: float = 0.8,
    verbose: bool = False,
) -> pd.DataFrame:
    cols = df["predictor"]
    if verbose:
        print("Got {} predictors".format(len(cols)))
    pearson_df, cramer_df = corr_matrices

    X3: list = []

    DF_predictors = pd.DataFrame({"predictor": cols})  # причина отсева предиктора
    L_reason = ["added"]

    df_ = df.set_index("predictor").copy()

    for x_i in tqdm(cols):  # цикл по отбираемым предикторам
        if len(X3) == 0:
            X3.append(x_i)  # Добавляется предиктор с максимальным Gini train
            continue

        condition = True  # проверка, что предиктор еще не отсеяли

        if df_.loc[x_i, "gini_train"] < 0.05:  # Gini
            condition = False
            if verbose:
                print(f"{x_i} - Gini")
            L_reason.append("Gini < 5%")

        if df_["IV"][x_i] < 0.05 and condition:  # IV
            condition = False
            if verbose:
                print(f"{x_i} - IV")
            L_reason.append("IV < 5%")

        if condition:
            for x_j in X3:  # цикл по отобранным предикторам
                if (
                    abs(pearson_df[x_i][x_j]) > pearson_sens and condition
                ):  # корреляция Пирсона
                    condition = False
                    if verbose:
                        print(f"{x_i} - корреляция Пирсона с {x_j}")
                    L_reason.append(f"abs(Pearson) > {pearson_sens*100:.0f}% ({x_j})")
                if (
                    cramer_df[x_i][x_j] > cramer_sens and condition
                ):  # корреляция Крамера
                    condition = False
                    if verbose:
                        print(f"{x_i} - корреляция Крамера с {x_j}")
                    L_reason.append(f"Cramer > {cramer_sens*100:.0f}% ({x_j})")

        if condition:
            X3.append(x_i)
            L_reason.append("added")

    DF_predictors["reason"] = L_reason
    if verbose:
        print(
            "Selected {} predictors".format(
                len(DF_predictors[DF_predictors["reason"] == "added"])
            )
        )

    return DF_predictors


def select_feats(
    X_train,
    y_train,
    gini_and_iv_stats,
    pearson_corr,
    cramer_corr,
    pearson_sens=0.8,
    cramer_sens=0.8,
    random_seed=42,
):
    np.random.seed(random_seed)
    print("Got {} predictors".format(len(X_train.columns)))
    gini_data = gini_and_iv_stats[["predictor", "gini_train", "gini_test"]]
    iv_ordered_feats = pd.Series(
        gini_and_iv_stats["IV"], index=gini_and_iv_stats["predictor"]
    )
    gini_iv_subset = gini_and_iv_stats[
        gini_and_iv_stats["predictor"].isin(X_train.columns)
    ]
    # Отбор фичей по корреляциям, Gini и IV
    corr_select_res = select_features_corr(
        gini_iv_subset,
        (pearson_corr, cramer_corr),
        pearson_sens=pearson_sens,
        cramer_sens=pearson_sens,
    )
    # Исключение предикторов с положительными коэффициентами
    feat_list = corr_select_res.loc[
        corr_select_res["reason"] == "added", "predictor"
    ].to_list()
    feat_list = positive_coef_drop(
        X_train[feat_list], y_train, gini_data, iv_ordered_feats, seed=random_seed
    )
    print("Selected {} predictors".format(len(feat_list)))

    return feat_list


def get_predictions(fitted_estimator, X):
    preds = fitted_estimator.predict_proba(X)[:, 1]

    return preds


def positive_coef_drop(
    X, y, gini_data, iv_ordered_feats, seed=42, verbose=False, enable_tqdm=False
):
    """
    Удаление фичей с положительными коэффициентами
    """

    np.random.seed(seed)
    predictors = list(X.columns)
    if enable_tqdm:
        predictors = tqdm(predictors)
    for _ in predictors:  # исключение предикторов с положительными коэфициентами
        # подбор параметров
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        model_grid = LogisticRegression(penalty="l2", max_iter=500, random_state=seed)
        param_grid_model = {
            "solver": ["lbfgs"],  # ['newton-cg', 'sag', 'saga', 'lbfgs'],
            "C": [0.01, 0.1, 0.5, 1.0, 2.0, 10.0],
        }
        grid_search = GridSearchCV(
            model_grid, param_grid_model, scoring="roc_auc", cv=skf
        )
        grid_search.fit(X[predictors], y)

        # анализ коэффициентов модели
        DF_model_inf = pd.DataFrame()
        DF_model_inf["predictor"] = predictors
        DF_model_inf["coef"] = grid_search.best_estimator_.coef_[0]
        # Используется внешний датафрейм с рассчитанными однофакторными Gini
        DF_model_inf = DF_model_inf.merge(
            gini_data[["predictor", "gini_train", "gini_test"]],
            how="left",
            on="predictor",
        ).rename(columns={"train": "gini_tr", "gini_t": "Gini_test"})
        # Используется внешний pd.Series с рассчитанными IV предикторов (и отсортированный по убыванию IV)
        DF_model_inf = DF_model_inf.merge(
            iv_ordered_feats, how="left", left_on="predictor", right_index=True
        )
        k_sum = (DF_model_inf["coef"] * DF_model_inf["IV"]).sum()

        DF_model_inf["coef_K"] = DF_model_inf["coef"] * DF_model_inf["IV"] / k_sum
        DF_model_inf_2 = (
            DF_model_inf.loc[DF_model_inf["coef"] >= 0]
            .sort_values("IV")
            .reset_index(drop=True)
        )
        positive_coef_count = DF_model_inf_2.shape[0]
        if positive_coef_count > 0:
            x_i = DF_model_inf_2["predictor"][0]
            predictors.remove(x_i)
            if verbose:
                print(positive_coef_count, x_i)
                # display(DF_model_inf_2)
        else:
            break

    return predictors

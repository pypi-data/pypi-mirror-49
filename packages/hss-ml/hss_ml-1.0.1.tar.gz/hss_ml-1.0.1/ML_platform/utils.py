import numpy as np
import re

def get_rank_data_from_df(df):
    """
    将df转换为xgboost rank的数据格式
    :param df:
    feature_data例子：[[0.8501470782711954 0.8413838513812395 0.1111111111111111 0.9988226124924564],
                    [0.8096037659992619 0.5227391531626076 0.6666666666666666 0.999407010779285],
                    [0.3709492441746188 0.48868571313684916 0.6666666666666666 0.9824130570606465]]
    lable：[1 0 1]
    group：[2 1] 表明第一组有2条数据，第二组有1条数据
    :return: feature_data, lable, group
    """
    orgdata = df.values
    last_q_id = ""
    current_q_id = ""
    dtrain = []
    dlable = []
    dgroup = []
    group_count = 0
    for i in range(len(orgdata)):
        if i == 0:
            last_q_id = orgdata[i, 1]
            current_q_id = last_q_id

        else:
            current_q_id = orgdata[i, 1]

        dtrain.append(orgdata[i, 2:])
        dlable.append(orgdata[i, 0])

        if current_q_id != last_q_id:
            last_q_id = current_q_id
            dgroup.append(group_count)
            group_count = 1

        else:
            group_count += 1
    dgroup.append(group_count)
    return np.array(dtrain), dlable, dgroup

def get_feature_data_from_df(df):
    """
    将df转换为feature, label的数据格式
    :param df:
    feature_data例子：[[0.8501470782711954 0.8413838513812395 0.1111111111111111 0.9988226124924564],
                    [0.8096037659992619 0.5227391531626076 0.6666666666666666 0.999407010779285],
                    [0.3709492441746188 0.48868571313684916 0.6666666666666666 0.9824130570606465]]
    lable：[1 0 1]
    :return: feature_data, lable
    """
    label = df["label"].values
    col = []
    for i in df.columns.values:
        if (i != "label") & (i != "group_id"):
            col.append(i)
    data = df[col].values

    return data, label

# 判断是int，float，string
def judgeNumberOrString(s):
    s = str(s)
    if s.isdigit():
        return int(s)

    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')  # 定义正则表达式
    result = value.match(s)
    if result:
        return float(s)

    return s
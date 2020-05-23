import os

import pandas as pd
import numpy as np
import warnings
from spcapi.model.spcSource import spcSource

warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
plt.rcParams['axes.unicode_minus'] = False   #解决负号不显示的问题
# plt.rcParams['font.SimHei'] = ['SimHei']  #显示中文


def create(df,device_no):
    df['timestamp'] = df['timestamp'].map(lambda x: str(datetime.datetime.fromtimestamp(x)))  # 将时间戳转换为datetime库的时间
    df['timestamp'] = df['timestamp'].map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))  # 将时间转换为strptime格式
    df['timestamp'] = df['timestamp'].map(lambda x: mdates.date2num(x))
    df['change_val_shift'] = df['change_val'].shift(1)
    df['R'] = df['change_val_shift'] - df['change_val']
    df['R'] = df['R'].map(lambda x: np.abs(x))
    df = df.drop('change_val_shift', axis=1)
    get_fig(df, device_no)

def judge_value(a):  # 判断df一行中的第3至最后一个值是否相同
    val = a[2]
    key = 1
    for l in range(3, len(a)):
        if a[l] != val:
            key = key * 0
    if key == 1:
        return True
    else:
        return False

def get_no(df_prob, p, no_columns_name):  # 根据问题点的index2筛选出问题点及后面p个点的prob_point
    prob_index = df_prob[df_prob.apply(judge_value, axis=1)].index
    prob_index_list = []
    for n in prob_index.to_list():
        for m in range(p):
            prob_index_list.append(n + m)
    dup_prob_index_list = list(set(prob_index_list))
    prob_nos = ",".join(
        [str(x) for x in df_prob.loc[dup_prob_index_list][no_columns_name]])  # 根据index2筛选出prob_point，并转换成字符串
    return prob_nos

def bigorsmall(b):  # 判断是否大于0,并返回1，-1和0
    if b > 0:
        return 1
    elif b < 0:
        return -1
    elif b == 0:
        return 0

def checkjiaocha(a):  # 检查df中每行第5至17个值是否交替上下
    val = a[4]
    v = 1
    for q in range(5, 18):
        if val != 0:
            if ((q % 2 == 1) & (val == -a[q])) or ((q % 2 == 0) & (val == a[q])):
                v = v + 1
    if v == 14:
        return True
    else:
        return False

def prob5_detect(df_prob5t, df_part, no_columns_name):  # 问题5检测
    df_prob5t["index2"] = df_prob5t.index
    df_prob5t["index_shift"] = df_prob5t["index2"].shift(1)
    df_prob5t["minus_value"] = df_prob5t["index_shift"] - df_prob5t["index2"]
    df_prob5t = df_prob5t.reset_index()
    df_prob5f = df_prob5t[df_prob5t['minus_value'] > -3]
    a_l = df_prob5f['index2'].to_list()
    b_l = df_prob5f["index_shift"].to_list()
    a_l.extend(b_l)
    c_l = df_part.loc[a_l][no_columns_name].to_list()
    return a_l

def prob6_detect(df_prob6_s, df_part, no_columns_name):
    df_prob6_s["index2"] = df_prob6_s.index
    df_prob6_s["index_shift"] = df_prob6_s["index2"].shift(-3)
    df_prob6_s["minus_value"] = df_prob6_s["index_shift"] - df_prob6_s["index2"]
    df_prob6_v = df_prob6_s[df_prob6_s["minus_value"] < 5]
    prob6_indexl = []
    for a in range(len(df_prob6_v)):
        prob6_indexl.extend(np.arange(df_prob6_v.iloc[a, 2], df_prob6_v.iloc[a, 3] + 1))
    prob6_indexl = list(set(prob6_indexl))
    prob6_indexl.sort()
    prob6_nos1 = df_part.loc[prob6_indexl][no_columns_name].to_list()
    return prob6_nos1

def prob_detection(df_part, column_name, no_columns_name, UCL, LCL):
    count = df_part.shape(0)
    df_prob = pd.DataFrame(columns=["prob_code", "prob_desc", "prob_points"])
    # 问题1判断 一个点落在a区之外
    df_prob1 = df_part[(df_part[column_name] < LCL) | (df_part[column_name] > UCL)]  # 筛选出异常点
    df_prob1_no = ','.join([str(x) for x in df_prob1[no_columns_name]])  # 提取异常点的prob_point
    if len(df_prob1) > 0:
        df_prob = df_prob.append(
            [{"prob_code": "01", "prob_desc": "The point falls outside of area A", "prob_points": df_prob1_no}],
            ignore_index=True)

    # 问题2判断 连续9点落在中心线同一侧
    if count>=9:
        df_prob2 = pd.DataFrame()
        df_prob2[no_columns_name] = df_part[no_columns_name]
        df_prob2[column_name] = df_part[column_name]
        df_prob2['shift_R_mp1'] = (df_part[column_name] > df_part[column_name].mean()).astype(int)  # 判断是否大于均值并返回0和1
        for i in range(2, 10):  # 移位建立新列
            shift_column_name = "shift_R_mp" + str(i)
            df_prob2[shift_column_name] = df_prob2['shift_R_mp1'].shift(-i + 1)
        prob2_nos = get_no(df_prob2, 9, no_columns_name)
        if len(prob2_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "02",
                                       "prob_desc": "9 consecutive points and above on one side of the center line",
                                       "prob_points": prob2_nos}], ignore_index=True)

    # 问题3判断  连续6点递增或递减（测试5点和6点）
    if count>=6:
        df_prob3 = pd.DataFrame()
        df_prob3[no_columns_name] = df_part[no_columns_name]
        df_prob3[column_name] = df_part[column_name]
        df_prob3["shift_R"] = df_prob3[column_name].shift(-1)
        df_prob3["minus_value"] = df_prob3["shift_R"] - df_prob3[column_name]  # 用后一个数减去前一个数
        df_prob3["minus_value1"] = df_prob3["minus_value"].map(bigorsmall)  # 将minus_value转为-1，0，1
        for i in range(2, 6):  # 移位建立新列
            minus_column_name = "minus_value" + str(i)
            df_prob3[minus_column_name] = df_prob3["minus_value1"].shift(-i + 1)
        prob3_nos = get_no(df_prob3.drop(['shift_R', 'minus_value'], axis=1), 6, no_columns_name)
        if len(prob3_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "03",
                                       "prob_desc": "It increases or decreases for six consecutive points",
                                       "prob_points": prob3_nos}], ignore_index=True)

    # 问题4判断  连续14个点交替上下
    if count>=14:
        df_prob4 = pd.DataFrame()
        df_prob4[no_columns_name] = df_part[no_columns_name]
        df_prob4[column_name] = df_part[column_name]
        df_prob4["shift_R"] = df_prob4[column_name].shift(-1)
        df_prob4["minus_value"] = df_prob4["shift_R"] - df_prob4[column_name]
        df_prob4["minus_value_mp"] = df_prob4["minus_value"].map(bigorsmall)
        for i in range(2, 15):  # 移位建立新列
            minus_column_name = "minus_value_mp" + str(i)
            df_prob4[minus_column_name] = df_prob4['minus_value_mp'].shift(-i + 1)
        prob4_index = df_prob4[df_prob4.apply(checkjiaocha, axis=1)].index
        prob4_index_list = []
        for n in prob4_index.to_list():
            for m in range(14):
                prob4_index_list.append(n + m)
        dup_prob4_index_list = list(set(prob4_index_list))
        prob4_nos = ",".join(
            [str(x) for x in df_part.loc[dup_prob4_index_list][no_columns_name]])  # 根据index2筛选出prob_point，并转换成字符串
        if len(prob4_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "04", "prob_desc": "14 points in a row alternating up and down",
                                       "prob_points": prob4_nos}], ignore_index=True)

    # 问题5判断 3点中有2点落在中心线同一侧的B区以外
    if count>=3:
        df_prob5 = pd.DataFrame()
        df_prob5[no_columns_name] = df_part[no_columns_name]
        df_prob5[column_name] = df_part[column_name]
        upper = UCL - (UCL - df_part[column_name].mean()) / 3
        lower = UCL - ((UCL - df_part[column_name].mean()) / 3) * 5
        df_prob5t = df_prob5[df_prob5[column_name] > upper]
        prob5_nos1 = prob5_detect(df_prob5t, df_part, no_columns_name)
        df_prob5b = df_prob5[df_prob5[column_name] < lower]
        prob5_nos2 = prob5_detect(df_prob5b, df_part, no_columns_name)
        prob5_nos1.extend(prob5_nos2)
        prob5_nos1 = list(set(prob5_nos1))
        prob5_nos1.sort()
        prob5_nos = ",".join([str(int(x)) for x in prob5_nos1])
        if len(prob5_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "05",
                                       "prob_desc": "Two in three points fall outside of zone B on the same side of average",
                                       "prob_points": prob5_nos}], ignore_index=True)

    # 问题6判断 连续5点中有4点落在中心线同一侧的C区以外
    if count>=5:
        upper6 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 2
        lower6 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 4
        df_prob6 = pd.DataFrame()
        df_prob6[no_columns_name] = df_part[no_columns_name]
        df_prob6[column_name] = df_part[column_name]
        df_prob6_u = df_prob6[df_prob6[column_name] > upper6]
        prob6_nos1 = prob6_detect(df_prob6_u, df_part, no_columns_name)
        df_prob6_l = df_prob6[df_prob6[column_name] < lower6]
        prob6_nos2 = prob6_detect(df_prob6_l, df_part, no_columns_name)
        prob6_nos1.extend(prob6_nos2)
        prob6_nos1 = list(set(prob6_nos1))
        prob6_nos1.sort()
        prob6_nos = ",".join([str(x) for x in prob6_nos1])
        if len(prob6_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "06",
                                       "prob_desc": "Four of the five points in a row fall outside zone C on the same side of the centerline",
                                       "prob_points": prob6_nos}], ignore_index=True)

    # 问题7判断 连续15点落在中心线两侧的C区内
    if count>=15:
        upper7 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 2
        lower7 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 4
        df_prob7 = pd.DataFrame()
        df_prob7[no_columns_name] = df_part[no_columns_name]
        df_prob7[column_name] = df_part[column_name]
        df_prob7_s = df_prob7[(df_prob7[column_name] < upper7) & (df_prob7[column_name] > lower7)]
        df_prob7_s['index2'] = df_prob7_s.index
        df_prob7_s["index_shift"] = df_prob7_s['index2'].shift(-15)
        df_prob7_s['minus_value'] = df_prob7_s["index_shift"] - df_prob7_s['index2']
        df_prob7_l = df_prob7_s[df_prob7_s['minus_value'] <= 15]
        prob7_indexl = []
        for c in range(len(df_prob7_l)):
            prob7_indexl.extend(np.arange(df_prob7_l.iloc[c, 2], df_prob7_l.iloc[c, 3] + 1))
        prob7_indexl = list(set(prob7_indexl))
        prob7_indexl.sort()
        prob7_nos = ",".join([str(x) for x in df_part.loc[prob7_indexl][no_columns_name]])
        if len(prob7_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "07",
                                       "prob_desc": "15 consecutive points fall in zone C on either side of the center line",
                                       "prob_points": prob7_nos}], ignore_index=True)

    # 问题8判断  连续8点落在中心线两侧，且无一在C区内
    if count>=8:
        upper8 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 2
        lower8 = UCL - ((UCL - df_part[column_name].mean()) / 3) * 4
        df_prob8 = pd.DataFrame()
        df_prob8[no_columns_name] = df_part[no_columns_name]
        df_prob8[column_name] = df_part[column_name]
        df_prob8_s = df_prob8[(df_prob8[column_name] > upper8) | (df_prob8[column_name] < lower8)]
        df_prob8_s['index2'] = df_prob8_s.index
        df_prob8_s["index_shift"] = df_prob8_s['index2'].shift(-8)
        df_prob8_s['minus_value'] = df_prob8_s["index_shift"] - df_prob8_s['index2']
        df_prob8_l = df_prob8_s[df_prob8_s['minus_value'] <= 8]
        prob8_indexl = []
        for c in range(len(df_prob8_l)):
            prob8_indexl.extend(np.arange(df_prob8_l.iloc[c, 2], df_prob8_l.iloc[c, 3] + 1))
        prob8_indexl = list(set(prob8_indexl))  # 去重
        prob8_indexl.sort()  # 排序
        prob8_nos = ",".join([str(x) for x in df_part.loc[prob8_indexl][no_columns_name]])
        if len(prob8_nos) > 0:
            df_prob = df_prob.append([{"prob_code": "08",
                                       "prob_desc": "8 consecutive points fall on both sides of the center line, and none of them are in zone C",
                                       "prob_points": prob8_nos}], ignore_index=True)
    return df_prob

def prob_columns(df, R_prob):  # 将问题类型添加到原表后面
    for k in range(1, 9):  # 先8个问题列设置为默认为“0”
        prob_columnname = "prob" + str(k)
        df[prob_columnname] = 0
    length = len(df)
    df_prob2 = pd.DataFrame(columns=["prob_point", "prob_code"])
    for index in range(len(R_prob)):
        for no in R_prob.iloc[index, 2].split(','):
            df_prob2 = df_prob2.append([{"prob_point": int(no), "prob_code": R_prob.loc[index, 'prob_code']}],
                                       ignore_index=True)
    df_prob2 = df_prob2.drop_duplicates()
    for k in range(1, 9):
        for l in range(length):
            number = df.iloc[l, 0]
            if number in df_prob2["prob_point"].to_list():
                prob_codes = df_prob2[df_prob2["prob_point"] == number]["prob_code"].to_list()
                if k in [int(x) for x in prob_codes]:
                    df.iloc[l, k - 9] = 1

def get_fig(df, device_no):
    df0 = df[df['device_no'] == device_no]
    size_type_list = df['size_type'].unique().tolist()
    num_size_type = len(size_type_list)
    plt.figure(figsize=(24, 12))
    d2 = 1.128  # 查表得
    E2 = 3 / d2
    D3 = 0.000  # 查表得
    D4 = 3.267  # 查表得

    for size_type in size_type_list:
        i = 1
        plt.clf()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 画移动极差的图
        df1 = df[df['size_type'] == size_type].reset_index()
        df2 = df[df['size_type'] == size_type].reset_index()
        x_max = max(df1['timestamp'])
        x_min = min(df1['timestamp'])

        R_ = df1['R'].mean()

        UCL = D4 * R_
        LCL = D3 * R_
        # UCL =
        sigma = (UCL - R_) / 3

        prob_demo = prob_detection(df1, "R", "index", UCL, LCL)
        prob_columns(df1, prob_demo)
        df1_prob1 = df1[df1['prob1'] == 1]
        df1_prob2 = df1[df1['prob2'] == 1]
        df1_prob3 = df1[df1['prob3'] == 1]
        df1_prob4 = df1[df1['prob4'] == 1]
        df1_prob5 = df1[df1['prob5'] == 1]
        df1_prob6 = df1[df1['prob6'] == 1]
        df1_prob7 = df1[df1['prob7'] == 1]
        df1_prob8 = df1[df1['prob8'] == 1]

        ax = plt.subplot(1, 2, i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M:%S'))
        ax.hlines(UCL, xmin=x_min, xmax=x_max, colors="r")
        ax.hlines(LCL, xmin=x_min, xmax=x_max, colors="r")
        ax.hlines(R_, xmin=x_min, xmax=x_max, colors="b")
        ax.hlines((UCL - sigma * 1), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.hlines((UCL - sigma * 2), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.hlines((UCL - sigma * 4), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.plot(df1['timestamp'], df1["R"], color="grey", label="移动极差")
        ax.scatter(df1_prob1['timestamp'], df1_prob1["R"], color="red", marker='x', alpha=0.9, label="问题一")
        ax.scatter(df1_prob2['timestamp'], df1_prob2["R"], color="blue", marker='o', alpha=0.9, label="问题二")
        ax.scatter(df1_prob3['timestamp'], df1_prob3["R"], color="yellow", marker='o', alpha=0.9, label="问题三")
        ax.scatter(df1_prob4['timestamp'], df1_prob4["R"], color="green", marker='o', alpha=0.9, label="问题四")
        ax.scatter(df1_prob5['timestamp'], df1_prob5["R"], color="black", marker='x', alpha=0.9, label="问题五")
        ax.scatter(df1_prob6['timestamp'], df1_prob6["R"], color="orange", marker='x', alpha=0.9, label="问题六")
        ax.scatter(df1_prob7['timestamp'], df1_prob7["R"], color="pink", marker='x', alpha=0.9, label="问题七")
        ax.scatter(df1_prob8['timestamp'], df1_prob8["R"], color="red", marker='o', alpha=0.9, label="问题八")
        plt.ylabel("移动极差R", fontsize=20)
        ax.text(x_max, UCL, "UCL", fontsize=15)
        ax.text(x_max, LCL, "LCL", fontsize=15)
        ax.text(x_max, R_, "中心线", fontsize=15)
        ax.text(x_min, UCL - sigma * 0.5, "A", fontsize=20)
        ax.text(x_min, UCL - sigma * 1.5, "B", fontsize=20)
        ax.text(x_min, UCL - sigma * 2.5, "C", fontsize=20)
        ax.text(x_min, UCL - sigma * 3.5, "C", fontsize=20)
        ax.text(x_min, UCL - sigma * 4.5, "B", fontsize=20)
        plt.legend()
        plt.xlim(x_min, x_max)
        plt.title("设备编号{device_no},尺寸类别{size_type},移动极差".format(device_no=device_no, size_type=size_type),
                  fontsize=20)
        i += 1

        # 以下画转换值的图

        x_max = max(df2['timestamp'])
        x_min = min(df2['timestamp'])

        R_ = df2['R'].mean()
        X_ = df2["change_val"].mean()
        UCLx = X_ + df2.iloc[-1, :]['control_up']
        LCLx = X_ - df2.iloc[-1, :]['control_down']
        sigmax = (UCLx - LCLx) / 6

        prob_demo = prob_detection(df2, "change_val", "index", UCLx, LCLx)
        prob_columns(df2, prob_demo)
        df1_prob1 = df2[df2['prob1'] == 1]
        df1_prob2 = df2[df2['prob2'] == 1]
        df1_prob3 = df2[df2['prob3'] == 1]
        df1_prob4 = df2[df2['prob4'] == 1]
        df1_prob5 = df2[df2['prob5'] == 1]
        df1_prob6 = df2[df2['prob6'] == 1]
        df1_prob7 = df2[df2['prob7'] == 1]
        df1_prob8 = df2[df2['prob8'] == 1]

        ax = plt.subplot(1, 2, i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M:%S'))
        ax.hlines(UCLx, xmin=x_min, xmax=x_max, colors="r")
        ax.hlines(LCLx, xmin=x_min, xmax=x_max, colors="r")
        ax.hlines(X_, xmin=x_min, xmax=x_max, colors="b")
        ax.hlines((UCLx - sigmax * 1), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.hlines((UCLx - sigmax * 2), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.hlines((UCLx - sigmax * 4), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.hlines((UCLx - sigmax * 5), xmin=x_min, xmax=x_max, linestyle="--", colors="y", alpha=0.5)
        ax.plot(df1['timestamp'], df1["change_val"], color="grey", label="转换值")
        ax.scatter(df1_prob1['timestamp'], df1_prob1["change_val"], color="red", marker='x', alpha=0.9, label="问题一")
        ax.scatter(df1_prob2['timestamp'], df1_prob2["change_val"], color="blue", marker='o', alpha=0.9,
                   label="问题二")
        ax.scatter(df1_prob3['timestamp'], df1_prob3["change_val"], color="yellow", marker='o', alpha=0.9,
                   label="问题三")
        ax.scatter(df1_prob4['timestamp'], df1_prob4["change_val"], color="green", marker='o', alpha=0.9,
                   label="问题四")
        ax.scatter(df1_prob5['timestamp'], df1_prob5["change_val"], color="black", marker='x', alpha=0.9,
                   label="问题五")
        ax.scatter(df1_prob6['timestamp'], df1_prob6["change_val"], color="orange", marker='x', alpha=0.9,
                   label="问题六")
        ax.scatter(df1_prob7['timestamp'], df1_prob7["change_val"], color="pink", marker='x', alpha=0.9,
                   label="问题七")
        ax.scatter(df1_prob8['timestamp'], df1_prob8["change_val"], color="red", marker='o', alpha=0.9, label="问题八")
        plt.ylabel("转换值X", fontsize=20)
        ax.text(x_max, UCLx, "UCL", fontsize=15)
        ax.text(x_max, LCLx, "LCL", fontsize=15)
        ax.text(x_max, X_, "中心线", fontsize=15)
        ax.text(x_min, UCLx - sigmax * 0.5, "A", fontsize=20)
        ax.text(x_min, UCLx - sigmax * 1.5, "B", fontsize=20)
        ax.text(x_min, UCLx - sigmax * 2.5, "C", fontsize=20)
        ax.text(x_min, UCLx - sigmax * 3.5, "C", fontsize=20)
        ax.text(x_min, UCLx - sigmax * 4.5, "B", fontsize=20)
        ax.text(x_min, UCLx - sigmax * 5.5, "A", fontsize=20)
        plt.xlim(x_min, x_max)
        plt.legend()
        plt.title("设备编号{device_no},尺寸类别{size_type},转换值".format(device_no=device_no, size_type=size_type),
                  fontsize=20)
        plt.savefig(base_dir+"/static/{device_no}_{size_type}.png".format(device_no=device_no,size_type=size_type))

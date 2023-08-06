# -*- coding: utf-8 -*-
# @Time     : 2021/6/16 10:54
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : _classification.py
# @info     :


from sklearn.metrics import confusion_matrix,roc_curve,auc
import numpy as np


class Evaluation:
    def __init__(self, model_name,y_true, y_pred, lables=None, pos_label=1):
        self.model_name = model_name
        # sklearn.metrics.confusion_matrix()
        self.confusion_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=lables)
        _fpr, _tpr, thresholds = roc_curve(y_true, y_pred, pos_label=pos_label)
        self.auc = auc(_fpr, _tpr)
        self.kappa = kappa(self.confusion_matrix)
        self.sensitivity = sensitivity(self.confusion_matrix)
        self.specificity = specificity(self.confusion_matrix)
        self.accuracy = accuracy(self.confusion_matrix)
        self.precision = precision(self.confusion_matrix)
        self.recall = recall(self.confusion_matrix)
        self.f1_score = 2 * (self.precision * self.recall) / (self.precision + self.recall)

    def summary(self):
        print()


def kappa(c_matrix):
    '''
    :param c_matrix: 混淆矩阵
    :return: kappa 系数
    '''

    N = np.sum(c_matrix)
    ground_truth = np.sum(c_matrix, axis=0)  # 真值
    pre = np.sum(c_matrix, axis=1)  # 预测值

    po = np.trace(c_matrix)
    pe = np.dot(ground_truth, pre) / N ** 2

    kappa_coef = (po - pe) / (1 - pe)
    return kappa_coef


def sensitivity(c_matrix):
    '''
    :param c_matrix: 混淆矩阵
    :return: 灵敏度[TPR]
    '''
    assert np.array(c_matrix).shape == (2, 2)
    TP = c_matrix[0][0]
    FN = c_matrix[0][1]
    FP = c_matrix[1][0]
    TN = c_matrix[1][1]

    tpr = TP / (TP + FN)
    # tnr = TN / (FP + TN)
    return tpr


def specificity(c_matrix):
    '''
    :param c_matrix: 混淆矩阵
    :return: 特异度[TNR]
    '''
    assert np.array(c_matrix).shape == (2, 2)
    TP = c_matrix[0][0]
    FN = c_matrix[0][1]
    FP = c_matrix[1][0]
    TN = c_matrix[1][1]

    # tpr = TP / (TP + FN)
    tnr = TN / (FP + TN)
    return tnr


def accuracy(c_matrix):
    '''
    :param c_matrix: 混淆矩阵
    :return: acc
    '''
    return np.trace(c_matrix) / np.sum(c_matrix)


def precision(c_matrix):
    '''
    :param c_matrix:
    :return:
    '''
    assert np.array(c_matrix).shape == (2, 2)
    TP = c_matrix[0][0]
    FN = c_matrix[0][1]
    FP = c_matrix[1][0]
    TN = c_matrix[1][1]

    precise = TP / (TP + FP)
    return precise


def recall(c_matrix):
    assert np.array(c_matrix).shape == (2, 2)
    TP = c_matrix[0][0]
    FN = c_matrix[0][1]
    FP = c_matrix[1][0]
    TN = c_matrix[1][1]

    rc = TP / (TP + FN)
    return rc

if __name__ == '__main__':
    y_true = np.random.randint(2,size=1000)
    y_pred = np.random.randint(2,size=1000)
    print(y_true)
    print(y_pred)
    e = Evaluation(model_name='test',y_true=y_true,y_pred=y_pred,pos_label=1,lables=[1,0])
    print(e.confusion_matrix)
    print(e.auc)
    print(e.accuracy)
    print(e.recall)
    print(e.precision)
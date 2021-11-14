import numpy as np
import torch
from typing import Optional
from scipy.optimize import linear_sum_assignment


def cluster_accuracy(y_true, y_predicted, cluster_number: Optional[int] = None):
    """
    Calculate clustering accuracy after using the linear_sum_assignment function in SciPy to
    determine reassignments.
    :param y_true: list of true cluster numbers, an integer array 0-indexed
    :param y_predicted: list  of predicted cluster numbers, an integer array 0-indexed
    :param cluster_number: number of clusters, if None then calculated from input
    :return: reassignment dictionary, clustering accuracy
    """
    # 재할당 결정하기 위해 SciPy linear_sum_assignment사용 -> 클러스터링 정확도 계산수행
    # linear_sum_assignment = Hungrian Algorithm -> 클러스터링 군집 번호를 라벨과 최대한 맞도록 재정렬하는 과정수행(열, 행) https://hongl.tistory.com/159
    if cluster_number is None:
        cluster_number = (
            max(y_predicted.max(), y_true.max()) + 1
        )  # assume labels are 0-indexed
    count_matrix = np.zeros((cluster_number, cluster_number), dtype=np.int64)
    for i in range(y_predicted.size):
        count_matrix[y_predicted[i], y_true[i]] += 1

    row_ind, col_ind = linear_sum_assignment(count_matrix.max() - count_matrix)
    reassignment = dict(zip(row_ind, col_ind))
    accuracy = count_matrix[row_ind, col_ind].sum() / y_predicted.size
    return reassignment, accuracy


def target_distribution(batch: torch.Tensor) -> torch.Tensor:
    """
    Compute the target distribution p_ij, given the batch (q_ij), as in 3.1.3 Equation 3 of
    Xie/Girshick/Farhadi; this is used the KL-divergence loss function.
    :param batch: [batch size, number of clusters] Tensor of dtype float
    :return: [batch size, number of clusters] Tensor of dtype float
    """
    # KL-divergence 사용. 클러스터는 높은 신뢰도로 train하며 반복적으로 재정의. 특히, soft assignment를 target distribution에 매칭하여 train.
    # 즉, soft assignments qi와 보조의 타겟분포 pi의 KL-divergence loss가 DEC network의 loss가 됨.
    # Loss = pi가 qi로 추정하고 싶은 target 분포
    # target분포는 1.예측강화 2.높은 신뢰도로 할당된 data point에 더 강조 3. 클러스터 사이즈로 loss값 정규화. 클러스터사이즈가 클수록 loss에 주는 기여도가 커 전체 feature space를 왜곡방지.
    # https://leedakyeong.tistory.com/m/entry/%EB%85%BC%EB%AC%B8Unsupervised-Deep-Embedding-for-Clustering-AnalysisDEC
    # 이 training 전략은 self-training처럼 라벨링되지않은데이터셋에 초기 classfier를 사용해 라벨데이터를 만듬
    weight = (batch ** 2) / torch.sum(batch, 0)
    return (weight.t() / torch.sum(weight, 1)).t()
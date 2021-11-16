import torch
import torch.nn as nn
from torch.nn import Parameter
from typing import Optional


class ClusterAssignment(nn.Module):
    def __init__(
        self, cluster_number: int, embedding_dimension: int, alpha: float = 1.0, cluster_centers: Optional[torch.Tensor] = None,
    ) -> None:
        """
        Module to handle the soft assignment, for a description see in 3.1.1. in Xie/Girshick/Farhadi,
        where the Student's t-distribution is used measure similarity between feature vector and each
        cluster centroid.
        :param cluster_number: 클러스터의 개수
        :param embedding_dimension: feature 벡터의 임베딩 차원
        :param alpha: t-분포의 자유도를 나타내는 모수, default 1.0
        :param cluster_centers: clusters centers to initialise, if None then use Xavier uniform / 클러스터중심 초기화, None이면 Xavier유니폼사용
        """
        # soft assignment 처리 모듈. 스튜던트 T-분포를 사용 -> feature벡터와 각 클러스터중심 사이의 유사성 측정
        super(ClusterAssignment, self).__init__()
        self.embedding_dimension = embedding_dimension
        self.cluster_number = cluster_number
        self.alpha = alpha
        if cluster_centers is None:
            initial_cluster_centers = torch.zeros(
                self.cluster_number, self.embedding_dimension, dtype=torch.float
            )
            nn.init.xavier_uniform_(initial_cluster_centers)   # 클러스터중심이 None이면 가중치 초기화 방식을 Xavier Uniform 채택
        else:
            initial_cluster_centers = cluster_centers
        self.cluster_centers = Parameter(initial_cluster_centers) # 클러스터중심이 None가 아니면 일반 파라미터 목록에 추가

    def forward(self, batch: torch.Tensor) -> torch.Tensor:
        """
        Compute the soft assignment for a batch of feature vectors, returning a batch of assignments
        for each cluster. # feature 벡터 배치에 대한 soft assignment계산, 각 클러스터에 대한 할당배치 반환
        :param batch: FloatTensor of [batch size, embedding dimension]
        :return: FloatTensor [batch size, number of clusters]
        """
        # embedded point와 centroid를 계산하기 위해 t분포 사용
        # alpha는 t분포의 자유도. 이 떄, 교차검증을 하지 않기 때문에 자유도는 1 -> 즉 alpha=1
        # soft assignment: q_ij이면 i번째 데이터가 j번째 cluster에 속할 확률
        norm_squared = torch.sum((batch.unsqueeze(1) - self.cluster_centers) ** 2, 2)
        numerator = 1.0 / (1.0 + (norm_squared / self.alpha))
        power = float(self.alpha + 1) / 2
        numerator = numerator ** power
        return numerator / torch.sum(numerator, dim=1, keepdim=True)   # 이 5줄은 soft assignment식 구하기임. # 배치사이즈, 클러스터의 개수 반환
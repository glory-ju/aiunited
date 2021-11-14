import torch
import torch.nn as nn

from pt_DEC.cluster import ClusterAssignment


class DEC(nn.Module):
    def __init__(
        self,
        cluster_number: int,
        hidden_dimension: int, # hidden차원, 인코더의 아웃풋
        encoder: torch.nn.Module,
        alpha: float = 1.0, # t분포의 자유도
    ):
        """
        Module which holds all the moving parts of the DEC algorithm, as described in
        Xie/Girshick/Farhadi; this includes the AutoEncoder stage and the ClusterAssignment stage.
        :param cluster_number: number of clusters
        :param hidden_dimension: hidden dimension, output of the encoder
        :param encoder: encoder to use
        :param alpha: parameter representing the degrees of freedom in the t-distribution, default 1.0
        """
        super(DEC, self).__init__()
        self.encoder = encoder
        self.hidden_dimension = hidden_dimension
        self.cluster_number = cluster_number
        self.alpha = alpha
        self.assignment = ClusterAssignment(
            cluster_number, self.hidden_dimension, alpha
        )

    def forward(self, batch: torch.Tensor) -> torch.Tensor:
        """
        Compute the cluster assignment using the ClusterAssignment after running the batch
        through the encoder part of the associated AutoEncoder module.
        :param batch: [batch size, embedding dimension] FloatTensor    / 파라미터: 배치사이즈, 임베딩차원
        :return: [batch size, number of clusters] FloatTensor          / 리턴: 배치사이즈, 클러스터의 개수
        """
        # 오토인코더의 인코더 부분을 통해 배치 실행 -> clusterassignment를 사용해 cluster assignment 계산
        return self.assignment(self.encoder(batch))
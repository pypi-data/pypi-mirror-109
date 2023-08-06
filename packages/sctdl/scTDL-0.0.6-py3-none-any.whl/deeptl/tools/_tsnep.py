# -*- coding: utf-8 -*-

from typing import Optional

import torch
import numpy as np
import pandas as pd
import scipy
import scanpy as sc
from anndata import AnnData

from scanpy._utils import NeighborsView


def tsne_p(
        adata: AnnData,
        no_dims: int = 2,
        jitter: float = 4.,
        max_iter: int = 300,
        random_state: int = 0,
        dev: Optional[str] = None,
        neighbors_key: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if dev is None or dev == "cuda":
        if torch.cuda.is_available():
          dev = "cuda"
        else:
          dev = "cpu"
    
    device = torch.device(dev)
    
    rng = torch.Generator()
    rng.manual_seed(random_state)
    
    adata = adata.copy() if copy else adata
    
    if neighbors_key is None:
        neighbors_key = 'manifold'
    
    if neighbors_key not in adata.uns:
        raise ValueError(f'Did not find .uns["{neighbors_key}"].')
    
    neighbors = NeighborsView(adata, neighbors_key)
    
    P = torch.tensor(neighbors['connectivities'].toarray()).type(dtype=torch.float32).to(device)
    
    # Initialize variables
    n = P.shape[0]
    initial_momentum = 0.5
    final_momentum = 0.8
    eta = 500
    min_gain = 0.01
    eps = torch.tensor([1e-12]).to(device)
    Y = torch.randn(n, no_dims, generator=rng).to(device)
    dY = torch.zeros((n, no_dims)).to(device)
    iY = torch.zeros((n, no_dims)).to(device)
    gains = torch.ones((n, no_dims)).to(device)
    
    # Compute P-values
    P = P + P.T
    P = P / torch.sum(P)
    P = P * 4.									# early exaggeration
    P = torch.maximum(P, eps)
    
    # Run iterations
    for iter in range(max_iter):
        
        # Compute pairwise affinities
        sum_Y = torch.sum(torch.square(Y), 1)
        num = -2. * torch.matmul(Y, Y.T)
        num = 1. / (1. + torch.add(torch.add(num, sum_Y).T, sum_Y))
        num[range(n), range(n)] = 0.
        Q = num / torch.sum(num)
        Q = torch.maximum(Q, eps)
        
        # Compute gradient
        L = (P - Q) * num
        dY = torch.matmul(torch.diag(torch.sum(L, 0)) - L, Y)
        
        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((dY > 0.) != (iY > 0.)) + \
                (gains * 0.8) * ((dY > 0.) == (iY > 0.))
        gains[gains < min_gain] = min_gain
        iY = momentum * iY - eta * (gains * dY)
        Y = Y + iY
        Y = Y - torch.mean(Y, 0)
        
        # Compute current value of cost function
        if (iter + 1) % 50 == 0:
            C = torch.sum(P * torch.log(P / Q))
            print("Iteration %d: error is %f" % (iter + 1, C))
        
        # Stop lying about P-values
        if iter == 100:
            P = P / jitter
    
    adata.uns['tsne'] = {'params': {'no_dims': no_dims,
                                    'jitter': jitter,
                                    'max_iter': max_iter,
                                    'random_state': random_state}}
    
    adata.obsm['X_tsne'] = Y.cpu().numpy()
    
    return adata if copy else None


def tsne_p_numpy(
        adata: AnnData,
        no_dims: int = 2,
        jitter: float = 4.,
        max_iter: int = 300,
        random_state: int = 0,
        neighbors_key: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    """
        Runs t-SNE on the dataset in the NxD array X to reduce its
        dimensionality to no_dims dimensions. The syntaxis of the function is
        `Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array.
    """
    
    rng = np.random.RandomState(seed=random_state)
    
    adata = adata.copy() if copy else adata
    
    if neighbors_key is None:
        neighbors_key = 'manifold'
    
    if neighbors_key not in adata.uns:
        raise ValueError(f'Did not find .uns["{neighbors_key}"].')
    
    neighbors = NeighborsView(adata, neighbors_key)
    
    P = neighbors['connectivities'].toarray()
    
    # Initialize variables
    n = P.shape[0]
    initial_momentum = 0.5
    final_momentum = 0.8
    eta = 500
    min_gain = 0.01
    Y = rng.randn(n, no_dims)
    dY = np.zeros((n, no_dims))
    iY = np.zeros((n, no_dims))
    gains = np.ones((n, no_dims))
    
    # Compute P-values
    P = P + np.transpose(P)
    P = P / np.sum(P)
    P = P * 4.									# early exaggeration
    P = np.maximum(P, 1e-12)
    
    # Run iterations
    for iter in range(max_iter):
        
        # Compute pairwise affinities
        sum_Y = np.sum(np.square(Y), 1)
        num = -2. * np.matmul(Y, Y.T)
        num = 1. / (1. + np.add(np.add(num, sum_Y).T, sum_Y))
        num[range(n), range(n)] = 0.
        Q = num / np.sum(num)
        Q = np.maximum(Q, 1e-12)
        
        # Compute gradient
        L = (P - Q) * num
        dY = np.matmul(np.diag(np.sum(L, axis=0)) - L, Y)
        
        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((dY > 0.) != (iY > 0.)) + \
                (gains * 0.8) * ((dY > 0.) == (iY > 0.))
        gains[gains < min_gain] = min_gain
        iY = momentum * iY - eta * (gains * dY)
        Y = Y + iY
        Y = Y - np.tile(np.mean(Y, 0), (n, 1))
        
        # Compute current value of cost function
        if (iter + 1) % 50 == 0:
            C = np.sum(P * np.log(P / Q))
            print("Iteration %d: error is %f" % (iter + 1, C))
        
        # Stop lying about P-values
        if iter == 100:
            P = P / jitter
    
    adata.uns['tsne'] = {'params': {'no_dims': no_dims,
                                    'jitter': jitter,
                                    'max_iter': max_iter,
                                    'random_state': random_state}}
    
    adata.obsm['X_tsne'] = Y
    
    return adata if copy else None




















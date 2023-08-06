# -*- coding: utf-8 -*-

from typing import Optional

import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse
from sklearn.neighbors import NearestNeighbors
import scanpy as sc
from anndata import AnnData

from scanpy.preprocessing import pca
from scanpy.tools._utils import _choose_representation


def knn_obs(
        adata: AnnData,
        n_neighbors: int = 15,
        n_pcs: Optional[int] = None,
        use_rep: Optional[str] = None,
        metric: str = 'euclidean',
        symmetrize: str = 'union',
        random_state: int = 0,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if symmetrize not in ['union', 'intersection']:
        raise ValueError("{symmetrize} is invalid, should be one of ['union', 'intersection']")
    
    adata = adata.copy() if copy else adata
    
    
    X = _choose_representation(adata, use_rep=use_rep, n_pcs=n_pcs)
    
    print("Computing KNN", flush=True)
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric=metric).fit(X)
    knn_network = nbrs.kneighbors_graph(X) - scipy.sparse.eye(X.shape[0])
    
    print("Symmetrizing affinities", flush=True)
    knn_network = knn_network + knn_network.T
    if symmetrize == 'union':
        knn_network.data[knn_network.data > 0] = 1
    elif symmetrize == 'intersection':
        knn_network.data[knn_network.data < 2] = 0
        knn_network.data[knn_network.data > 0] = 1
    
    
    if key_added is None:
        key_added = 'knn_obs'
        knn_key = 'knn'
    else:
        knn_key = key_added + '_knn'
    
    adata.uns[key_added] = {}
    
    knn_dict = adata.uns[key_added]
    
    knn_dict['knn_key'] = knn_key
    
    knn_dict['params'] = {}
    knn_dict['params']['n_neighbors'] = n_neighbors
    knn_dict['params']['metric'] = metric
    knn_dict['params']['symmetrize'] = symmetrize
    knn_dict['params']['random_state'] = random_state
    
    if n_pcs is not None:
        knn_dict['params']['n_pcs'] = n_pcs
    
    if use_rep is not None:
        knn_dict['params']['use_rep'] = use_rep
    
    adata.obsp[knn_key] = knn_network
    
    return adata if copy else None


def knn_var(
        adata: AnnData,
        n_neighbors: int = 15,
        n_pcs: Optional[int] = None,
        metric: str = 'euclidean',
        symmetrize: str = 'union',
        random_state: int = 0,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if symmetrize not in ['union', 'intersection']:
        raise ValueError("{symmetrize} is invalid, should be one of ['union', 'intersection']")
    
    adata = adata.copy() if copy else adata
    
    X = adata.X.toarray().T if issparse(adata.X) else adata.X.T
    
    
    if n_pcs is not None:
        print("Computing PCA", flush=True)
        X = pca(X, n_comps=n_pcs, random_state=random_state)
    
    print("Computing KNN", flush=True)
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric=metric).fit(X)
    knn_network = nbrs.kneighbors_graph(X) - scipy.sparse.eye(X.shape[0])
    
    print("Symmetrizing affinities", flush=True)
    knn_network = knn_network + knn_network.T
    if symmetrize == 'union':
        knn_network.data[knn_network.data > 0] = 1
    elif symmetrize == 'intersection':
        knn_network.data[knn_network.data < 2] = 0
        knn_network.data[knn_network.data > 0] = 1
    
    
    if key_added is None:
        key_added = 'knn_var'
        knn_key = 'knn'
    else:
        knn_key = key_added + '_knn'
    
    adata.uns[key_added] = {}
    
    knn_dict = adata.uns[key_added]
    
    knn_dict['knn_key'] = knn_key
    
    knn_dict['params'] = {}
    knn_dict['params']['n_neighbors'] = n_neighbors
    knn_dict['params']['metric'] = metric
    knn_dict['params']['symmetrize'] = symmetrize
    knn_dict['params']['random_state'] = random_state
    
    if n_pcs is not None:
        knn_dict['params']['n_pcs'] = n_pcs
    
    adata.varp[knn_key] = knn_network
    
    return adata if copy else None




















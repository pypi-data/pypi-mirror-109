# -*- coding: utf-8 -*-

from typing import Optional

import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse
from sklearn.neighbors import NearestNeighbors
import scanpy as sc
from anndata import AnnData

from scanpy.tools._utils import _choose_representation


def knn_obs_minibatch(
        adata: AnnData,
        n_neighbors: int = 5,
        n_pcs: Optional[int] = None,
        use_rep: Optional[str] = None,
        metric: str = 'euclidean',
        symmetrize: str = 'union',
        random_state: int = 0,
        ref_key: Optional[str] = None,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if symmetrize not in ['union', 'intersection']:
        raise ValueError("{symmetrize} is invalid, should be one of ['union', 'intersection']")
    
    adata = adata.copy() if copy else adata
    
    if ref_key is None or ref_key == 'reference_centers':
        if 'reference_centers' not in adata.obs.columns:
            raise KeyError('No "reference_centers" in .obs')
        center_idx = np.flatnonzero(adata.obs['reference_centers'])
    else:
        if ref_key not in adata.obs.columns:
            raise KeyError(f'No "{ref_key}" in .obs')
        center_idx = np.flatnonzero(adata.obs[ref_key])
    
    
    X = _choose_representation(adata, use_rep=use_rep, n_pcs=n_pcs)
    
    print("Computing KNN", flush=True)
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric=metric).fit(X[center_idx,:])
    knn_network = nbrs.kneighbors_graph(X).tolil()
    
    print("Symmetrizing affinities", flush=True)
    knn_network[center_idx, np.arange(center_idx.shape[0])] = 0
    knn_network_ref = knn_network[np.ix_(center_idx, np.arange(center_idx.shape[0]))]
    knn_network_ref = knn_network_ref + knn_network_ref.T
    if symmetrize == 'union':
        knn_network_ref.data[knn_network_ref.data > 0] = 1
    elif symmetrize == 'intersection':
        knn_network_ref.data[knn_network_ref.data < 2] = 0
        knn_network_ref.data[knn_network_ref.data > 0] = 1
    knn_network[np.ix_(center_idx, np.arange(center_idx.shape[0]))] = knn_network_ref
    knn_network = knn_network.tocsr()
    
    
    if key_added is None:
        key_added = 'knn_obs_minibatch'
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
    
    adata.obsm[knn_key] = knn_network
    
    return adata if copy else None




















# -*- coding: utf-8 -*-

from typing import Optional

import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics.pairwise import euclidean_distances
import scanpy as sc
from anndata import AnnData

from scanpy.tools._utils import _choose_representation


def reference_centers_random(
        adata: AnnData,
        n_centers: int,
        random_state: int = 0,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if n_centers > adata.shape[0]:
        raise ValueError("n_centers {n_centers} should be smaller than n_obs {adata.shape[0]}")
    
    rng = np.random.RandomState(seed=random_state)
    
    adata = adata.copy() if copy else adata
    
    
    reference_centers = pd.Series(False, index=adata.obs_names)
    reference_centers.iloc[rng.choice(np.arange(adata.shape[0]), size=n_centers, replace=False)] = True
    
    
    if key_added is None:
        key_added = 'reference_centers'
    
    adata.uns[key_added] = {}
    
    ref_dict = adata.uns[key_added]
    
    ref_dict['params'] = {}
    ref_dict['params']['n_centers'] = np.count_nonzero(reference_centers)
    ref_dict['params']['method'] = 'random'
    ref_dict['params']['random_state'] = random_state
    
    adata.obs[key_added] = reference_centers
    
    return adata if copy else None


def reference_centers_kmeans(
        adata: AnnData,
        n_centers: int,
        method: str = 'MiniBatchKMeans',
        n_pcs: Optional[int] = None,
        use_rep: Optional[str] = None,
        random_state: int = 0,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    if method not in ['MiniBatchKMeans', 'KMeans']:
        raise ValueError("{method} is invalid, should be one of ['MiniBatchKMeans', 'KMeans']")
    
    if n_centers > adata.shape[0]:
        raise ValueError("n_centers {n_centers} should be smaller than n_obs {adata.shape[0]}")
    
    adata = adata.copy() if copy else adata
    
    
    X = _choose_representation(adata, use_rep=use_rep, n_pcs=n_pcs)
    
    if method == 'MiniBatchKMeans':
        kmeans = MiniBatchKMeans(n_clusters=n_centers, random_state=random_state).fit(X)
        print("When using MiniBatchKMeans, resulting n_centers may less than provided n_centers", flush=True)
    else:
        kmeans = KMeans(n_clusters=n_centers, random_state=random_state).fit(X)
    
    reference_centers = pd.Series(False, index=adata.obs_names)
    reference_centers.iloc[np.unique(np.argmin(euclidean_distances(X, kmeans.cluster_centers_), axis=0))] = True
    
    
    if key_added is None:
        key_added = 'reference_centers'
    
    adata.uns[key_added] = {}
    
    ref_dict = adata.uns[key_added]
    
    ref_dict['params'] = {}
    ref_dict['params']['n_centers'] = np.count_nonzero(reference_centers)
    print("resulting n_centers is", ref_dict['params']['n_centers'], flush=True)
    ref_dict['params']['method'] = method
    ref_dict['params']['random_state'] = random_state
    
    if n_pcs is not None:
        ref_dict['params']['n_pcs'] = n_pcs
    
    if use_rep is not None:
        ref_dict['params']['use_rep'] = use_rep
    
    adata.obs[key_added] = reference_centers
    
    return adata if copy else None




















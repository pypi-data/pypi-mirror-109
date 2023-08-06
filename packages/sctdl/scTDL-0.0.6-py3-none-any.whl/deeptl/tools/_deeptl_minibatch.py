# -*- coding: utf-8 -*-

from typing import Optional, Tuple, Sequence

import torch
from torch import Tensor
import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse, csr_matrix, lil_matrix
import scanpy as sc
from anndata import AnnData
import time

from ._deeptl import DeepTL_TL


@torch.no_grad()
def DeepTL_minibatch(
        adata: AnnData,
        center_idx: np.ndarray,
        betas: float = 0.01,
        tol_err: float = 1e-8,
        maxIter: int = 1000,
        deep: int = 1,
        SS_matrix: Optional[np.ndarray] = None,
        FS_matrix: Optional[np.ndarray] = None,
        random_state: int = 0,
        dev: Optional[str] = None,
        ) -> Tuple[np.ndarray, np.ndarray]:
    
    if dev is None or dev == "cuda":
        if torch.cuda.is_available():
          dev = "cuda"
        else:
          dev = "cpu"
    
    device = torch.device(dev)
    
    rng = torch.Generator()
    rng.manual_seed(random_state)
    rng_numpy = np.random.RandomState(seed=random_state)
    
    deep_max = 5
    if deep > deep_max:
        deep = deep_max
    
    X = adata.X.toarray().T if issparse(adata.X) else adata.X.T
    X = torch.tensor(X).type(dtype=torch.float32).to(device)
    
    m, n = X.shape
    k = center_idx.shape[0]
    
    batch_size = k
    num_batches = (n - k) // batch_size
    batch_size_extra = (n - k) % batch_size
    
    W = torch.rand(m, m, generator=rng).to(device)
    
    V = torch.rand(k, n, generator=rng).to(device)
    
    X_ref = X[:, center_idx]
    
    data_idx = np.setdiff1d(np.arange(n), center_idx)
    
    time_deep = time.time()
    
    for dep in range(deep):
        
        print('deep:', dep+1, flush=True)
        
        if SS_matrix is not None:
            SS_matrix_batch = SS_matrix[:, center_idx]
        else:
            SS_matrix_batch = None
        
        W, V[:, center_idx], FUNC_ERR = DeepTL_TL(
            X_ref,
            W,
            V[:, center_idx],
            beta=betas,
            tol_err=tol_err,
            maxIter=maxIter,
            SS_matrix=SS_matrix_batch,
            FS_matrix=FS_matrix,
            dev=dev,
            )
        
        n_perm = rng_numpy.permutation(data_idx)
        
        time_batch = time.time()
        
        for batch_i in range(num_batches+1):
            
            if batch_i < num_batches:
                batch_idx = n_perm[(batch_i * batch_size):((batch_i+1) * batch_size)]
            elif batch_size_extra:
                batch_idx = n_perm[-batch_size:]
            else:
                break
            
            n_batch = batch_idx.shape[0]
            
            SS_matrix_batch = np.ones((k+n_batch, k+n_batch))
            SS_matrix_batch[np.ix_(np.arange(k), np.arange(k))] = 0
            SS_matrix_batch[np.ix_(np.arange(k, k+n_batch), np.arange(k, k+n_batch))] = 0
            
            if SS_matrix is not None:
                SS_matrix_batch[np.ix_(np.arange(k), np.arange(k, k+n_batch))] = SS_matrix[:, batch_idx]
                SS_matrix_batch[np.ix_(np.arange(k, k+n_batch), np.arange(k))] = SS_matrix[:, batch_idx].T
            
            X_batch = torch.cat((X_ref, X[:, batch_idx]), axis=1)
            
            Z_batch = torch.zeros((k+n_batch, k+n_batch)).to(device)
            Z_batch[np.ix_(np.arange(k), np.arange(k, k+n_batch))] = V[:, batch_idx]
            Z_batch[np.ix_(np.arange(k, k+n_batch), np.arange(k))] = V[:, batch_idx].T
            
            W, Z_batch, FUNC_ERR = DeepTL_TL(
                X_batch,
                W,
                Z_batch,
                beta=betas,
                tol_err=tol_err,
                maxIter=maxIter,
                SS_matrix=SS_matrix_batch,
                FS_matrix=FS_matrix,
                dev=dev,
                )
            
            V[:, batch_idx] = Z_batch[np.ix_(np.arange(k), np.arange(k, k+n_batch))]
            
            if batch_i % 1 == 0:
                print("batch", batch_i+1, "time:", time.time()-time_batch, flush=True)
                time_batch = time.time()
        
        if deep % 1 == 0:
                print("deep", dep+1, "time:", time.time()-time_deep, flush=True)
                time_deep = time.time()
    
    return W.cpu().numpy(), V.cpu().numpy()


def run_DeepTL_minibatch(
        adata: AnnData,
        betas: float = 0.01,
        tol_err: float = 1e-8,
        maxIter: int = 1000,
        deep: int = 1,
        random_state: int = 0,
        dev: Optional[str] = None,
        ref_key: Optional[str] = None,
        use_knn_obs: bool = False,
        use_knn_var: bool = False,
        knn_obs_key: Optional[str] = None,
        knn_var_key: Optional[str] = None,
        key_added: Optional[str] = None,
        key_added_var: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    n, m = adata.shape
    
    SSMatrix = None
    FSMatrix = None
    
    if ref_key is None or ref_key == 'reference_centers':
        if 'reference_centers' not in adata.obs.columns:
            raise KeyError('No "reference_centers" in .obs')
        center_idx = np.flatnonzero(adata.obs['reference_centers'])
    else:
        if ref_key not in adata.obs.columns:
            raise KeyError(f'No "{ref_key}" in .obs')
        center_idx = np.flatnonzero(adata.obs[ref_key])
    
    if use_knn_obs:
        if knn_obs_key is None or knn_obs_key == 'knn_obs_minibatch':
            if 'knn_obs_minibatch' not in adata.uns:
                raise KeyError('No "knn_obs_minibatch" in .uns')
            SSMatrix = adata.obsm[adata.uns['knn_obs_minibatch']['knn_key']].toarray().T
        else:
            if knn_obs_key not in adata.uns:
                raise KeyError(f'No "{knn_obs_key}" in .uns')
            SSMatrix = adata.obsm[adata.uns[knn_obs_key]['knn_key']].toarray().T
    
    if use_knn_var:
        if knn_var_key is None or knn_var_key == 'knn_var':
            if 'knn_var' not in adata.uns:
                raise KeyError('No "knn_var" in .uns')
            FSMatrix = adata.varp[adata.uns['knn_var']['knn_key']].toarray()
        else:
            if knn_var_key not in adata.uns:
                raise KeyError(f'No "{knn_var_key}" in .uns')
            FSMatrix = adata.varp[adata.uns[knn_var_key]['knn_key']].toarray()
    
    
    W, V = DeepTL_minibatch(adata,
                            center_idx=center_idx,
                            betas=betas,
                            tol_err=tol_err,
                            maxIter=maxIter,
                            deep=deep,
                            SS_matrix=SSMatrix,
                            FS_matrix=FSMatrix,
                            random_state=random_state,
                            dev=dev)
    
    Z = lil_matrix((n, n))
    Z[center_idx, :] = V
    # Z[:, center_idx] = V.T
    Z = Z.tocsr()
    
    
    if key_added is None:
        key_added = 'manifold'
        conns_key = 'manifold'
        dists_key = 'manifold'
    else:
        conns_key = key_added + '_manifold'
        dists_key = key_added + '_manifold'
    
    adata.uns[key_added] = {}
    
    neighbors_dict = adata.uns[key_added]
    
    neighbors_dict['connectivities_key'] = conns_key
    neighbors_dict['distances_key'] = dists_key
    
    neighbors_dict['params'] = {}
    neighbors_dict['params']['n_neighbors'] = Z.count_nonzero() // Z.shape[0]
    neighbors_dict['params']['betas'] = betas
    neighbors_dict['params']['tol_err'] = tol_err
    neighbors_dict['params']['maxIter'] = maxIter
    neighbors_dict['params']['deep'] = deep
    neighbors_dict['params']['use_knn_obs'] = use_knn_obs
    neighbors_dict['params']['random_state'] = random_state
    
    adata.obsm[conns_key] = V.T
    adata.obsp[conns_key] = Z
    
    
    if key_added_var is None:
        key_added_var = 'manifold_var'
        conns_var_key = 'manifold'
        dists_var_key = 'manifold'
    else:
        conns_var_key = key_added_var + '_manifold'
        dists_var_key = key_added_var + '_manifold'
    
    adata.uns[key_added_var] = {}
    
    neighbors_var_dict = adata.uns[key_added_var]
    
    neighbors_var_dict['connectivities_key'] = conns_var_key
    neighbors_var_dict['distances_key'] = dists_var_key
    
    neighbors_var_dict['params'] = {}
    neighbors_var_dict['params']['n_neighbors'] = np.count_nonzero(W) // W.shape[0]
    neighbors_var_dict['params']['betas'] = betas
    neighbors_var_dict['params']['tol_err'] = tol_err
    neighbors_var_dict['params']['maxIter'] = maxIter
    neighbors_var_dict['params']['deep'] = deep
    neighbors_var_dict['params']['use_knn_var'] = use_knn_var
    neighbors_var_dict['params']['random_state'] = random_state
    
    adata.varp[conns_var_key] = csr_matrix(W)
    
    return adata if copy else None




















# -*- coding: utf-8 -*-

from typing import Optional, Tuple

import torch
from torch import Tensor
import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse, csr_matrix
import scanpy as sc
from anndata import AnnData


@torch.no_grad()
def DeepTL_W(
        X: Tensor,
        Z: Tensor,
        Y_w: Tensor,
        z_eye: Tensor,
        ones_w: Tensor,
        lamba_w: Tensor,
        beta: float,
        rho: float,
        ceta: float,
        ) -> Tuple[Tensor, Tensor]:
    
    optimize_zz = torch.matmul(Z, Z.T) + z_eye
    
    L_w_matrix = torch.matmul(torch.matmul(X, 2*optimize_zz - 2*Z), X.T)
        
    L_w = 2*torch.norm(L_w_matrix, 2)+ beta * lamba_w.shape[1] / ceta
    
    M_w = torch.matmul(2*L_w_matrix + beta/ceta, Y_w) - 2*torch.matmul(torch.matmul(X, optimize_zz), X.T) - beta/ceta + lamba_w
    
    W = (Y_w - M_w/L_w) * ones_w
    W = (torch.abs(W) + W) / 2
    W = (W + W.T) / 2
    
    leq3 = torch.sum(W, dim=0) - 1
    
    lamba_w = lamba_w + beta*rho*leq3
    
    return W, lamba_w


@torch.no_grad()
def DeepTL_Z(
        X: Tensor,
        W: Tensor,
        Y_z: Tensor,
        w_eye: Tensor,
        ones_z: Tensor,
        lamba_z: Tensor,
        beta: float,
        rho: float,
        ceta: float,
        ) -> Tuple[Tensor, Tensor]:
    
    optimize_ww = torch.matmul(W, W.T) + w_eye
    
    L_z_matrix = torch.matmul(torch.matmul(X.T, 2*optimize_ww - 2*W), X)
    
    L_z = 2*torch.norm(L_z_matrix, 2) + beta * lamba_z.shape[1] / ceta
    
    M_z = torch.matmul(2*L_z_matrix + beta/ceta, Y_z) - 2*torch.matmul(torch.matmul(X.T, optimize_ww), X) - beta/ceta + lamba_z
    
    Z = (Y_z - M_z/L_z) * ones_z
    Z = (torch.abs(Z) + Z)/2
    Z = (Z + Z.T)/2
    
    leq4 = torch.sum(Z, dim=0) - 1
    
    lamba_z = lamba_z + beta*rho*leq4
    
    return Z, lamba_z


@torch.no_grad()
def DeepTL_TL(
        X: Tensor,
        W: Tensor,
        Z: Tensor,
        beta: float,
        tol_err: float,
        maxIter: int,
        SS_matrix: Optional[np.ndarray],
        FS_matrix: Optional[np.ndarray],
        dev: str,
        ) -> Tuple[Tensor, Tensor, Tensor]:
    
    device = torch.device(dev)
    
    m, n = X.shape
    
    rho = 0.8
    ceta_prev = 1 / rho
    ceta = 1
    
    func_err = float('inf')
    
    W_prev = W
    Z_prev = Z
    
    lamba_w = torch.zeros(1, m).to(device)
    lamba_z = torch.zeros(1, n).to(device)
    
    z_eye = torch.eye(n).to(device)
    w_eye = torch.eye(m).to(device)
    
    if SS_matrix is None:
        ones_z = 1 - z_eye
    else:
        ones_z = torch.tensor(SS_matrix, dtype=torch.float32).to(device)
    
    if FS_matrix is None:
        ones_w = 1 - w_eye
    else:
        ones_w = torch.tensor(FS_matrix, dtype=torch.float32).to(device)
    
    for Iter in range(maxIter):
        
        func_err_prev = func_err
        
        Y_iter_value = (ceta * (1 - ceta_prev)) / ceta_prev
        
        Y_w = W + Y_iter_value * (W - W_prev)
        Y_z = Z + Y_iter_value * (Z - Z_prev)
        
        W_prev = W
        Z_prev = Z
        
        W, lamba_w = DeepTL_W(
            X=X,
            Z=Z,
            Y_w=Y_w,
            z_eye=z_eye,
            ones_w=ones_w,
            lamba_w=lamba_w,
            beta=beta,
            rho=rho,
            ceta=ceta,
            )
        
        Z, lamba_z = DeepTL_Z(
            X=X,
            W=W,
            Y_z=Y_z,
            w_eye=w_eye,
            ones_z=ones_z,
            lamba_z=lamba_z,
            beta=beta,
            rho=rho,
            ceta=ceta,
            )
        
        ceta_prev = ceta
        ceta = 1 / (1 - rho + 1 / ceta)
        
        func_1_err = torch.norm(torch.matmul(W.T, torch.matmul(X, z_eye-Z)), 'fro')
        func_2_err = torch.norm(torch.matmul(X, z_eye-Z), 'fro')
        func_3_err = torch.norm(torch.matmul(Z.T, torch.matmul(X.T, w_eye-W)), 'fro')
        func_4_err = torch.norm(torch.matmul(X.T, w_eye-W), 'fro')
        
        func_err = func_1_err + func_2_err + func_3_err + func_4_err
        
        func_err_rel = torch.abs(func_err_prev - func_err) / func_err_prev
        
        if Iter == 0 or (Iter+1) % 100 == 0:
            print('iter', str(Iter+1)+',', 'func_err='+str(func_err.item()), flush=True)
        
        if func_err_rel < tol_err:
            print('iter', str(Iter+1)+',', 'func_err='+str(func_err.item())+',', 'TL converged!', flush=True)
            break
        
    return W, Z, func_err


@torch.no_grad()
def DeepTL_main(
        adata: AnnData,
        betas: float = 0.01,
        tol_err: float = 1e-8,
        maxIter: int = 1000,
        deep: int = 1,
        SSMatrix: Optional[np.ndarray] = None,
        FSMatrix: Optional[np.ndarray] = None,
        random_state: int = 0,
        dev: Optional[str] = None,
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    if dev is None or dev == "cuda":
        if torch.cuda.is_available():
          dev = "cuda"
        else:
          dev = "cpu"
    
    device = torch.device(dev)
    
    rng = torch.Generator()
    rng.manual_seed(random_state)
    
    deep_max = 5
    if deep > deep_max:
        deep = deep_max
    
    X = adata.X.toarray().T if issparse(adata.X) else adata.X.T
    r = torch.tensor(X).type(dtype=torch.float32).to(device)
    m, n = X.shape
    W = torch.rand(m, m, generator=rng).to(device)
    Z = torch.rand(n, n, generator=rng).to(device)
    
    for dep in range(deep):
        print('deep:', dep+1, flush=True)
        
        if dep:
            r = torch.matmul(torch.matmul(W, r), Z.T)
        
        W, Z, err = DeepTL_TL(
            X=r,
            W=W,
            Z=Z,
            beta=betas,
            tol_err=tol_err/(dep+1),
            maxIter=maxIter,
            SS_matrix=SSMatrix,
            FS_matrix=FSMatrix,
            dev=dev,
            )
    
    return W.cpu().numpy(), Z.cpu().numpy(), err.cpu().numpy()


def run_DeepTL(
        adata: AnnData,
        betas: float = 0.01,
        tol_err: float = 1e-8,
        maxIter: int = 1000,
        deep: int = 1,
        random_state: int = 0,
        dev: Optional[str] = None,
        use_knn_obs: bool = False,
        use_knn_var: bool = False,
        knn_obs_key: Optional[str] = None,
        knn_var_key: Optional[str] = None,
        key_added: Optional[str] = None,
        key_added_var: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    
    SSMatrix = None
    FSMatrix = None
    
    if use_knn_obs:
        if knn_obs_key is None or knn_obs_key == 'knn_obs':
            if 'knn_obs' not in adata.uns:
                raise KeyError('No "knn_obs" in .uns')
            SSMatrix = adata.obsp[adata.uns['knn_obs']['knn_key']].toarray()
        else:
            if knn_obs_key not in adata.uns:
                raise KeyError(f'No "{knn_obs_key}" in .uns')
            SSMatrix = adata.obsp[adata.uns[knn_obs_key]['knn_key']].toarray()
    
    if use_knn_var:
        if knn_var_key is None or knn_var_key == 'knn_var':
            if 'knn_var' not in adata.uns:
                raise KeyError('No "knn_var" in .uns')
            FSMatrix = adata.varp[adata.uns['knn_var']['knn_key']].toarray()
        else:
            if knn_var_key not in adata.uns:
                raise KeyError(f'No "{knn_var_key}" in .uns')
            FSMatrix = adata.varp[adata.uns[knn_var_key]['knn_key']].toarray()
    
    
    W, Z, err = DeepTL_main(
        adata=adata,
        betas=betas,
        tol_err=tol_err,
        maxIter=maxIter,
        deep=deep,
        SSMatrix=SSMatrix,
        FSMatrix=FSMatrix,
        random_state=random_state,
        dev=dev,
        )
    
    
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
    neighbors_dict['params']['n_neighbors'] = np.count_nonzero(Z) // Z.shape[0]
    neighbors_dict['params']['betas'] = betas
    neighbors_dict['params']['tol_err'] = tol_err
    neighbors_dict['params']['maxIter'] = maxIter
    neighbors_dict['params']['deep'] = deep
    neighbors_dict['params']['use_knn_obs'] = use_knn_obs
    neighbors_dict['params']['random_state'] = random_state
    
    adata.obsp[conns_key] = csr_matrix(Z)
    
    
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




















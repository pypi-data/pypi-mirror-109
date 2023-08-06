# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import scipy
import scanpy as sc
from anndata import AnnData
from tqdm import tqdm


def enrich_pathway(
        adata: AnnData,
        pathway: Union[pd.Series, pd.DataFrame],
        weight_threshold: float = 0.8,
        top_n_markers: int = 100,
        marker_enrich_threshold: float = 0.3,
        min_genes: int = 5,
        neighbors_var_key: Optional[str] = None,
        marker_key: Optional[str] = None,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    
    if neighbors_var_key is None:
        neighbors_var_key = 'manifold_var'
    
    if neighbors_var_key not in adata.uns:
        raise ValueError(f'Did not find .uns["{neighbors_var_key}"].')
    
    conns_var_key = adata.uns[neighbors_var_key]['connectivities_key']
    
    if conns_var_key not in adata.varp:
        raise ValueError(f'Did not find .varp["{conns_var_key}"].')
    
    if marker_key is None:
        marker_key = 'rank_genes_groups'
    
    if marker_key not in adata.uns:
        raise ValueError(
            'Could not find marker gene data. '
            'Please run `sc.tl.rank_genes_groups()` first.'
        )
    
    
    marker_genes = pd.DataFrame(adata.uns[marker_key]['names']).iloc[:top_n_markers,:]
    
    weights = pd.Series(np.squeeze(adata.varp[conns_var_key].sum(axis=0).A, axis=0), index=adata.var_names)
    
    if isinstance(pathway, pd.DataFrame):
        pathway = pathway.iloc[:,0]
    
    pathway_unique = np.unique(pathway.index)
    
    pathway_enriched = {}
    
    for idx in tqdm(range(pathway_unique.shape[0])):
        elements = pathway.loc[pathway_unique[idx]]
        if isinstance(elements, str):
            elements = pd.Series(elements)
        elements = elements[elements.isin(adata.var_names)]
        pathway_df = weights.loc[elements].reset_index()
        pathway_df = pathway_df[pathway_df.iloc[:,1] > weight_threshold]
        
        marker_enrich_percent = np.sum(marker_genes.isin(pathway_df.iloc[:,0].values), axis=0) / pathway_df.shape[0]
        
        if pathway_df.shape[0] >= min_genes and np.any(marker_enrich_percent > marker_enrich_threshold):
            pathway_enriched[pathway_unique[idx]] = pathway_df.to_records(index=False)
    
    print("number of enriched pathways:", len(pathway_enriched), flush=True)
    
    
    if key_added is None:
        key_added = 'enrich_pathway'
    
    adata.uns[key_added] = {}
    
    pathway_dict = adata.uns[key_added]
    
    pathway_dict['pathway'] = pathway_enriched
    
    pathway_dict['params'] = {}
    pathway_dict['params']['weight_threshold'] = weight_threshold
    pathway_dict['params']['top_n_markers'] = top_n_markers
    pathway_dict['params']['marker_enrich_threshold'] = marker_enrich_threshold
    pathway_dict['params']['min_genes'] = min_genes
    
    return adata if copy else None


def aucell_pathway(
        adata: AnnData,
        auc_threshold: float = 0.05,
        noweights: bool = False,
        normalize: bool = False,
        random_state: int = 0,
        key: Optional[str] = None,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    
    if key is None:
        key = 'enrich_pathway'
    
    if key not in adata.uns:
        raise ValueError(f'Did not find .uns["{key}"].')
    
    
    pathway_enriched = adata.uns[key]['pathway']
    
    ex_mtx = adata.to_df()
    
    df_rnk = ex_mtx.sample(frac=1.0, replace=False, axis=1, random_state=random_state).rank(axis=1, ascending=False, method='first', na_option='bottom').astype('uint32') - 1
    var_names = df_rnk.columns
    df_rnk = df_rnk.to_numpy()
    
    ex_mtx_argsort = np.argsort(df_rnk, axis=1)
    
    auc_mtx = pd.DataFrame(index=ex_mtx.index)
    
    auc_cutoff = round(auc_threshold * ex_mtx.shape[1])
    
    weights_mask = np.repeat(np.arange(auc_cutoff)[None, :], ex_mtx.shape[0], axis=0)
    weights_mask = weights_mask < np.sum(ex_mtx.to_numpy() > 0, axis=1, keepdims=True)
    
    for pth in tqdm(pathway_enriched.keys()):
        pathway_df = pd.DataFrame(pathway_enriched[pth]).to_numpy()
        weights_df = pd.Series(0, index=var_names)
        if noweights:
            weights_tmp = np.ones(pathway_df.shape[0])
        else:
            weights_tmp = pathway_df[:,1].astype(np.float64)
        weights_df[pathway_df[:,0]] = weights_tmp
        weights_sorted = weights_df.to_numpy()[ex_mtx_argsort][:,:auc_cutoff] * weights_mask
        auc_mtx[pth] = np.sum(np.cumsum(weights_sorted, axis=1) , axis=1) / (np.sum(weights_tmp) * auc_cutoff)
    
    auc_mtx = auc_mtx.astype(np.float64)
    
    if normalize:
        auc_mtx /= auc_mtx.max(axis=0)
    
    
    if key_added is None:
        key_added = 'aucell_pathway'
    
    adata.uns[key_added] = {}
    
    aucell_dict = adata.uns[key_added]
    
    aucell_dict['params'] = {}
    aucell_dict['params']['auc_threshold'] = auc_threshold
    aucell_dict['params']['noweights'] = noweights
    aucell_dict['params']['normalize'] = normalize
    aucell_dict['params']['random_state'] = random_state
    
    adata.obsm[key_added] = auc_mtx.loc[adata.obs_names,:]
    
    return adata if copy else None




















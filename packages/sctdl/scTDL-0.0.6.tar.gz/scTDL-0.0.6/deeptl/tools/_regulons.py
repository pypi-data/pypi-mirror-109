# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd
import scipy
import scanpy as sc
from anndata import AnnData
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pyscenic.rnkdb import FeatherRankingDatabase as RankingDatabase
from pyscenic.utils import modules_from_adjacencies
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell as pyscenic_aucell


def regulons(
        adata: AnnData,
        tf_names: Optional[Sequence[str]] = None,
        motif_annotations_fname: Optional[str] = None,
        db_fnames: Optional[Sequence[str]] = None,
        thresholds=(0.75, 0.90),
        top_n_targets=(50,),
        top_n_regulators=(5,10,50),
        min_genes=20,
        neighbors_var_key: Optional[str] = None,
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
    
    
    neighbors = pd.DataFrame(adata.varp[conns_var_key].toarray(),
                             index=adata.var_names,
                             columns=adata.var_names)
    
    if tf_names is None:
        neighbors = pd.melt(neighbors, ignore_index=False)
        neighbors.columns = ['target', 'importance']
        neighbors = neighbors.reset_index()
    else:
        tf_idx = np.flatnonzero(np.isin(adata.var_names, tf_names))
        if tf_idx.shape[0] == 0:
            raise ValueError("Could not find any tf in var_names")
        neighbors = pd.melt(neighbors.iloc[tf_idx, :], ignore_index=False)
        neighbors.columns = ['target', 'importance']
        neighbors = neighbors.reset_index()
    
    neighbors.columns = ['TF', 'target', 'importance']
    neighbors = neighbors[neighbors['importance'] > 0]
    neighbors = neighbors.sort_values(by='importance', ascending=False)
    neighbors = neighbors.reset_index(drop=True)
    
    regulons = modules_from_adjacencies(
        adjacencies=neighbors,
        ex_mtx=adata.to_df(),
        thresholds=thresholds,
        top_n_targets=top_n_targets,
        top_n_regulators=top_n_regulators,
        min_genes=min_genes,
        rho_dichotomize=False,
        )
    
    for idx in range(len(regulons)):
        gene2weight = dict(regulons[idx].gene2weight)
        gene2weight[regulons[idx].transcription_factor] = regulons[idx].weights[1]
        regulons[idx] = regulons[idx].copy(gene2weight=gene2weight)
    
    if motif_annotations_fname is not None and db_fnames is not None:
        def name(fname):
            return os.path.splitext(os.path.basename(fname))[0]
        dbs = [RankingDatabase(fname=fname, name=name(fname)) for fname in db_fnames]
        
        df = prune2df(dbs, regulons, motif_annotations_fname)
        
        regulons = df2regulons(df)
    
    
    if key_added is None:
        key_added = 'regulons'
    
    adata.uns[key_added] = {}
    
    regulons_dict = adata.uns[key_added]
    
    regulons_dict['regulons'] = dump(regulons, default_flow_style=False, Dumper=Dumper)
    
    regulons_dict['params'] = {}
    regulons_dict['params']['tf_names'] = tf_names
    regulons_dict['params']['thresholds'] = str(thresholds)
    regulons_dict['params']['top_n_targets'] = str(top_n_targets)
    regulons_dict['params']['top_n_regulators'] = str(top_n_regulators)
    regulons_dict['params']['min_genes'] = min_genes
    
    return adata if copy else None


def aucell(
        adata: AnnData,
        auc_threshold: float = 0.05,
        noweights: bool = False,
        normalize: bool = False,
        random_state: int = 0,
        num_workers: int = 1,
        key: Optional[str] = None,
        key_added: Optional[str] = None,
        copy: bool = False,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    
    if key is None:
        key = 'regulons'
    
    if key not in adata.uns:
        raise ValueError(f'Did not find .uns["{key}"].')
    
    
    regulons = load(adata.uns[key]['regulons'], Loader=Loader)
    
    auc_mtx = pyscenic_aucell(
        exp_mtx=adata.to_df(),
        signatures=regulons,
        auc_threshold=auc_threshold,
        noweights=noweights,
        normalize=normalize,
        seed=random_state,
        num_workers=num_workers,
        )
    
    
    if key_added is None:
        key_added = 'aucell'
    
    adata.uns[key_added] = {}
    
    aucell_dict = adata.uns[key_added]
    
    aucell_dict['params'] = {}
    aucell_dict['params']['auc_threshold'] = auc_threshold
    aucell_dict['params']['noweights'] = noweights
    aucell_dict['params']['normalize'] = normalize
    aucell_dict['params']['random_state'] = random_state
    
    adata.obsm[key_added] = auc_mtx.loc[adata.obs_names,:]
    
    return adata if copy else None




















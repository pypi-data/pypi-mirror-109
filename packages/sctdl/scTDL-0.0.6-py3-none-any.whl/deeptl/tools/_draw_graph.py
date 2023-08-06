# -*- coding: utf-8 -*-

from typing import Optional

import numpy as np
import pandas as pd
import scipy
import scanpy as sc
from anndata import AnnData

from scanpy.tl._draw_graph import _Layout

from ._tsnep import tsne_p


def draw_graph_tsne_p(
        adata: AnnData,
        no_dims: int = 2,
        jitter: float = 1.5,
        max_iter: int = 300,
        n_neighbors: int = 15,
        layout: _Layout = 'fa',
        jitter_init_pos: Optional[float] = 4,
        max_iter_init_pos: Optional[int] = 300,
        random_state: int = 0,
        copy: bool = False,
        **kwds,
        ) -> Optional[AnnData]:
    
    adata = adata.copy() if copy else adata
    
    init_pos = None
    
    if jitter_init_pos is not None:
        init_pos = 'X_tsne_init_pos'
        tsne_p(
            adata,
            no_dims=2,
            jitter=jitter_init_pos,
            max_iter=max_iter_init_pos,
            random_state=random_state,
            )
        adata.uns['tsne_init_pos'] = adata.uns['tsne']
        del adata.uns['tsne']
        adata.obsm['X_tsne_init_pos'] = adata.obsm['X_tsne']
        del adata.obsm['X_tsne']
    
    tsne_p(
        adata,
        no_dims=no_dims,
        jitter=jitter,
        max_iter=max_iter,
        random_state=random_state,
        )
    
    sc.pp.neighbors(
        adata,
        n_neighbors=n_neighbors,
        n_pcs=None,
        use_rep='X_tsne',
        knn=True,
        random_state=random_state,
        method='gauss',
        )
    
    sc.tl.draw_graph(
        adata,
        layout=layout,
        init_pos=init_pos,
        root=None,
        random_state=random_state,
        **kwds,
        )
    
    return adata if copy else None




















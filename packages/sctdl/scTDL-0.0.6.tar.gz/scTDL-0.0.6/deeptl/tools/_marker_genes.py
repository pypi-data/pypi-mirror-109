# -*- coding: utf-8 -*-

import collections.abc as cabc
from typing import Union, Dict, Optional
from anndata import AnnData

from scanpy import logging as logg


def marker_gene_overlap_dict(
        adata: AnnData,
        reference_markers: Union[Dict[str, set], Dict[str, list]],
        *,
        key: str = 'rank_genes_groups',
        top_n_markers: Optional[int] = None,
        adj_pval_threshold: Optional[float] = None,
        key_added: str = 'marker_gene_overlap_dict',
        inplace: bool = False,
        ):
    
    # Test user inputs
    if key not in adata.uns:
        raise ValueError(
            'Could not find marker gene data. '
            'Please run `sc.tl.rank_genes_groups()` first.'
        )
    
    if not all(isinstance(val, cabc.Set) for val in reference_markers.values()):
        try:
            reference_markers = {
                key: set(val) for key, val in reference_markers.items()
            }
        except Exception:
            raise ValueError(
                'Please ensure that `reference_markers` contains '
                'sets or lists of markers as values.'
            )
    
    if adj_pval_threshold is not None:
        if 'pvals_adj' not in adata.uns[key]:
            raise ValueError(
                'Could not find adjusted p-value data. '
                'Please run `sc.tl.rank_genes_groups()` with a '
                'method that outputs adjusted p-values.'
            )

        if adj_pval_threshold < 0:
            logg.warning(
                '`adj_pval_threshold` was set below 0. Threshold will be set to 0.'
            )
            adj_pval_threshold = 0
        elif adj_pval_threshold > 1:
            logg.warning(
                '`adj_pval_threshold` was set above 1. Threshold will be set to 1.'
            )
            adj_pval_threshold = 1

        if top_n_markers is not None:
            logg.warning(
                'Both `adj_pval_threshold` and `top_n_markers` is set. '
                '`adj_pval_threshold` will be ignored.'
            )
    
    if top_n_markers is not None and top_n_markers < 1:
        logg.warning(
            '`top_n_markers` was set below 1. `top_n_markers` will be set to 1.'
        )
        top_n_markers = 1
    
    # Get data-derived marker genes in a dictionary of sets
    data_markers = dict()
    cluster_ids = adata.uns[key]['names'].dtype.names

    for group in cluster_ids:
        if top_n_markers is not None:
            n_genes = min(top_n_markers, adata.uns[key]['names'].shape[0])
            data_markers[group] = set(adata.uns[key]['names'][group][:n_genes])
        elif adj_pval_threshold is not None:
            n_genes = (adata.uns[key]['pvals_adj'][group] < adj_pval_threshold).sum()
            data_markers[group] = set(adata.uns[key]['names'][group][:n_genes])
            if n_genes == 0:
                logg.warning(
                    'No marker genes passed the significance threshold of '
                    f'{adj_pval_threshold} for cluster {group!r}.'
                )
        # Use top 100 markers as default if top_n_markers = None
        else:
            data_markers[group] = set(adata.uns[key]['names'][group][:100])
    
    marker_matching_dict = dict()
    
    for group in cluster_ids:
        marker_matching_dict[group] = dict()
        for key, val in reference_markers.items():
            intersection = data_markers[group] & val
            if len(intersection):
                marker_matching_dict[group][key] = intersection
    
    # Store the results
    if inplace:
        adata.uns[key_added] = marker_matching_dict
        logg.hint(f'added\n    {key_added!r}, marker overlap scores (adata.uns)')
    else:
        return marker_matching_dict
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


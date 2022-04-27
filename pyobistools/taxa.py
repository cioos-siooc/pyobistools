#!/usr/bin/env python
# coding=utf-8

import typing as t

import pyworms
import pandas as pd

from pyobistools.utils import removesuffix


STANDARD_SPECIES_COLUMNS = [
    'taxon_id', 'url', 'scientificname', 'authority', 'status', 'unacceptreason',
    'taxon_rank_id', 'rank', 'valid_taxon_id', 'valid_name', 'valid_authority',
    'parent_name_usage_id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus',
    'citation', 'lsid', 'is_marine', 'is_brackish', 'is_fresh_water', 'is_terrestrial',
    'is_extinct', 'match_type', 'modified', 'input_name'
]


def remove_suffix(name: str) -> str:
    suffixes = [
        ' sp.',
        ' spp.',
        ' sp',
        ' spp',
    ]
    for suf in suffixes:
        if name.endswith(suf):
            return removesuffix(name, suf)

    # If no suffix was found return the original name
    # with whitespace removed
    return name.strip()


def add_suffix(name: str) -> t.List[str]:
    """
    Adds suffixes to a name for searching ITIS
    """
    suffixes = [
        ' sp.',
        ' spp.',
        ' sp',
        ' spp',
    ]
    for suf in suffixes:
        if name.endswith(suf):
            # Strip off any existing suffixes from the name
            # and break out
            name = removesuffix(name, suf)
            break

    # Return a name for each suffix with whitespace remvoed
    return [ name.strip() + s for s in suffixes ]


def search_worms(names: t.List[str],
                 worms_kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Searches WoRMS for records based on a list of scientific names and returns
    a standardized pandas DataFrame representing the results

    Args:
        names (t.List[str]): List of scientific names to match

    Returns:
        pd.DataFrame: Species records
    """
    # WoRMS doesn't like suffixes so remove them
    suffixless_names = [ remove_suffix(s) for s in names ]

    results = pyworms.aphiaRecordsByMatchNames(
        suffixless_names,
        **worms_kwargs
    )

    rows = []
    for input_idx, name_results in enumerate(results):

        # Carry through the input name for the output DataFrame
        input_name = names[input_idx]

        # To track the results that are not matched, add a blank
        # row to be included in the resulting dataframe
        if not name_results:
            # Just carry through the input name
            rows.append({'input_name': input_name})

        for individual_result in name_results:
            # Carry through the input name
            individual_result['input_name'] = input_name
            rows.append(individual_result)

    # Now standardize the columns
    results = pd.DataFrame(rows)
    results = results.rename(columns={
        'AphiaID': 'taxon_id',
        'valid_AphiaID': 'valid_taxon_id',
        'taxonRankID': 'taxon_rank_id',
        'isExtinct': 'is_extinct',
        'parentNameUsageID': 'parent_name_usage_id',
        'isFreshwater': 'is_fresh_water',
        'isTerrestrial': 'is_terrestrial',
        'isMarine': 'is_marine',
        'isBrackish': 'is_brackish',
    })
    return results


def search_itis(names: t.List[str],
                itis_kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Searches ITIS for records based on a list of scientific names and returns
    a standardized pandas DataFrame representing the results

    Args:
        names (t.List[str]): List of scientific names to match

    Returns:
        pd.DataFrame: Species records
    """
    # ITIS wants suffixes?
    suffix_names = [ add_suffix(s) for s in names ]  # noqa

    # TODO: Hit ITIS API to return results

    # This is a placeholder for now, we don't actually hit ITIS at all
    results = pd.DataFrame(columns=STANDARD_SPECIES_COLUMNS)
    for n in names:
        results.append({'input_name': n})

    results = results.rename(columns={
        'tsn': 'taxon_id',
        'combinedName': 'valid_name',
    })

    # Add LSID urn
    results['lsid'] = results.apply(lambda x: "urn:lsid:itis.gov:itis_tsn:" + x.taxon_id)
    results['valid_taxon_id'] = results.taxon_id.copy()

    return results


def match_taxa(names: t.List[str],
               worms_kwargs: t.Dict[str, t.Any] = {},
               itis_kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Match a list of scientific names with WoRMS and ITIS and return the resulting
    record information in a DataFrame. Tries WoRMS first and only hits ITIS if
    nothing is found.

    Args:
        names (t.List[str]): List of scientific names to match
        worms_kwargs (t.Dict[str, t.Any]): keyword arguments to pass to pyworm's
            "aphiaRecordsByMatchNames" function
        itis_kwargs (t.Dict[str, t.Any]): keyword arguments to pass to ITIS
    Returns:
        pd.DataFrame: Species records
    """
    # Accept inputs that are strings (single species)
    if isinstance(names, str):
        names = [names]

    results = search_worms(names, worms_kwargs)
    if results.empty:
        results = search_itis(names, itis_kwargs)

    return results

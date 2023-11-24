#!/usr/bin/env python
# coding=utf-8

import typing as t
from functools import partial

import numpy as np
import pandas as pd
import pyworms
import requests

from pyobistools.utils import removesuffix

from pyobistools.validation import check_scientificname_and_ids as check_names


STANDARD_SPECIES_COLUMNS = {
    'taxon_id': np.nan,
    'url': '',
    'scientificname': '',
    'authority': '',
    'status': '',
    'unacceptreason': '',
    'taxon_rank_id': np.nan,
    'rank': '',
    'valid_taxon_id': np.nan,
    'valid_name': '',
    'valid_authority': '',
    'parent_name_usage_id': np.nan,
    'kingdom': '',
    'phylum': '',
    'class': '',
    'order': '',
    'family': '',
    'genus': '',
    'citation': '',
    'lsid': '',
    'is_marine': False,
    'is_brackish': False,
    'is_fresh_water': False,
    'is_terrestrial': False,
    'is_extinct': False,
    'match_type': '',
    'modified': '',
    'matched': False,
    'match_input': '',
    'match_from': '',
}


def _standardize_types(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if c in STANDARD_SPECIES_COLUMNS:
            if isinstance(STANDARD_SPECIES_COLUMNS[c], bool):
                df[c] = df[c].astype(bool)
            elif isinstance(STANDARD_SPECIES_COLUMNS[c], str):
                df[c] = df[c].astype(str)
            elif np.isnan(STANDARD_SPECIES_COLUMNS[c]):
                df[c] = pd.to_numeric(df[c])
    return df


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
    return [name.strip() + s for s in suffixes]


def match_taxa(names, ask=True, itis_usage=False):
    """
    Wrap the existing functionality in validation in the expected name for this function as per R's iobis/obistools.

    @param names    List of scientific names to check against
    @param ask      Do we ask the user to resolve multi-match or ambiguous names?
    @param itis_usage   Pass through the ITIS check setting for the client function to handle

    @return structure with appended lsids where WoRMS (or ITIS can resolve them)
    """

    return check_names.check_scientificname_and_ids(names, value='names', itis_usage=itis_usage)


def search_worms(names: t.List[str],
                 kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Searches WoRMS for records based on a list of scientific names and returns
    a standardized pandas DataFrame representing the results

    Args:
        names (t.List[str]): List of scientific names to match

    Returns:
        pd.DataFrame: Species records
    """
    # WoRMS doesn't like suffixes so remove them
    suffixless_names = [remove_suffix(s) for s in names]

    # Renames from pyworks output to the standard columns
    renames = {
        'AphiaID': 'taxon_id',
        'valid_AphiaID': 'valid_taxon_id',
        'taxonRankID': 'taxon_rank_id',
        'isExtinct': 'is_extinct',
        'parentNameUsageID': 'parent_name_usage_id',
        'isFreshwater': 'is_fresh_water',
        'isTerrestrial': 'is_terrestrial',
        'isMarine': 'is_marine',
        'isBrackish': 'is_brackish',
    }

    results = pyworms.aphiaRecordsByMatchNames(
        suffixless_names,
        **kwargs
    )

    rows = []
    for input_idx, name_results in enumerate(results):

        # Carry through the input name for the output DataFrame
        match_input = names[input_idx]

        # Track rows which did not return any data
        if not name_results:
            rows.append({'match_input': match_input, 'matched': False})

        for row in name_results:
            for k, v in renames.items():
                if k in row:
                    row[v] = row.pop(k)
            row.update({
                'match_input': match_input,
                'matched': True
            })
            rows.append(row)

    # Now standardize the columns
    for r in rows:
        # Fill in columns that don't exist
        r.update({
            k: v for k, v in STANDARD_SPECIES_COLUMNS.items()
            if k not in r
        })

    results = pd.DataFrame(rows)
    results['match_from'] = 'worms'
    results = _standardize_types(results)
    return results


def search_itis(names: t.List[str],
                kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Searches ITIS for records based on a list of scientific names and returns
    a standardized pandas DataFrame representing the results

    Args:
        names (t.List[str]): List of scientific names to match

    Returns:
        pd.DataFrame: Species records
    """
    # ITIS wants suffixes?
    suffix_names = [add_suffix(s) for s in names]  # noqa

    # TODO: Hit ITIS API to return results
    # renames = {
    #     'tsn': 'taxon_id',
    #     'combinedName': 'valid_name',
    # }

    # This is a placeholder for now, we don't actually hit ITIS at all
    rows = []
    for n in names:
        rows.append({'match_input': n, 'matched': False})

    # Now standardize the columns
    for r in rows:
        # Fill in columns that don't exist
        r.update({
            k: v for k, v in STANDARD_SPECIES_COLUMNS.items()
            if k not in r
        })

    # Standardize the OBIS return data format
    results = pd.DataFrame(rows)

    # Set the lsid when a taxon_id is defined
    results.loc[results.taxon_id.notna(), 'lsid'] = results.apply(
        lambda x: "urn:lsid:itis.gov:itis_tsn:" + str(x.taxon_id), axis=1
    )
    results['valid_taxon_id'] = results.taxon_id.copy()
    results['match_from'] = 'itis'
    results = _standardize_types(results)
    return results


def search_obis(names: t.List[str],
                kwargs: t.Dict[str, t.Any] = {}) -> pd.DataFrame:
    """
    Searches OBIS for records based on a list of scientific names and returns
    a standardized pandas DataFrame representing the results

    Args:
        names (t.List[str]): List of scientific names to match

    Returns:
        pd.DataFrame: Species records
    """
    obis_api = kwargs.pop('url', 'https://api.obis.org/v3/')
    http_headers = {
        'content-type': 'application/json; charset=utf-8'
    }

    renames = {
        'taxonRank': 'rank',
        'scientificName': 'scientificname',
        'scientificNameAuthorship': 'authority',
        'taxonID': 'taxon_id',
        'taxonomicStatus': 'status',
        'acceptedNameUsage': 'valid_name',
    }

    # WoRMS doesn't like suffixes so remove them
    suffixless_names = [remove_suffix(s) for s in names]

    rows = []
    for name in suffixless_names:

        r = requests.get(
            f'{obis_api}taxon/{name}',
            headers=http_headers
        )
        try:
            r.raise_for_status()
        except BaseException:
            # Error, fill with empty dataframe
            rows.append({'match_input': name, 'matched': False})
        else:
            results = r.json()['results']
            if not results:
                rows.append({'match_input': name, 'matched': False})
            for row in results:
                for k, v in renames.items():
                    if k in row:
                        row[v] = row.pop(k)
                row.update({
                    'match_input': name,
                    'matched': True
                })
                rows.append(row)

    # Now standardize the columns
    for r in rows:
        # Fill in columns that don't exist
        r.update({
            k: v for k, v in STANDARD_SPECIES_COLUMNS.items()
            if k not in r
        })

    # Standardize the OBIS return data format
    results = pd.DataFrame(rows)
    results['match_from'] = 'obis'
    results = _standardize_types(results)

    return results


def search(names: t.List[str],
           worms_kwargs: t.Dict[str, t.Any] = {},
           itis_kwargs: t.Dict[str, t.Any] = {},
           obis_kwargs: t.Dict[str, t.Any] = {},
           order: t.List[str] = None,
           quick: bool = False) -> pd.DataFrame:
    """
    Search a list of scientific names in WoRMS, ITIS and OBIS and return the resulting
    record information in a DataFrame. Tries WoRMS first, ITIS second, and OBIS third unless
    another order is specificed with the "order" parameter.

    Args:
        names (t.List[str]): List of scientific names to match
        worms_kwargs (t.Dict[str, t.Any]): keyword arguments to pass to pyworm's
            "aphiaRecordsByMatchNames" function
        itis_kwargs (t.Dict[str, t.Any]): keyword arguments to pass to ITIS
        obis_kwargs (t.Dict[str, t.Any]): keyword arguments to pass to OBIS
        order (t.List[str]): order which to to check external services, defaults to
            ['worms', 'idis', 'obis']. To only check a subset of sources set to a smaller list.
        quick (bool): Stop when the first match is found and return rather than query additional
            services
    Returns:
        pd.DataFrame: Species records
    """
    # Accept inputs that are strings (single species)
    if isinstance(names, str):
        names = [names]

    if order is None:
        order = ['worms', 'itis', 'obis']

    # A mapping between the "order" and the function to call
    # for each one
    funcs = {
        'worms': partial(search_worms, **worms_kwargs),
        'itis': partial(search_itis, **itis_kwargs),
        'obis': partial(search_obis, **obis_kwargs),
    }

    # Call individual search functions until one doesn't return empty
    all_results = []

    for o in order:
        if o not in funcs:
            continue

        results = funcs[o](names)
        all_results.append(results)

        # Break if we want to stop searching on first match
        if results.matched.any() and quick is True:
            break

    # Return all results subset by the standard columns
    results = pd.concat(all_results, ignore_index=True)
    results = results[STANDARD_SPECIES_COLUMNS.keys()]
    return results

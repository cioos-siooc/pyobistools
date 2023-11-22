
import numpy as np

from pyobistools import taxa


def test_match_quick():
    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ],
        quick=True
    )
    assert len(results) == 2


def test_match_all_with_details():
    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ]
    )
    assert len(results) == 6

    # No match for first result, but the standard columns are still returned
    notaspecies = results.iloc[0]
    assert notaspecies.match_input == 'thisisntaspecies'
    assert not notaspecies['url']
    assert not notaspecies['scientificname']
    assert not notaspecies['authority']
    assert not notaspecies['status']
    assert not notaspecies['unacceptreason']
    assert not notaspecies['rank']
    assert not notaspecies['valid_name']
    assert not notaspecies['valid_authority']
    assert not notaspecies['kingdom']
    assert not notaspecies['phylum']
    assert not notaspecies['class']
    assert not notaspecies['order']
    assert not notaspecies['family']
    assert not notaspecies['genus']
    assert not notaspecies['citation']
    assert not notaspecies['lsid']
    assert not notaspecies['is_marine']
    assert not notaspecies['is_brackish']
    assert not notaspecies['is_fresh_water']
    assert not notaspecies['is_terrestrial']
    assert not notaspecies['is_extinct']
    assert np.isnan(notaspecies['taxon_id'])
    assert np.isnan(notaspecies['taxon_rank_id'])
    assert np.isnan(notaspecies['valid_taxon_id'])
    assert np.isnan(notaspecies['parent_name_usage_id'])
    assert not notaspecies['match_type']
    assert not notaspecies['modified']

    # Found a match for second result
    mola = results.iloc[1]
    assert mola['match_input'] == 'Mola mola'
    assert mola['taxon_id'] == 127405.0
    assert mola['url'] == 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=127405'
    assert mola['scientificname'] == 'Mola mola'
    assert mola['authority'] == '(Linnaeus, 1758)'
    assert mola['status'] == 'accepted'
    assert mola['taxon_rank_id'] == 220.0
    assert mola['rank'] == 'Species'
    assert mola['valid_taxon_id'] == 127405.0
    assert mola['valid_name'] == 'Mola mola'
    assert mola['valid_authority'] == '(Linnaeus, 1758)'
    assert mola['parent_name_usage_id'] == 126233.0
    assert mola['kingdom'] == 'Animalia'
    assert mola['phylum'] == 'Chordata'
    # actinopteri became the superclass recently, Dec 2021, class is now Teleostei
    # assert mola['class'] == 'Actinopteri'
    # do we assert superclass?
    # assert mola['superclass'] == 'Actinopteri'
    assert mola['class'] == 'Teleostei'
    assert mola['order'] == 'Tetraodontiformes'
    assert mola['family'] == 'Molidae'
    assert mola['genus'] == 'Mola'
    # Can't assert citation this way, today's date is part of the return string from WoRMS.
    # assert mola['citation'] == 'Froese, R. and D. Pauly. Editors. (2022). FishBase. Mola mola (Linnaeus, 1758). Accessed through: World Register of Marine Species at: https://www.marinespecies.org/aphia.php?p=taxdetails&id=127405 on 2022-04-27'
    assert mola['lsid'] == 'urn:lsid:marinespecies.org:taxname:127405'
    assert mola['is_marine']
    assert not mola['is_brackish']
    assert not mola['is_fresh_water']
    assert not mola['is_terrestrial']
    assert not mola['is_extinct']
    assert mola['match_type'] == 'exact'
    assert mola['modified'] == '2021-12-07T22:23:16.560Z'
    assert mola['unacceptreason'] == 'None'


def test_add_suffix():
    expected = [
        'hello sp.',
        'hello spp.',
        'hello sp',
        'hello spp',
    ]
    assert taxa.add_suffix('hello') == expected
    assert taxa.add_suffix('hello    ') == expected
    assert taxa.add_suffix('    hello') == expected
    assert taxa.add_suffix('hello sp.') == expected
    assert taxa.add_suffix('hello spp.') == expected
    assert taxa.add_suffix('hello sp') == expected
    assert taxa.add_suffix('hello spp') == expected

    expected = [
        'spaces and other things sp.',
        'spaces and other things spp.',
        'spaces and other things sp',
        'spaces and other things spp',
    ]
    assert taxa.add_suffix('spaces and other things') == expected
    assert taxa.add_suffix('spaces and other things    ') == expected
    assert taxa.add_suffix('    spaces and other things') == expected
    assert taxa.add_suffix('spaces and other things sp.') == expected
    assert taxa.add_suffix('spaces and other things spp.') == expected
    assert taxa.add_suffix('spaces and other things sp') == expected
    assert taxa.add_suffix('spaces and other things spp') == expected


def test_remove_suffix():
    expected = 'hello'
    assert taxa.remove_suffix('hello') == expected
    assert taxa.remove_suffix('hello    ') == expected
    assert taxa.remove_suffix('    hello') == expected
    assert taxa.remove_suffix('hello sp.') == expected
    assert taxa.remove_suffix('hello spp.') == expected
    assert taxa.remove_suffix('hello sp') == expected
    assert taxa.remove_suffix('hello spp') == expected

    expected = 'spaces and other things'
    assert taxa.remove_suffix('spaces and other things') == expected
    assert taxa.remove_suffix('spaces and other things    ') == expected
    assert taxa.remove_suffix('    spaces and other things') == expected
    assert taxa.remove_suffix('spaces and other things sp.') == expected
    assert taxa.remove_suffix('spaces and other things spp.') == expected
    assert taxa.remove_suffix('spaces and other things sp') == expected
    assert taxa.remove_suffix('spaces and other things spp') == expected


def test_search_worms():
    results = taxa.search_worms([
        'thisisntaspecies',
        'Mola mola'
    ])
    assert len(results) == 2

    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ],
        order=['worms']
    )
    assert len(results) == 2


def test_search_itis():
    results = taxa.search_itis([
        'thisisntaspecies',
        'Mola mola'
    ])
    assert len(results) == 2

    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ],
        order=['itis']
    )
    assert len(results) == 2


def test_search_obis():
    results = taxa.search_obis([
        'thisisntaspecies',
        'Mola mola'
    ])
    assert len(results) == 2

    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ],
        order=['obis']
    )
    assert len(results) == 2


def test_search_two():
    results = taxa.search_obis([
        'thisisntaspecies',
        'Mola mola'
    ])
    assert len(results) == 2

    results = taxa.search([
            'thisisntaspecies',
            'Mola mola'
        ],
        order=['worms', 'obis']
    )
    assert len(results) == 4

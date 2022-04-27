
import numpy as np

from pyobistools.taxa import match_taxa, remove_suffix, add_suffix


def test_match_single_name():
    results = match_taxa([
        'thisisntaspecies',
        'Mola mola'
    ])
    assert len(results) == 2

    # No match for first result, but the standard columns are still returned
    notaspecies = results.iloc[0]
    assert notaspecies.input_name == 'thisisntaspecies'
    assert np.isnan(notaspecies['taxon_id'])
    assert np.isnan(notaspecies['url'])
    assert np.isnan(notaspecies['scientificname'])
    assert np.isnan(notaspecies['authority'])
    assert np.isnan(notaspecies['status'])
    assert np.isnan(notaspecies['unacceptreason'])
    assert np.isnan(notaspecies['taxon_rank_id'])
    assert np.isnan(notaspecies['rank'])
    assert np.isnan(notaspecies['valid_taxon_id'])
    assert np.isnan(notaspecies['valid_name'])
    assert np.isnan(notaspecies['valid_authority'])
    assert np.isnan(notaspecies['parent_name_usage_id'])
    assert np.isnan(notaspecies['kingdom'])
    assert np.isnan(notaspecies['phylum'])
    assert np.isnan(notaspecies['class'])
    assert np.isnan(notaspecies['order'])
    assert np.isnan(notaspecies['family'])
    assert np.isnan(notaspecies['genus'])
    assert np.isnan(notaspecies['citation'])
    assert np.isnan(notaspecies['lsid'])
    assert np.isnan(notaspecies['is_marine'])
    assert np.isnan(notaspecies['is_brackish'])
    assert np.isnan(notaspecies['is_fresh_water'])
    assert np.isnan(notaspecies['is_terrestrial'])
    assert np.isnan(notaspecies['is_extinct'])
    assert np.isnan(notaspecies['match_type'])
    assert np.isnan(notaspecies['modified'])

    # Found a match for second result
    mola = results.iloc[1]
    assert mola['input_name'] == 'Mola mola'
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
    assert mola['class'] == 'Actinopteri'
    assert mola['order'] == 'Tetraodontiformes'
    assert mola['family'] == 'Molidae'
    assert mola['genus'] == 'Mola'
    assert mola['citation'] == 'Froese, R. and D. Pauly. Editors. (2022). FishBase. Mola mola (Linnaeus, 1758). Accessed through: World Register of Marine Species at: https://www.marinespecies.org/aphia.php?p=taxdetails&id=127405 on 2022-04-27'
    assert mola['lsid'] == 'urn:lsid:marinespecies.org:taxname:127405'
    assert mola['is_marine'] == 1.0
    assert mola['is_brackish'] == 0.0
    assert mola['is_fresh_water'] == 0.0
    assert mola['is_terrestrial'] == 0.0
    assert mola['match_type'] == 'exact'
    assert mola['modified'] == '2021-12-07T22:23:16.560Z'
    assert np.isnan(mola['unacceptreason'])
    assert np.isnan(mola['is_extinct'])


def test_add_suffix():
    expected = [
        'hello sp.',
        'hello spp.',
        'hello sp',
        'hello spp',
    ]
    assert add_suffix('hello') == expected
    assert add_suffix('hello    ') == expected
    assert add_suffix('    hello') == expected
    assert add_suffix('hello sp.') == expected
    assert add_suffix('hello spp.') == expected
    assert add_suffix('hello sp') == expected
    assert add_suffix('hello spp') == expected

    expected = [
        'spaces and other things sp.',
        'spaces and other things spp.',
        'spaces and other things sp',
        'spaces and other things spp',
    ]
    assert add_suffix('spaces and other things') == expected
    assert add_suffix('spaces and other things    ') == expected
    assert add_suffix('    spaces and other things') == expected
    assert add_suffix('spaces and other things sp.') == expected
    assert add_suffix('spaces and other things spp.') == expected
    assert add_suffix('spaces and other things sp') == expected
    assert add_suffix('spaces and other things spp') == expected


def test_remove_suffix():
    expected = 'hello'
    assert remove_suffix('hello') == expected
    assert remove_suffix('hello    ') == expected
    assert remove_suffix('    hello') == expected
    assert remove_suffix('hello sp.') == expected
    assert remove_suffix('hello spp.') == expected
    assert remove_suffix('hello sp') == expected
    assert remove_suffix('hello spp') == expected

    expected = 'spaces and other things'
    assert remove_suffix('spaces and other things') == expected
    assert remove_suffix('spaces and other things    ') == expected
    assert remove_suffix('    spaces and other things') == expected
    assert remove_suffix('spaces and other things sp.') == expected
    assert remove_suffix('spaces and other things spp.') == expected
    assert remove_suffix('spaces and other things sp') == expected
    assert remove_suffix('spaces and other things spp') == expected

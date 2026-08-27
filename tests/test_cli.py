from plummet import cli


def test_generate_permutations():
    mock_impls = {
        'bianchini': {'enabled': False},
        'huyghens': {'enabled': True, 'client': True, 'server': False},
        'jang': {'enabled': True, 'client': True, 'server': True}
    }
    expected = [
        {'server': 'jang', 'client': 'huyghens'},
        {'server': 'jang', 'client': 'jang'}
    ]
    actual = cli.generate_permutations(mock_impls)
    assert expected == actual


def test_generate_permutations_focus():
    mock_impls = {
        'bianchini': {'enabled': True, 'client': True, 'server': True},
        'huyghens': {'enabled': True, 'client': True, 'server': False},
        'jang': {'enabled': True, 'client': True, 'server': True}
    }
    actual = cli.generate_permutations(mock_impls, focus='huyghens')
    assert {p['server'] for p in actual} <= {'bianchini', 'jang'}
    assert all(p['client'] == 'huyghens' for p in actual)
    assert len(actual) == 2


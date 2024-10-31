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

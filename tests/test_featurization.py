from package.featurization import extract_features, tokenize


def test_tokenize():
    assert tokenize("foo BAR BAR foo Foo bar") == {"foo", "bar"}
    assert tokenize("") == {""}
    assert tokenize("foo. Foo bar") == {"foo.", "foo", "bar"}


def test_extract_features():
    assert extract_features("foo bar") == [
        1,
        0,
        0,
        0,
        0,
    ]

    assert extract_features("foo bar") == [
        1,
        0,
        0,
        0,
        0,
    ]

    assert extract_features("foo bar") == [
        1,
        0,
        0,
        0,
        0,
    ]

    assert extract_features("foo bar") == [
        1,
        0,
        0,
        0,
        0,
    ]

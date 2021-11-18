from package.featurization import extract_features, tokenize


def test_tokenize():
    assert tokenize("foo BAR BAR foo Foo bar") == {"foo", "bar"}
    assert tokenize("") == set()
    assert tokenize("foo. Foo bar") == {"foo.", "foo", "bar"}


def test_extract_features():
    assert extract_features("Bigger Splash ist ein Gemälde von David Hockney") == [
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
    ]
    assert extract_features("Die Sopranos ist eine US-amerikanische Fernsehserie") == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert extract_features("Pretzel Logic ist das dritte Studioalbum der Band Steely Dan") == [
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
    ]
    assert extract_features("foo bar") == [0, 0, 0, 0, 0, 0, 0, 0, 0]

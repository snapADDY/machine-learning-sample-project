from package.classification import classify_text


def test_classify_text():
    prediction = classify_text("Bigger Splash ist ein Gemälde von David Hockney")
    assert prediction["label"] == "Gemälde"
    assert prediction["probability"] > 0.9

    prediction = classify_text("Die Sopranos ist eine US-amerikanische Fernsehserie")
    assert prediction["label"] == "Fernsehserie"
    assert prediction["probability"] > 0.9

    prediction = classify_text("Pretzel Logic ist das dritte Studioalbum der Band Steely Dan")
    assert prediction["label"] == "Musikalbum"
    assert prediction["probability"] > 0.9

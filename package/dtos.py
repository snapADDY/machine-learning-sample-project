from marshmallow import Schema
from marshmallow.fields import Float, String


class RequestDTO(Schema):
    text = String(
        required=True,
        metadata={
            "example": "Die Sopranos ist eine US-amerikanische Fernsehserie.",
            "description": "Text to classify.",
        },
    )


class ResponseDTO(Schema):
    label = String(
        required=True,
        metadata={
            "example": "Fernsehserie",
            "description": "Predicted category label,",
        },
    )

    probability = Float(
        required=True,
        metadata={
            "example": 0.99,
            "description": "Probability of the most likely label.",
        },
    )

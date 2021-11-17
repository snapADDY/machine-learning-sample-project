from marshmallow import Schema
from marshmallow.fields import Float, String


class RequestDTO(Schema):
    text = String(
        required=True,
        metadata={
            "example": "Die Sopranos ist eine US-amerikanische Fernsehserie.",
            "description": "German text to classify.",
        },
    )


class ResponseDTO(Schema):
    label = String(
        required=True,
        metadata={
            "example": "Fernsehserie",
            "description": "tba",
        },
    )

    probability = Float(
        required=True,
        metadata={
            "example": 0.99,
            "description": "tba",
        },
    )

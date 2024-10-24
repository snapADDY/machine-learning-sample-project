from marshmallow import Schema
from marshmallow.fields import Float, String


class RequestDTO(Schema):
    """DTO for the request body."""

    text = String(
        required=True,
        metadata={
            "example": "Die Sopranos ist eine US-amerikanische Fernsehserie.",
            "description": "Text to classify.",
        },
    )


class ResponseDTO(Schema):
    """DTO for the response body."""

    label = String(
        required=True,
        metadata={
            "example": "show",
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

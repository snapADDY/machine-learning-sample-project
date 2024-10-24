from marshmallow import Schema
from marshmallow.fields import String


class PostClassificationRequestDTO(Schema):
    """DTO for classification POST requests."""

    text = String(
        required=True,
        metadata={
            "example": "Die Sopranos ist eine US-amerikanische Fernsehserie.",
            "description": "Text to classify.",
        },
    )

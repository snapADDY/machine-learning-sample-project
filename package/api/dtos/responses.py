from marshmallow import Schema
from marshmallow.fields import Float, String


class PostClassificationResponseDTO(Schema):
    """DTO for classification POST responses."""

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

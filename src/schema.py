from pydantic import BaseModel, Field

class ConfidenceField(BaseModel):
    value: str | float | None = Field(default=None, description="The extracted data point")
    confidence: float = Field(
        default=0.0, 
        ge=0.0, le=1.0, 
        description="Confidence score (0.0 to 1.0) of the extraction"
    )

class ChangeOrderOutput(BaseModel):
    project_name: ConfidenceField = Field(default_factory=ConfidenceField)
    change_order_id: ConfidenceField = Field(default_factory=ConfidenceField)
    total_cost_impact: ConfidenceField = Field(default_factory=ConfidenceField)
    schedule_impact_days: ConfidenceField = Field(default_factory=ConfidenceField)
    description_of_change: ConfidenceField = Field(default_factory=ConfidenceField)
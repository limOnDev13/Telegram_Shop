"""The module responsible for the subscription channel scheme."""

from pydantic import BaseModel, Field


class ChannelToSubscribeSchema(BaseModel):
    """Channel to subscribe schema."""

    id: str = Field(..., description="Chat ID")
    title: str = Field(..., description="Chat name")
    url: str = Field(..., description="Chat utl")

    class Config:
        """Config class."""

        from_attributes = True

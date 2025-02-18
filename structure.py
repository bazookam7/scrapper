from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

class CardRates(BaseModel):
    currency: str = Field(description="The currency of the rates")
    TT_Buy: float = Field(description="The buy rate")
    TT_Sell: float = Field(description="The sell rate")

class CardRatesList(BaseModel):
    card_rates: List[CardRates] = Field(description="The list of card rates")





from datetime import date
from sqlalchemy import Column, Date, Float, Integer, String
from dao.data_source import DataSource
from dao.models.base_model import SQLBaseModel

class CardRatesDo(SQLBaseModel):
    __tablename__ = "card_rates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, nullable=False)
    reference_date = Column(Date, nullable=False)
    currency = Column(String, nullable=False)
    tt_buy = Column(Float, nullable=False)
    tt_sell = Column(Float, nullable=False)

    def __init__(self, company_name: str, reference_date: date, currency: str, tt_buy: float, tt_sell: float):
        super().__init__()
        self.company_name = company_name
        self.reference_date = reference_date
        self.currency = currency
        self.tt_buy = tt_buy
        self.tt_sell = tt_sell

    @classmethod
    def get_data_source(cls) -> DataSource:
        return DataSource.POSTGRES

from dao.models.no_sql.bse_company import BseCompany
from dao.query.mongo_query import MongoQuery


class BseCompanyQuery(MongoQuery):
    _collection_name="bse_company"
    _model_class=BseCompany

    
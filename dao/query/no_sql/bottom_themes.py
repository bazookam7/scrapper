from dao.query.mongo_query import MongoQuery
from dao.models.no_sql.bottom_themes import BottomThemes

class BottomThemesQuery(MongoQuery):
    _collection_name = "bottom_themes"
    _model_class = BottomThemes

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self

""" This module implement data entities functionality  """
import pandas as pd

from superwise.controller.base import BaseController
from superwise.controller.summary.entities_validator import EntitiesValidator
from superwise.controller.summary.summary import Summary
from superwise.models.data_entity import DataEntity
from superwise.models.data_entity import DataEntitySummary
from superwise.resources.supwewise_enums import CategoricalSecondaryType
from superwise.resources.supwewise_enums import FeatureType


class DataEntityController(BaseController):
    """ controller for Data entities  """

    def __init__(self, client):
        """
        constructer for DataEntityController class

        :param client:

        """
        super().__init__(client)
        self.path = "model/v1/data_entities"
        self.model_name = "DataEntity"
        self._entities_df = None
        self.data = None

    def create(self, name=None, type=None, is_dimension=None, role=None, feature_importance=None):
        """
        create data entity
        """

        params = locals()
        return self._dict_to_model(params)

    def update_summary(self, data_entity_id, summary):
        """
        update summary implementation
        """
        self.model = DataEntitySummary(data_entity_id, summary)
        self.model_name = "DataEntitySummary"
        self.create(self.model)

    def generate_summary(self, data_entities, task, data, is_return_model=True, **kwargs):
        """

        :param model: model of version
        :return: model of version
        """
        entities_df = DataEntity.list_to_df(data_entities)
        self.data = data
        self._entities_df = entities_df
        validator = EntitiesValidator(task, entities_df)
        validator.prepare(data)
        entities_df_summary = Summary(self._entities_df, self.data).generate()
        data_entities = DataEntity.df_to_list(entities_df_summary)
        return data_entities

        if len(model.data_entities) and isinstance(model.data_entities[0], DataEntity):
            model.data_entities = [m.get_properties() for m in model.data_entities]
        # return super().create(model, **kwargs)

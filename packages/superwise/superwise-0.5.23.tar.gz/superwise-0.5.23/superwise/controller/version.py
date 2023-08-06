""" This module implement version functionality  """
import time

from superwise.config import Config
from superwise.controller.base import BaseController
from superwise.controller.exceptions import SuperwiseValidationException
from superwise.models.data_entity import DataEntity


class VersionController(BaseController):
    """ Version api controller """

    def __init__(self, client):
        """
        Constructor of VersionController

        :param client: rest api client
        """
        super().__init__(client)
        self.path = "model/v1/versions"
        self.model_name = "Version"

    def create(self, model, is_return_model=True, **kwargs):
        """

        :param model: model of version
        :return: model of version
        """
        if len(model.data_entities) and isinstance(model.data_entities[0], DataEntity):
            model.data_entities = [m.get_properties() for m in model.data_entities]
        return super().create(model, **kwargs)

    def _dict(self, params, model_name=None):
        """

        :param params: dict
        :return: model of version
        """
        model_name = model_name or self.model_name

        model = super()._dict_to_model(params, model_name=model_name)
        print(model.get_properties())

        if model_name != "DataEntity" and len(model.data_entities) and isinstance(model.data_entities[0], DataEntity):
            model.data_entities = [m.get_properties() for m in model.data_entities]
        return model

    def get_data_entities(self, version_id):
        """

        :param version_id:
        :return: list of models of data entities
        """
        models = []
        url = self.build_url("{}/{}/data_entities".format(self.path, version_id))
        self.logger.info("CALL GET DATA ENTITIES {} ".format(url))
        r = self.client.get(url)
        entities_lst = self.parse_response(r, "DataEntity", is_return_model=False)
        entities_lst = [e["data_entity"] for e in entities_lst]
        for entity in entities_lst:
            models.append(self._dict_to_model(entity, "DataEntity"))
        return models

    def get_by_id(self, idx, is_pooling=False):
        """ get by id implementation as we need to implement pooling version"""
        if is_pooling:
            while True:
                time.sleep(Config.POOLING_INTERVAL_SEC)
                model = super().get_by_id(idx)
                status = model.status
                print("{" + status + "}")
                if status in ["SUMMARIZING", "CREATED"]:
                    self.logger.info("still summerizing the data, next pooling in %s sec", Config.POOLING_INTERVAL_SEC)
                    continue
                elif status == "SUMMARIZED":
                    self.logger.info("finished summerizing the version, return results")
                    return model
                elif status in ["VALIDATION_ERROR"]:
                    raise SuperwiseValidationException(model.get_properties())
                else:
                    raise Exception("unknown status %s", model.get_properties())
        else:
            return super().get_by_id(idx)

        ### activate

    def activate(self, version_id):
        url = "{}/{}".format(self.path, version_id)
        print(url)
        res = self.patch(url, {"status": "ACTIVATED"})
        print(res)
        return res

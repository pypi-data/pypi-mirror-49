# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Seattle crime."""

from datetime import datetime
from ._abstract_opendataset import AbstractOpenDataset
from .accessories._seattle_reported_crime_accessory import SeattleReportedCrimeAccessory
from azureml.core import Dataset
from typing import List, Optional


class SeattleReportedCrime(AbstractOpenDataset):
    """Seattle city crime class."""

    def __init__(
            self,
            start_date: datetime = SeattleReportedCrimeAccessory.default_start_date,
            end_date: datetime = SeattleReportedCrimeAccessory.default_end_date,
            cols: Optional[List[str]] = None,
            dataset: Dataset = None,
            enable_telemetry: bool = True):
        """
        Initializes an instance of the SeattleReportedCrime class.
        It can be initialized from parameters, or dataset alone, but can't from both.

        :param start_date: start date you'd like to query inclusively.
        :type start_date: datetime
        :param end_date: end date you'd like to query inclusively.
        :type end_date: datetime
        :param cols: a list of column names you'd like to retrieve. None will get all columns.
        :type cols: List[str]
        :param dataset: if it's not None, then this will override all the arguments previously.
        :type dataset: Dataset
        :param enable_telemetry: whether to enable telemetry, disabled for UT only.
        :type enable_telemetry: bool
        """
        worker = SeattleReportedCrimeAccessory(
            start_date=start_date,
            end_date=end_date,
            cols=cols,
            enable_telemetry=enable_telemetry)
        if dataset is not None:
            if start_date != SeattleReportedCrimeAccessory.default_start_date and \
                end_date != SeattleReportedCrimeAccessory.default_end_date and \
                    cols is not None:
                raise ValueError('With enable_telemetry excluded, it is invalid to set dataset and other parameters \
at the same time! Please use either of them.')
            worker.update_dataset(dataset, enable_telemetry=enable_telemetry)
            self.worker = worker
            Dataset.__init__(
                self,
                definition=dataset.get_definition(),
                workspace=dataset.workspace,
                name=dataset.name,
                id=dataset.id)
        else:
            AbstractOpenDataset.__init__(self, worker=worker)

    @staticmethod
    def get(dataset: Dataset, enable_telemetry: bool = True):
        """Get an instance of SeattleReportedCrime.

        :param dataset: input an instance of Dataset.
        :type end_date: Dataset.
        :param enable_telemetry: whether to enable telemetry, disabled for UT only.
        :type enable_telemetry: bool
        :return: an instance of SeattleReportedCrime.
        """
        sea = SeattleReportedCrime(dataset=dataset, enable_telemetry=enable_telemetry)
        sea._tags = dataset.tags
        if enable_telemetry:
            AbstractOpenDataset.log_get_operation(sea.worker)
        return sea

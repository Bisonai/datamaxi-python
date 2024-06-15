from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Google(API):
    """Client to fetch Google trend data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def keywords(self) -> List[str]:
        """Get Google trend supported keywords

        `GET /v1/google/keywords`

        <https://docs.datamaxi.finance/api/datasets/trend/google/keywords>

        Returns:
            List of supported Google trend keywords
        """
        url_path = "/v1/google/keywords"
        return self.query(url_path)

    @postprocess()
    def trend(self, keyword: str, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get Google trend for given keyword

        `GET /v1/google/trend`

        <https://docs.datamaxi.finance/api/datasets/trend/google/trend>

        Args:
            keyword (str): keyword to search for
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Google trend data
        """
        check_required_parameter(keyword, "keyword")
        params = {"keyword": keyword}
        return self.query("/v1/google/trend", params)

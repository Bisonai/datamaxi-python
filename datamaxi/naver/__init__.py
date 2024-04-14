from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import BASE_URL
from datamaxi.lib.utils import postprocess


class Naver(API):
    """Client to fetch Naver trend data from DataMaxi+ API."""

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
        """Get Naver trend supported keywords

        `GET /v1/naver/keywords`

        <https://docs.datamaxi.finance/naver/keywords>

        Returns:
            List of supported Naver trend keywords
        """
        url_path = "/v1/naver/keywords"
        return self.query(url_path)

    @postprocess()
    def trend(self, keyword: str, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get Naver trend for given keyword

        `GET /v1/naver/trend`

        <https://docs.neverest.finance/naver/trend>

        Args:
            keyword (str): keyword to search for
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Naver trend data
        """
        check_required_parameter(keyword, "keyword")
        params = {"keyword": keyword}
        return self.query("/v1/naver/trend", params)

"""Tests for the typed response models (#141).

TypedDicts are hint-only, so these assert the documented field sets (guarding
against transcription drift) and that the pandas=False return still matches
the typed shape at runtime.
"""

import re
import responses
import pandas as pd

from datamaxi import (
    CandleRow,
    CandleResponse,
    TickerData,
    TickerResponse,
    AnnouncementRow,
    TokenUpdateRow,
    WalletStatusRow,
    ForexRow,
    FundingRateRow,
    LatestFundingRate,
    PremiumRow,
    PremiumDetail,
    TelegramChannel,
    TelegramMessage,
    NaverTrendRow,
)
from datamaxi.resources.cex_candle import CexCandle
from datamaxi.resources.cex_ticker import CexTicker

BASE_URL = "https://api.datamaxiplus.com"


def test_candle_row_fields():
    assert set(CandleRow.__annotations__) == {"d", "o", "h", "l", "c", "v"}
    assert set(CandleResponse.__annotations__) == {"data"}


def test_ticker_data_fields():
    assert set(TickerData.__annotations__) == {
        "b",
        "d",
        "e",
        "hb",
        "la",
        "ld",
        "m",
        "p",
        "p24h",
        "q",
        "s",
        "ud",
        "v",
        "pc",
    }
    assert set(TickerResponse.__annotations__) == {"data"}


@responses.activate
def test_candle_pandas_false_matches_envelope_shape():
    payload = {
        "data": [{"d": "1700000000", "o": "1", "h": "2", "l": "1", "c": "2", "v": "9"}]
    }
    responses.add(
        responses.GET, re.compile(".*/api/v1/cex/candle.*"), json=payload, status=200
    )
    res = CexCandle(api_key="k", base_url=BASE_URL)(
        exchange="binance", market="spot", symbol="BTC-USDT", pandas=False
    )
    assert set(res.keys()) == {"data"}
    assert set(res["data"][0].keys()) == set(CandleRow.__annotations__)


def test_new_model_field_sets():
    assert set(AnnouncementRow.__annotations__) == {"c", "d", "e", "s", "t", "u"}
    assert set(TokenUpdateRow.__annotations__) == {"b", "d", "e", "m", "q", "t"}
    assert set(WalletStatusRow.__annotations__) == {
        "currency",
        "deposit_state",
        "deposit_message",
        "withdraw_state",
        "withdraw_message",
        "exchange",
        "network",
        "updated_at",
    }
    assert set(ForexRow.__annotations__) == {"d", "r", "s"}
    assert set(FundingRateRow.__annotations__) == {"d", "f"}
    assert set(LatestFundingRate.__annotations__) == {
        "b",
        "d",
        "e",
        "f",
        "i",
        "id",
        "p",
        "q",
        "s",
    }
    assert set(PremiumRow.__annotations__) == {
        "detail",
        "source_annualized_funding_rate",
        "target_annualized_funding_rate",
    }
    assert set(TelegramChannel.__annotations__) == {
        "category",
        "channelName",
        "channelTitle",
        "createdAt",
        "description",
        "link",
        "subscribers",
    }
    assert set(TelegramMessage.__annotations__) == {
        "channelHandle",
        "channelId",
        "channelName",
        "forwards",
        "message",
        "messageId",
        "messageLink",
        "publishedAt",
        "reactions",
        "views",
    }
    assert set(NaverTrendRow.__annotations__) == {"d", "v"}


def test_type_exceptions_native_not_str():
    # Naver trend value is a native int; premium has real booleans.
    assert NaverTrendRow.__annotations__["v"] is int
    for f in ("t", "sms", "tms"):
        assert PremiumDetail.__annotations__[f] is bool
    # premium detail is optional-keyed (AMM-only fields absent for many pairs)
    assert PremiumDetail.__total__ is False


@responses.activate
def test_ticker_pandas_true_still_dataframe():
    payload = {"data": {"d": "1700000000", "p": "105.5"}}
    responses.add(
        responses.GET, re.compile(".*/api/v1/ticker.*"), json=payload, status=200
    )
    df = CexTicker(api_key="k", base_url=BASE_URL).get(
        exchange="binance", market="spot", symbol="BTC-USDT"
    )
    assert isinstance(df, pd.DataFrame)  # annotation change is hint-only

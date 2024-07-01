import os
import requests
from tests.util import random_str
from datamaxi.api import API
from datamaxi.__version__ import __version__
import logging


def test_API_initial():
    """Tests the API initialization"""

    client = API()

    client.should.be.a(API)
    client.api_key.should.be.none
    client.timeout.should.be.none
    client.show_limit_usage.should.be.false
    client.show_header.should.be.false
    client.session.should.be.a(requests.Session)
    client.session.headers.should.have.key("Content-Type").which.should.equal(
        "application/json;charset=utf-8"
    )
    client.session.headers.should.have.key("User-Agent").which.should.equal(
        "datamaxi/" + __version__
    )
    client.session.headers.should.have.key("X-DTMX-APIKEY").which.should.be.equal(
        "None"
    )

    client._logger.should.be(logging.getLogger("datamaxi.api"))


def test_API_env_key():
    """Tests the API initialization with API key in environment variable"""

    api_key = random_str()
    os.environ["DATAMAXI_API_KEY"] = api_key
    client = API()

    client.should.be.a(API)
    client.api_key.should.be.equal(api_key)
    client.session.headers.should.have.key("X-DTMX-APIKEY").which.should.be.equal(
        api_key
    )


def test_API_with_extra_parameters():
    """Tests the API initialization with extra parameters"""

    api_key = random_str()
    base_url = random_str()
    proxies = {"https": "https://1.2.3.4:8080"}

    client = API(
        api_key,
        base_url=base_url,
        show_limit_usage=True,
        show_header=True,
        timeout=0.1,
        proxies=proxies,
    )

    client.should.be.a(API)
    client.api_key.should.equal(api_key)
    client.timeout.should.equal(0.1)
    client.base_url.should.equal(base_url)
    client.show_limit_usage.should.be.true
    client.show_header.should.be.true
    client.proxies.should.equal(proxies)
    client.session.headers.should.have.key("X-DTMX-APIKEY").which.should.equal(api_key)

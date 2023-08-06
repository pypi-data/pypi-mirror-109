def test_it():
    pass


def test_create_request():
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_request("9999999")
    assert result.full_url == "https://api.kenall.jp/v1/postalcode/9999999"
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_fetch(mocker, dummy_json):
    import json
    import io
    from kenallclient.client import KenAllClient

    dummy_response = io.StringIO(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = object()
    target = KenAllClient("testing-api-key")
    result = target.fetch(request)
    mock_urlopen.assert_called_with(request)
    assert result

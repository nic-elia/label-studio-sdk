# This file was auto-generated by Fern from our API Definition.

import typing

from label_studio_sdk import FileUpload
from label_studio_sdk.client import AsyncLabelStudio, LabelStudio

from .utilities import validate_response


async def test_get(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response = {"id": 1, "file": "file"}
    expected_types: typing.Any = {"id": "integer", "file": None}
    response = client.files.get(id=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.files.get(id=1)
    validate_response(async_response, expected_response, expected_types)


async def test_delete(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert client.files.delete(id=1) is None  # type: ignore[func-returns-value]

    assert await async_client.files.delete(id=1) is None  # type: ignore[func-returns-value]


async def test_update(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response = {"id": 1, "file": "file"}
    expected_types: typing.Any = {"id": "integer", "file": None}
    response = client.files.update(id=1, request=FileUpload())
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.files.update(id=1, request=FileUpload())
    validate_response(async_response, expected_response, expected_types)


async def test_list_(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response = [{"id": 1, "file": "file"}]
    expected_types: typing.Any = ("list", {0: {"id": "integer", "file": None}})
    response = client.files.list(id=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.files.list(id=1)
    validate_response(async_response, expected_response, expected_types)


async def test_delete_many(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert client.files.delete_many(id=1) is None  # type: ignore[func-returns-value]

    assert await async_client.files.delete_many(id=1) is None  # type: ignore[func-returns-value]


async def test_download(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert client.files.download(filename="filename") is None  # type: ignore[func-returns-value]

    assert await async_client.files.download(filename="filename") is None  # type: ignore[func-returns-value]

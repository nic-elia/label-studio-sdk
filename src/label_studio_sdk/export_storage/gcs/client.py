# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pydantic_utilities import pydantic_v1
from ...core.request_options import RequestOptions
from ...types.gcs_export_storage import GcsExportStorage
from .types.gcs_create_response import GcsCreateResponse
from .types.gcs_update_response import GcsUpdateResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class GcsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list(
        self, *, project: typing.Optional[int] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[GcsExportStorage]:
        """
        You can connect your Google Cloud Storage bucket to Label Studio as a source storage or target storage. Use this API request to get a list of all GCS export (target) storage connections for a specific project.

        The project ID can be found in the URL when viewing the project in Label Studio, or you can retrieve all project IDs using [List all projects](../projects/list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        project : typing.Optional[int]
            Project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[GcsExportStorage]


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.list()
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs", method="GET", params={"project": project}, request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.List[GcsExportStorage], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        project: typing.Optional[int] = OMIT,
        bucket: typing.Optional[str] = OMIT,
        prefix: typing.Optional[str] = OMIT,
        google_application_credentials: typing.Optional[str] = OMIT,
        google_project_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GcsCreateResponse:
        """
        Create a new target storage connection to Google Cloud Storage.

        For information about the required fields and prerequisites, see [Google Cloud Storage](https://labelstud.io/guide/storage#Google-Cloud-Storage) in the Label Studio documentation.

        <Tip>After you add the storage, you should validate the connection before attempting to sync your data. Your data will not be exported until you [sync your connection](sync).</Tip>

        Parameters
        ----------
        project : typing.Optional[int]
            Project ID

        bucket : typing.Optional[str]
            GCS bucket name

        prefix : typing.Optional[str]
            GCS bucket prefix

        google_application_credentials : typing.Optional[str]
            The content of GOOGLE_APPLICATION_CREDENTIALS json file

        google_project_id : typing.Optional[str]
            Google project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsCreateResponse


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.create()
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs",
            method="POST",
            json={
                "project": project,
                "bucket": bucket,
                "prefix": prefix,
                "google_application_credentials": google_application_credentials,
                "google_project_id": google_project_id,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsCreateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def validate(self, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Validate a specific GCS export storage connection. This is useful to ensure that the storage configuration settings are correct and operational before attempting to export data.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.validate()
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs/validate", method="POST", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Get a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.get(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Delete a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        Deleting an export/target storage connection does not affect tasks with synced data in Label Studio. If you want to remove the tasks that were synced from the external storage, you will need to delete them manually from within the Label Studio UI or use the [Delete tasks](../../tasks/delete-all-tasks) API.

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.delete(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}", method="DELETE", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update(
        self,
        id: int,
        *,
        project: typing.Optional[int] = OMIT,
        bucket: typing.Optional[str] = OMIT,
        prefix: typing.Optional[str] = OMIT,
        google_application_credentials: typing.Optional[str] = OMIT,
        google_project_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GcsUpdateResponse:
        """
        Update a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        project : typing.Optional[int]
            Project ID

        bucket : typing.Optional[str]
            GCS bucket name

        prefix : typing.Optional[str]
            GCS bucket prefix

        google_application_credentials : typing.Optional[str]
            The content of GOOGLE_APPLICATION_CREDENTIALS json file

        google_project_id : typing.Optional[str]
            Google project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsUpdateResponse


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.update(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}",
            method="PATCH",
            json={
                "project": project,
                "bucket": bucket,
                "prefix": prefix,
                "google_application_credentials": google_application_credentials,
                "google_project_id": google_project_id,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsUpdateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def sync(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Sync tasks to a GCS export/target storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        Sync operations with external buckets only go one way. They either create tasks from objects in the bucket (source/import storage) or push annotations to the output bucket (export/target storage). Changing something on the bucket side doesn’t guarantee consistency in results.

        <Note>Before proceeding, you should review [How sync operations work - Source storage](https://labelstud.io/guide/storage#Source-storage) to ensure that your data remains secure and private.</Note>

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.export_storage.gcs.sync(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}/sync", method="POST", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncGcsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list(
        self, *, project: typing.Optional[int] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[GcsExportStorage]:
        """
        You can connect your Google Cloud Storage bucket to Label Studio as a source storage or target storage. Use this API request to get a list of all GCS export (target) storage connections for a specific project.

        The project ID can be found in the URL when viewing the project in Label Studio, or you can retrieve all project IDs using [List all projects](../projects/list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        project : typing.Optional[int]
            Project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[GcsExportStorage]


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.list()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs", method="GET", params={"project": project}, request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.List[GcsExportStorage], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create(
        self,
        *,
        project: typing.Optional[int] = OMIT,
        bucket: typing.Optional[str] = OMIT,
        prefix: typing.Optional[str] = OMIT,
        google_application_credentials: typing.Optional[str] = OMIT,
        google_project_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GcsCreateResponse:
        """
        Create a new target storage connection to Google Cloud Storage.

        For information about the required fields and prerequisites, see [Google Cloud Storage](https://labelstud.io/guide/storage#Google-Cloud-Storage) in the Label Studio documentation.

        <Tip>After you add the storage, you should validate the connection before attempting to sync your data. Your data will not be exported until you [sync your connection](sync).</Tip>

        Parameters
        ----------
        project : typing.Optional[int]
            Project ID

        bucket : typing.Optional[str]
            GCS bucket name

        prefix : typing.Optional[str]
            GCS bucket prefix

        google_application_credentials : typing.Optional[str]
            The content of GOOGLE_APPLICATION_CREDENTIALS json file

        google_project_id : typing.Optional[str]
            Google project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsCreateResponse


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.create()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs",
            method="POST",
            json={
                "project": project,
                "bucket": bucket,
                "prefix": prefix,
                "google_application_credentials": google_application_credentials,
                "google_project_id": google_project_id,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsCreateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def validate(self, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Validate a specific GCS export storage connection. This is useful to ensure that the storage configuration settings are correct and operational before attempting to export data.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.validate()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "api/storages/export/gcs/validate", method="POST", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Get a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.get(
            id=1,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Delete a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        Deleting an export/target storage connection does not affect tasks with synced data in Label Studio. If you want to remove the tasks that were synced from the external storage, you will need to delete them manually from within the Label Studio UI or use the [Delete tasks](../../tasks/delete-all-tasks) API.

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.delete(
            id=1,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}", method="DELETE", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update(
        self,
        id: int,
        *,
        project: typing.Optional[int] = OMIT,
        bucket: typing.Optional[str] = OMIT,
        prefix: typing.Optional[str] = OMIT,
        google_application_credentials: typing.Optional[str] = OMIT,
        google_project_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GcsUpdateResponse:
        """
        Update a specific GCS export storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        For more information about working with external storage, see [Sync data from external storage](https://labelstud.io/guide/storage).

        Parameters
        ----------
        id : int
            A unique integer value identifying this gcs export storage.

        project : typing.Optional[int]
            Project ID

        bucket : typing.Optional[str]
            GCS bucket name

        prefix : typing.Optional[str]
            GCS bucket prefix

        google_application_credentials : typing.Optional[str]
            The content of GOOGLE_APPLICATION_CREDENTIALS json file

        google_project_id : typing.Optional[str]
            Google project ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsUpdateResponse


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.update(
            id=1,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}",
            method="PATCH",
            json={
                "project": project,
                "bucket": bucket,
                "prefix": prefix,
                "google_application_credentials": google_application_credentials,
                "google_project_id": google_project_id,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsUpdateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def sync(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> GcsExportStorage:
        """
        Sync tasks to a GCS export/target storage connection. You will need to provide the export storage ID. You can find this using [List export storages](list).

        Sync operations with external buckets only go one way. They either create tasks from objects in the bucket (source/import storage) or push annotations to the output bucket (export/target storage). Changing something on the bucket side doesn’t guarantee consistency in results.

        <Note>Before proceeding, you should review [How sync operations work - Source storage](https://labelstud.io/guide/storage#Source-storage) to ensure that your data remains secure and private.</Note>

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GcsExportStorage


        Examples
        --------
        from label_studio_sdk.client import AsyncLabelStudio

        client = AsyncLabelStudio(
            api_key="YOUR_API_KEY",
        )
        await client.export_storage.gcs.sync(
            id="id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"api/storages/export/gcs/{jsonable_encoder(id)}/sync", method="POST", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(GcsExportStorage, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

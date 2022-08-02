"""
Test s3 manager.
"""

import pytest
from fastapi.exceptions import HTTPException

from jobbergate_api.s3_manager import (
    get_s3_object_as_tarfile,
    s3man_applications_source_files,
    s3man_jobscripts,
)


@pytest.mark.parametrize(
    "s3_manager, template",
    [
        (s3man_applications_source_files, "applications/{}/jobbergate.py"),
        (s3man_jobscripts, "job-scripts/{}/jobbergate.txt"),
    ],
)
@pytest.mark.parametrize("id", [0, 1, 2, 10, 100, 9999])
class TestS3ManagerKeyIdTwoWayMapping:
    """
    Test the conversions from id number to S3 key and vice versa.
    """

    @pytest.mark.parametrize("input_type", [int, str])
    def test_s3_manager__get_key_from_id_str(self, s3_manager, template, id, input_type):
        """
        Test the conversions from id number to S3 key.

        Notice both int and str are valid types for id and are tested.
        """
        key = template.format(id)
        assert s3_manager._get_engine_key(input_type(id)) == key

    def test_s3_manager__get_app_id_from_key(self, s3_manager, template, id):
        """
        Test the conversions from S3 key to id number.
        """
        key = template.format(id)
        assert s3_manager._get_dict_key(key) == id


@pytest.fixture
def dummy_s3man(s3_object):
    """
    Provide a dummy S3 manager used for tests containing only one key and object.
    """
    return {1: s3_object}


@pytest.mark.asyncio
async def test_get_s3_object_as_tarfile(dummy_s3man):
    """
    Test getting a file from S3 with get_s3_object function.
    """
    s3_file = get_s3_object_as_tarfile(dummy_s3man, 1)

    assert s3_file is not None


@pytest.mark.asyncio
async def test_get_s3_object_not_found(dummy_s3man):
    """
    Test exception at get_s3_object function when file does not exist in S3.
    """
    s3_file = None

    with pytest.raises(HTTPException) as exc:
        s3_file = get_s3_object_as_tarfile(dummy_s3man, 9999)

    assert "Application with app_id=9999 not found in S3" in str(exc)

    assert s3_file is None

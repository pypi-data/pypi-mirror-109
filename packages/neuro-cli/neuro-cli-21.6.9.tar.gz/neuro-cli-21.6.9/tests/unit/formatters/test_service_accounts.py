from typing import Any, List

import pytest
from dateutil.parser import isoparse

from neuro_sdk import ServiceAccount

from neuro_cli.formatters.service_accounts import (
    ServiceAccountFormatter,
    ServiceAccountsFormatter,
    SimpleServiceAccountsFormatter,
)
from neuro_cli.formatters.utils import format_datetime_human


def test_service_account_formatter(rich_cmp: Any) -> None:
    account = ServiceAccount(
        id="account",
        name="test1",
        role="test-role",
        owner="user",
        default_cluster="cluster",
        created_at=isoparse("2017-03-04T12:28:59.759433+00:00"),
        role_deleted=False,
    )
    fmtr = ServiceAccountFormatter(datetime_formatter=format_datetime_human)
    rich_cmp(fmtr(account))


@pytest.fixture
def service_accounts_list() -> List[ServiceAccount]:
    return [
        ServiceAccount(
            id="account-1",
            name="test1",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=isoparse("2017-03-04T12:28:59.759433+00:00"),
            role_deleted=False,
        ),
        ServiceAccount(
            id="account-2",
            name="test2",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=isoparse("2017-03-04T12:28:59.759433+00:00"),
            role_deleted=True,
        ),
        ServiceAccount(
            id="account-3",
            name="test3",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=isoparse("2017-03-04T12:28:59.759433+00:00"),
            role_deleted=False,
        ),
        ServiceAccount(
            id="account-4",
            name="test4",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=isoparse("2017-03-04T12:28:59.759433+00:00"),
            role_deleted=False,
        ),
    ]


def test_service_accounts_formatter_simple(
    service_accounts_list: List[ServiceAccount], rich_cmp: Any
) -> None:
    fmtr = SimpleServiceAccountsFormatter()
    rich_cmp(fmtr(service_accounts_list))


def test_disks_formatter(
    service_accounts_list: List[ServiceAccount], rich_cmp: Any
) -> None:
    fmtr = ServiceAccountsFormatter(datetime_formatter=format_datetime_human)
    rich_cmp(fmtr(service_accounts_list))

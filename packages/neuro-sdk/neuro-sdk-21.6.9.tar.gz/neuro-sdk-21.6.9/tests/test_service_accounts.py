from datetime import datetime, timedelta
from typing import Callable

from aiohttp import web

from neuro_sdk import Client, Cluster, ServiceAccount

from tests import _TestServerFactory

_MakeClient = Callable[..., Client]


async def test_list(
    aiohttp_server: _TestServerFactory,
    make_client: _MakeClient,
    cluster_config: Cluster,
) -> None:
    created_at = datetime.now() - timedelta(days=1)

    async def handler(request: web.Request) -> web.Response:
        return web.json_response(
            [
                {
                    "id": "account-1",
                    "owner": "user",
                    "name": "test1",
                    "role": "test-role-1",
                    "default_cluster": "cluster1",
                    "role_deleted": False,
                    "created_at": created_at.isoformat(),
                },
                {
                    "id": "account-2",
                    "owner": "user",
                    "name": "test2",
                    "role": "test-role-2",
                    "default_cluster": "cluster2",
                    "role_deleted": True,
                    "created_at": created_at.isoformat(),
                },
            ]
        )

    app = web.Application()
    app.router.add_get("/service_accounts", handler)

    srv = await aiohttp_server(app)

    ret = []

    async with make_client(srv.make_url("/")) as client:
        async for s in client.service_accounts.list():
            ret.append(s)

    assert ret == [
        ServiceAccount(
            id="account-1",
            name="test1",
            role="test-role-1",
            owner="user",
            default_cluster="cluster1",
            created_at=created_at,
            role_deleted=False,
        ),
        ServiceAccount(
            id="account-2",
            name="test2",
            role="test-role-2",
            owner="user",
            default_cluster="cluster2",
            created_at=created_at,
            role_deleted=True,
        ),
    ]


async def test_add(
    aiohttp_server: _TestServerFactory,
    make_client: _MakeClient,
    cluster_config: Cluster,
) -> None:
    created_at = datetime.now()

    async def handler(request: web.Request) -> web.Response:
        data = await request.json()
        assert data == {
            "name": "test-account",
            "role": "test-role",
            "default_cluster": "cluster",
        }
        return web.json_response(
            {
                "id": "account-1",
                "owner": "user",
                "name": "test-account",
                "role": "test-role",
                "default_cluster": "cluster",
                "role_deleted": False,
                "created_at": created_at.isoformat(),
                "token": "fake-token",
            },
        )

    app = web.Application()
    app.router.add_post("/service_accounts", handler)

    srv = await aiohttp_server(app)

    async with make_client(srv.make_url("/")) as client:
        account, token = await client.service_accounts.create(
            name="test-account", role="test-role", default_cluster="cluster"
        )
        assert account == ServiceAccount(
            id="account-1",
            name="test-account",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=created_at,
            role_deleted=False,
        )
        assert token == "fake-token"


async def test_get(
    aiohttp_server: _TestServerFactory,
    make_client: _MakeClient,
    cluster_config: Cluster,
) -> None:
    created_at = datetime.now()

    async def handler(request: web.Request) -> web.Response:
        assert request.match_info["key"] == "name"
        return web.json_response(
            {
                "id": "account-1",
                "owner": "user",
                "name": "test-account",
                "role": "test-role",
                "default_cluster": "cluster",
                "role_deleted": False,
                "created_at": created_at.isoformat(),
            },
        )

    app = web.Application()
    app.router.add_get("/service_accounts/{key}", handler)

    srv = await aiohttp_server(app)

    async with make_client(srv.make_url("/")) as client:
        account = await client.service_accounts.get("name")
        assert account == ServiceAccount(
            id="account-1",
            name="test-account",
            role="test-role",
            owner="user",
            default_cluster="cluster",
            created_at=created_at,
            role_deleted=False,
        )


async def test_rm(aiohttp_server: _TestServerFactory, make_client: _MakeClient) -> None:
    async def handler(request: web.Request) -> web.Response:
        assert request.match_info["key"] == "name"
        raise web.HTTPNoContent

    app = web.Application()
    app.router.add_delete("/service_accounts/{key}", handler)

    srv = await aiohttp_server(app)

    async with make_client(srv.make_url("/")) as client:
        await client.service_accounts.rm("name")

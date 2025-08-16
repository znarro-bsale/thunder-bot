import asyncio
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Any, Iterator
from .adapter import DatabaseAdapter
from ..config import TURSO_DATABASE_URL, TURSO_AUTH_TOKEN

class TursoAdapter(DatabaseAdapter):

    def __init__(self):
        if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
            raise ValueError("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set for Turso adapter")

        try:
            import libsql_client
        except ImportError:
            raise ImportError("libsql_client is required for Turso adapter. Install it with: uv add libsql-client")

        self.url = TURSO_DATABASE_URL
        self.auth_token = TURSO_AUTH_TOKEN
        self.libsql = libsql_client

    def _run_async(self, coro):
        """Run async coroutine in a dedicated thread"""
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()

        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_in_thread)
            return future.result()

    async def _create_client(self):
        """Create and return a properly configured client"""
        http_url = self.url.replace("libsql://", "https://") + "/v1"
        return self.libsql.create_client(url=http_url, auth_token=self.auth_token)

    @contextmanager
    def connection(self) -> Iterator[Any]:
        yield self.libsql

    def execute_script(self, script: str) -> None:
        async def _execute():
            client = await self._create_client()
            try:
                statements = [stmt.strip() for stmt in script.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        await client.execute(statement)
            finally:
                await client.close()

        self._run_async(_execute())

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        async def _fetch():
            client = await self._create_client()
            try:
                result = await client.execute(query, params)
                if result.rows:
                    return dict(zip(result.columns, result.rows[0]))
                return None
            finally:
                await client.close()

        return self._run_async(_fetch())

    def fetch_all(self, query: str, params: tuple = ()) -> list[Dict[str, Any]]:
        async def _fetch():
            client = await self._create_client()
            try:
                result = await client.execute(query, params)
                if result.rows:
                    return [dict(zip(result.columns, row)) for row in result.rows]
                return []
            finally:
                await client.close()

        return self._run_async(_fetch())

    def execute(self, query: str, params: tuple = ()) -> None:
        async def _execute():
            client = await self._create_client()
            try:
                await client.execute(query, params)
            finally:
                await client.close()

        self._run_async(_execute())

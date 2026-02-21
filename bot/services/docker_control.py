from __future__ import annotations

import aiohttp


class DockerControlService:
    async def restart(self, container_name: str) -> None:
        connector = aiohttp.UnixConnector(path="/var/run/docker.sock")
        async with aiohttp.ClientSession(connector=connector) as s:
            async with s.post(f"http://docker/containers/{container_name}/restart") as r:
                if r.status >= 300:
                    raise RuntimeError(await r.text())

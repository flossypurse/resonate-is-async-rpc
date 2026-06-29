from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def baz(ctx: Context) -> int:
    print("running function baz")
    return 1


async def main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-c",
    )
    r.register(baz)
    print("service-c is running", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

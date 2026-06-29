from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def rax(ctx: Context) -> int:
    print("running function bar")
    return 1


async def main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-h",
    )
    r.register(rax)
    print("service-h is running", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

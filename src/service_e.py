from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def quz(ctx: Context, arg: int) -> None:
    print("running function quz")
    await ctx.options(target="service-f").detached("cog", arg + 1).id()


async def main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-e",
    )
    r.register(quz)
    print("service e is running", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

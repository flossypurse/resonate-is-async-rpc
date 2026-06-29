from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from resonate.resonate import Resonate

if TYPE_CHECKING:
    from resonate.context import Context


async def zim(ctx: Context, arg: int) -> int:
    print("running function zim")
    future_rax = ctx.options(target="service-h").rpc("rax")
    future_dop = ctx.options(target="service-i").rpc("dop")
    result_bar = await future_rax
    result_baz = await future_dop
    return result_bar + result_baz + arg


async def main() -> None:
    r = Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="service-g",
    )
    r.register(zim)
    print("service-g is running", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

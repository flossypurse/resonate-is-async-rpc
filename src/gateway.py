from __future__ import annotations

import asyncio
import os
import threading
from typing import Any

from flask import Flask, jsonify
from resonate.resonate import Resonate

# ---------------------------------------------------------------------------
# Asyncio event loop running in a background thread.
# Resonate uses asyncio internally, so we keep a dedicated loop alive for the
# lifetime of the process and dispatch coroutines into it from Flask's sync
# route handlers via run_coroutine_threadsafe.
# ---------------------------------------------------------------------------

_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
_resonate: Resonate


def _start_loop() -> None:
    asyncio.set_event_loop(_loop)
    _loop.run_forever()


_loop_thread = threading.Thread(target=_start_loop, daemon=True)
_loop_thread.start()


def _run_async(coro: Any) -> Any:
    """Run a coroutine on the background loop and block until it completes."""
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()


async def _create_resonate() -> Resonate:
    return Resonate(
        url=os.environ.get("RESONATE_URL", "http://localhost:8001"),
        group="gateway",
    )


_resonate = _run_async(_create_resonate())

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app_node_id = "gateway"
app_node_group = "gateway"

app = Flask(app_node_id)


@app.route("/await-chain", methods=["POST"])
def await_chain_route_handler() -> Any:
    try:
        print("running await_chain_route_handler")
        promise_id = "await-chain"
        handle = _resonate.options(target="service-a").rpc(promise_id, "foo")
        print("waiting on result")
        message = _run_async(handle.result())
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/detached-chain", methods=["POST"])
def detached_chain_route_handler() -> Any:
    try:
        print("running detached_chain_route_handler")
        promise_id = "detached-chain"
        _resonate.options(target="service-d").rpc(promise_id, "qux", 1)
        message = "detached-chain started"
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/fan-out-workflow", methods=["POST"])
def fan_out_workflow_route_handler() -> Any:
    try:
        print("running fan-out-workflow_route_handler")
        promise_id = "fan-out-workflow"
        handle = _resonate.options(target="service-g").rpc(promise_id, "zim", 1)
        print("waiting on result")
        message = _run_async(handle.result())
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main() -> None:
    print(
        f"app node id {app_node_id} | app node group {app_node_group} | http capable | running",
        flush=True,
    )
    app.run(port=5000)


if __name__ == "__main__":
    main()

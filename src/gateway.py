from resonate.message_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate import Resonate
from flask import Flask, jsonify


app_node_id = "gateway"
app_node_group = "gateway"

app = Flask(app_node_id)

resonate = Resonate(
    store=RemoteStore(host="http://localhost", port="8001"),
    message_source=Poller(
        host="http://localhost", port="8002", id=app_node_id, group=app_node_group
    ),
)


@app.route("/await-chain", methods=["POST"])
def await_chain_route_handler():
    try:
        print("running await_chain_route_handler")
        promise_id = "await-chain"
        handle = resonate.options(target="poll://service-a").begin_rpc(promise_id, "foo")
        print("waiting on result")
        message = handle.result()
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/detached-chain", methods=["POST"])
def detached_chain_route_handler():
    try:
        print("running detached_chain_route_handler")
        promise_id = "detached-chain"
        resonate.options(target="poll://service-d").begin_rpc(promise_id, "qux", 1)
        message = "detached-chain started"
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/fan-out-workflow", methods=["POST"])
def fan_out_workflow_route_handler():
    try:
        print("running fan-out-workflow_route_handler")
        promise_id = "fan-out-workflow"
        handle = resonate.options(target="poll://service-g").begin_rpc(promise_id, "zim", 1)
        print("waiting on result")
        message = handle.result()
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main():
    print(
        f"app node id {app_node_id} | app node group {app_node_group} | http capable | running"
    )
    app.run(port=5000)


if __name__ == "__main__":
    main()

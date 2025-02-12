# Resonate is also an Async RPC framework

This project showcases Resonate as an Async RPC framework with three different request flows.

- [chain](./chain/README.md)
- [fan_out](./fan_out/README.md)
- [fire_and_forget](./fire_and_forget/README.md)

To learn more about Resonate as an Async RPC, checkout the [Resonate is also an Async RPC Framework](https://resonatehqio.substack.com/p/resonate-is-also-an-async-rpc-framework) article.

## Project prerequisites

This project uses [uv](https://docs.astral.sh/uv/) as the Python environment and package manager.

This project requires that a [Resonate Server](https://docs.resonatehq.io/get-started/server-quickstart) is running locally.

## Chain request flow

The chain request flow has the foo service make a synchronous RPC (known by Resonate as an RFC) to the bar service, which will cause the bar service to make a synchronous RPC to the baz service.

## Fan-out request flow

The fan-out request flow has the foo service make two asynchronous RPCs (known by Resonate as RFIs), one to the bar service and one to the baz service, and await on the results only after making the RPCs.

## Fire-and-forget request flow

The fire-and-forget request flow has the foo service make an async call to bar and returns without waiting for a result. Bar then makes an async call to baz without waiting for a result. Baz prints the cummulative result.

## RFCs vs RFIs

RFI stands for Remote Function Invocation.

With Resonate a Remote Function Invocation returns a Durable Promise. You don't have to block the rest of the function on the result of the function that was invoked. You can yield the result at any point later in the execution. However, yielding the result of the promise (yielding the result of the function that was invoked) does block execution until the result is available. In other words, RFI is an asynchronous API.

RFC stands for Remote Function Call, it is effectively an RFI but with syntax sugar, and yields the result of the function that was invoked. In other words, it is a synchronous API.

# Gevent Block Monitor Examples

A demonstration project showcasing gevent block monitoring capabilities with Flask applications.

## Overview

This project demonstrates:
- Using gevent with Flask for high-concurrency web applications
- Detecting and monitoring blocking operations in gevent's event loop

## Requirements

- Python 3.11+
- `uv`

## Installation

```bash
uv sync
```

## Running the Application

To run the application with gevent workers and thread monitoring enabled:

```bash
./run.sh
```

The `run.sh` script:
- Sets the `GEVENT_MONITOR_THREAD_ENABLE=1` environment variable to enable gevent thread monitoring
- Launches gunicorn with 2 gevent workers on port 5555
- Automatically monitors and logs blocking operations in the event loop

## API Endpoints

- `/prime/<n>`: Checks if a number is prime (CPU-bound task in main thread)
- `/prime_thread/<n>`: Checks if a number is prime (CPU-bound task in separate thread)

## Test Scripts for Gevent Block Logging

Use these scripts to demonstrate gevent's thread monitoring and block logging capabilities:

```bash
# Test the threaded endpoint (should not trigger block logs)
ab -k -c 10 -n 20000 http://localhost:5555/prime_thread/6

# Test the main-thread endpoint (will trigger gevent block logs)
ab -k -c 10 -n 20000 http://localhost:5555/prime/6
```

**Note**: The second test on the `/prime/` endpoint will produce gevent block logs because CPU-bound operations in the main thread block the gevent event loop. This demonstrates how gevent's monitoring can detect and log blocking operations, which is useful for identifying performance bottlenecks in your application.

You can check the logs for messages like:
```
2025-05-19T10:09:20Z : Greenlet <Greenlet "Greenlet-1" at 0x107123d80: _handle_and_close_when_done(functools.partial(<bound method GeventWorker.handl, <bound method StreamServer.do_close of <StreamServ, (<gevent._socket3.socket at 0x105ce2140 object, fd)> appears to be blocked
    Reported by <gevent._gevent_c_tracer.GreenletTracer object at 0x10582ddf0>
Blocked Stack (for thread id 0x1fc3e8c80):
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/baseserver.py", line 34, in _handle_and_close_when_done
    return handle(*args_tuple)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/workers/ggevent.py", line 123, in handle
    super().handle(listener, client, addr)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/workers/base_async.py", line 55, in handle
    self.handle_request(listener_name, req, client, addr)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/workers/ggevent.py", line 127, in handle_request
    super().handle_request(listener_name, req, sock, addr)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/workers/base_async.py", line 116, in handle_request
    resp.write(item)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/http/wsgi.py", line 346, in write
    util.write(self.sock, arg, self.chunked)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gunicorn/util.py", line 287, in write
    sock.sendall(data)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/_socketcommon.py", line 698, in sendall
    return _sendall(self, data_memory, flags)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/_socketcommon.py", line 387, in _sendall
    timeleft = __send_chunk(socket, chunk, flags, timeleft, end)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/_socketcommon.py", line 316, in __send_chunk
    data_sent += socket.send(chunk, flags)
  File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/_socketcommon.py", line 721, in send
    return self._sock.send(data, flags)
                    File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/baseserver.py", line 246, in _do_read
                      self.do_handle(*args)
                    File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/baseserver.py", line 208, in do_handle
                      spawn(_handle_and_close_when_done, handle, close, args)
                    File "/Users/xxx/gevent-block-monitor-examples/.venv/lib/python3.11/site-packages/gevent/pool.py", line 392, in spawn
```

These indicate when a CPU-bound operation has blocked the gevent event loop.


## License

[MIT License](LICENSE)

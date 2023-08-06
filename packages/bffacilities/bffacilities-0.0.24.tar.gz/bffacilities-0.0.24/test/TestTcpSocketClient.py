import unittest
from bffacilities.socketserver import TcpSocketServer, SocketClient, logger
from bffacilities.utils import changeLoggerLevel
import logging
changeLoggerLevel(logger, logging.DEBUG)
import time
import threading
import asyncio
async def createClient(id, address):
    client = SocketClient.createTcpClient(address)
    try:
        client.connect()
        data = f"{{'name': '{id}'}}"
        i = 0
        while i < 10:
            client.sock.send(data.encode())
            await asyncio.sleep(2) 
            i += 1
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        print("exception:", e)
    print("Client Done ", id)
async def main(args):
    tasks = []
    for i in range(args["count"]):
        tasks.append(createClient(i, (args["host"], args["port"])))
    print("start")
    try:
        await asyncio.gather(*tasks)
    except (KeyboardInterrupt, SystemExit):
        pass
    

if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser("TestTcpSocketClient")
    parser.add_argument("--port", type=int, default=54134, help="set port")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="set host")
    parser.add_argument("--count", type=int, default=10, help="parallel count")
    args = vars(parser.parse_args(sys.argv[1:]))
    
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(args))


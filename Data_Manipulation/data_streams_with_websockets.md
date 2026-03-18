---
title: Real Time Data Streams with WebSockets
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: false
---

Real Time Data Streams with WebSockets

Introduction

In data science and statistics, the speed of data ingestion directly affects the accuracy of models and interpretations. One common way to access data is through APIs (Application Programming Interfaces), which allow communication between two computers, often called the client and server.

Traditional APIs rely on a request response model where a client repeatedly requests new data from a server. A WebSocket connection works differently. It establishes a persistent, bidirectional channel between the client and server.

Once a WebSocket connection is opened, the server can continuously push updates without requiring repeated requests. This allows statistical models to receive data the exact moment a new observation occurs.

A helpful analogy is to think of a traditional API like a faucet that only produces water when the handle is turned, while a WebSocket behaves more like a river where the data continuously flows once you connect.

This architecture is particularly useful in environments where latency matters, such as financial markets, and sensor such as Internet of Things (IoT).

To learn more about websockets see the Wiki here.

Keep in Mind

When working with WebSockets in data workflows, several considerations are important.

WebSocket streams can generate extremely high frequency data, which may require filtering or aggregation before analysis, or displaying data.

Long running connections require stable infrastructure since interruptions will stop the data stream, to learn more about establishing such connection, see below.

Many WebSocket APIs require a subscription message specifying which symbols or datasets you want to receive.

Real time data pipelines often require asynchronous programming patterns, which may differ from standard statistical scripting workflows.

High frequency streams may produce far more data than can realistically be stored or processed without intermediate buffering systems.

Also Consider

Before getting started, you may want to ensure you are in the correct working directory:

See here Set a Working Directory

Also ensure your environment is correctly configured.

To learn more about a Python environment see here.

Implementations

JavaScript

JavaScript is commonly used for WebSocket connections due to its event driven architecture and native browser support. Additionally if you are building a front end, it would be convenient in using a similar language for the backend as well.

const socket = new WebSocket("wss://econ_data.com"); // replace with your url

socket.onopen = () => {
    socket.send(JSON.stringify({
        type: "subscribe", // notice the subscribe message
        symbol: "TICKER"
    }));
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Market Update:", data);
};


Python

Python provides several libraries for working with WebSockets. A commonly used combination is websockets and asyncio, which allow asynchronous data ingestion. To learn more see documentation here; websockets and asyncio.

import asyncio  
import websockets  
import json  
  
async def stream_economic_data():  
  
    uri = "wss://econ_data.com" # put your url here
  
    async with websockets.connect(uri) as websocket:  
  
        await websocket.send(json.dumps({  
            "type": "subscribe",  
            "symbol": "TICKER"  
        }))  
  
        while True:  
            data = await websocket.recv()  
            message = json.loads(data)  
  
            print(message)  
  
if __name__ == "__main__":  
    asyncio.run(stream_economic_data())


This script connects to a WebSocket server, subscribes to a data stream, and continuously receives updates.

If you are working inside a Jupyter Notebook, the event loop is already running. In that case you get rid of the last if statement, and can call the function directly using:

await stream_economic_data()

Python (Example with Real Time Calculations)

The following example demonstrates how a statistical process can be applied to a streaming dataset.

import asyncio  
import websockets  
import json  
from datetime import datetime  
import statistics  
  
async def stream_dummy_data():  
  
    uri = "wss://echo.websocket.events"  # acts as an actor for websocket
    # Note that there are many such test servers we might consider as alternatives
    THRESHOLD = 150.50  
  
    prices = []  
  
    async with websockets.connect(uri) as websocket:  
  
        payload = {  
            "type": "subscribe",  
            "symbol": "DUMMY_INDEX",  
            "price": 150.00  
        }  
  
        await websocket.send(json.dumps(payload))  
        
        # Error handling is a good idea since servers may experience downtime!
        try:
          while True:  
    
              data = await websocket.recv()  
              message = json.loads(data)  
    
              current_price = message["price"] + 0.05  
              message["price"] = current_price  
              
              # For long-running scripts, this will eventually consume all memory
              # In application you may want to instead take just a rolling mean of the last N observations
              prices.append(current_price)  
    
              current_mean = statistics.mean(prices)  
    
              timestamp = datetime.now().strftime("%H:%M:%S")  
    
              if current_mean > THRESHOLD:  
                  print(f"[{timestamp}] ALERT: mean exceeded threshold")  
              else:  
                  print(f"[{timestamp}] price={current_price} mean={current_mean}")  
    
              await asyncio.sleep(1)  
              await websocket.send(json.dumps(message))  
      except:
        pass
        # Depending on the application, consider waiting here and trying again later
  
if __name__ == "__main__":  
    asyncio.run(stream_dummy_data())

This example simulates a streaming dataset by sending data through an echo server and updating the price value over time. The script calculates the running mean of the data and triggers an alert when the value exceeds a specified threshold. This example shows the possibilities of using a websocket. For example, imagine if we wanted to run additional models or statistics in this script with a possible SMS message alert to the user.

Deployment and Infrastructure

Local scripts are useful for experimentation, but real time systems generally require persistent infrastructure so that data streams remain active even when your local machine is offline.

Cloud Infrastructure (AWS)

Connecting your real time data pipeline to AWS (Amazon Web Services) is a common approach for achieving production level reliability and scalability. The architecture you choose will depend on whether you are building your own websocket server or simply ingesting an external data stream.

Building Your Own WebSocket API If you want to distribute real time data to users, AWS provides infrastructure designed to manage persistent connections.

API Gateway: Handles persistent websocket connections between clients and your server.

AWS Lambda and DynamoDB: Often used together to manage connection mapping. This allows the system to track active users and determine where to push updates.

See more here: AWS Docs

Ingesting and Processing External Data Feeds If you are consuming an existing real time stream, such as financial market data or IoT, the following services are commonly used.

Amazon Kinesis Data Streams: Designed for ingesting high frequency data streams and processing thousands of records per second.

Amazon SNS (Simple Notification Service): Can trigger real time alerts via email or SMS when statistical thresholds or model outputs meet certain conditions.

AWS Lambda and DynamoDB: Often used to process messages, maintain and store data about the incoming stream, and used for connection mapping.

Persistent Compute (EC2 and Lightsail) Some applications require scripts that run continuously rather than event driven serverless functions.

Amazon EC2: Provides full control of a virtual server where long running Python or JavaScript WebSocket clients can operate continuously.

Amazon Lightsail: A simplified and lower cost alternative to EC2 that is useful for hosting lightweight streaming services or data connectors.

Virtual Private Server (VPS)

A Virtual Private Server provides an always on Linux environment for running WebSocket clients and data processing scripts.

While each provider such as DigitalOcean, Linode, or ForestRacks has slightly different setup procedures, the workflow generally follows the same pattern: - Deploy your scripts to the remote server - Configure them to run as background processes - Maintain persistent connections to the data stream

Advantages - Predictable and relatively low monthly cost - Full root level access to the operating system - Complete control over deployment and system configuration

Disadvantages - Requires manual setup and maintenance - Security hardening and monitoring are your responsibility - Scaling infrastructure must be configured manually

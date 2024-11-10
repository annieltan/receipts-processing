# Instructions
Run these commands after cloning my repo:
1. `docker build -t fetch-receipts .`
2. `docker run --rm -p 8080:8080 fetch-receipts`
Server should start running on port 8080

In a separate terminal, run:
 ```
 curl -X POST http://127.0.0.1:8080/receipts/process -H 'Content-Type: application/json' -d '{paste json receipt here}'
 ```
You can find examples in the `receipts` folder for a receipt.
That should return a UUID which will be used to calculate points.

Now run:
```
curl -X GET http://127.0.0.1:8080/receipts/{UUID}/points
```
(You can also use the browser to make this GET request)
You should see the number of points given from processing the receipt.
/* require() calls */
const http    = require("http");
const https   = require("https");
const os      = require("os");
const process = require("process");
const fs      = require("fs");
const express = require("express");
const spawn   = require("child_process").spawn;

const SERVER_IP  = "127.0.0.1";
const HTTP_PORT  = 8080; // HTTP port

/* Get datetime as a string */
function getTime(){
	return new Date().getTime();
}

/* Express Variables */
const app = express(); // Create Express app.

/* Express Request Handlers */
app.get("/latest_hash", (request, response) => {
    /* Initialize GET variables */
    response.set("Content-Type", "application/json"); // Set response header to JSON.
    response.set("Access-Control-Allow-Origin", "*"); // Set Access-Control header.
    let requestInfo = {};
    let timeRecv = getTime();

    requestInfo.error = {}; // No error.
    requestInfo.statusCode = response.statusCode; // Set requestInfo status code.
    
    let py = spawn('python', ['./blockchain.py']);
    let data;
    console.log("running blockchain");
    py.stdout.on('data', function(d){
        console.log("callback received, data ", d);
        data = {"latest_hash": d.toString()};
        const responseJSON = {requestInfo, data}; // Create response body.
        response.send(JSON.stringify(responseJSON)); // Write HTTP response.
    });
});

app.all("*", (request, response) => {
    response.set("Access-Control-Allow-Origin", "*"); // Set Access-Control header.
	response.sendStatus(404); // Default router -- send 404 because it doesn't exist.
});

/* Information Code */
console.log("--- Node.js Info ---");
console.log(`Current time: ${getTime()}`); // Print datetime
console.log("Node version:", process.version); // Print node version
console.log("Server IP:", SERVER_IP);
console.log("HTTP port:", HTTP_PORT);
console.log("--- System Info ---");
console.log("OS Version:", os.type(), os.release());
console.log("--- Console Output ---");

/* Executed Code */
http.createServer(app).listen(HTTP_PORT); // Listen on port specified.

/* Error handlers */
process.on("unhandledRejection", (reason, p) => {
	console.error("Unhandled promise rejection at promise", p, "with reason", reason);
});

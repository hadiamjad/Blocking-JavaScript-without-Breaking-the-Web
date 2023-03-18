window.tabId=0;
var stmt = {};
var url = [];
const port = 3000;

function getHeaderString(headers) {
  let responseHeader = '';
  headers.forEach((header, key) => {
    responseHeader += key + ':' + header + '\n';
  });
  return responseHeader;
}

async function ajaxMe(url, headers, method, postData, success, error) {
  let finalResponse = {};
  let response = await fetch(url, {
    method,
    mode: 'cors',
    headers,
    redirect: 'follow',
    body: postData
  });
  finalResponse.response = await response.text();
  finalResponse.headers = getHeaderString(response.headers);
  if (response.ok) {
    success(finalResponse);
  } else {
    error(finalResponse);
  }
}

function editResponse(resp, lineNo, columnNo) {
  var startLine;
  var endLine;
  var count = 0;

  for(let i=0; i<resp.length; i++){
      if(resp[i]=='\n'){
        count++;
        if(count == lineNo){
          startLine = i;
          break;
        }
      }
  }
  startLine +=parseInt(columnNo)

  for(let i=columnNo; i<resp.length; i++){
      if(resp[i] == ';'){
        endLine = i;
        break;
      }
  }
  return resp.substr(0, startLine-1) + resp.substr(endLine);
}

chrome.tabs.query({active:true},
  function(d){
    //current tab_id--d[1].id--d[1].url==top_level_url
    window.tabId = d[0].id;
    chrome.debugger.attach({tabId:tabId}, version,
     function(err){
       if(err)
          console.log(err);
       else
          console.log("debugger attached");
     } );
    chrome.debugger.sendCommand({tabId:tabId}, "Network.enable");
    // chrome.debugger.sendCommand({tabId:tabId}, "Fetch.enable", { patterns: [{ urlPattern: '*' }] });

    // // blocking specified request
    // chrome.webRequest.onBeforeRequest.addListener(
    //   function(details) { return {cancel: true}; },
    //   {urls: url},
    //   ["blocking"]
    // );
    chrome.debugger.onEvent.addListener(onEvent);
  })

function onEvent(debuggeeId, message, params) {
  if (tabId != debuggeeId.tabId)
    return;
  if (message == "Network.requestWillBeSent") {
      fetch(`http://localhost:${port}/request`, {
        method: "POST", 
        body: JSON.stringify({"http_req": params.request.url,
        "request_id":params.requestId,
        "top_level_url": 0,
        "frame_url":params.documentURL,
        "resource_type":params.type,
        "header": params.request.headers,
        "timestamp": params.timestamp,
        "frameId": params.frameId,
        "call_stack":params.initiator}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("Request complete! response");
      }); 
  }
  else if (message == "Network.requestWillBeSentExtraInfo"){
    fetch(`http://localhost:${port}/requestinfo`, {
      method: "POST", 
      body: JSON.stringify({
      "request_id":params.requestId,
      "cookies": params.associatedCookies,
      "headers":params.headers,
      "connectTiming":params.connectTiming,
      "clientSecurityState": params.clientSecurityState}),
      mode: 'cors',
      headers: {
        'Access-Control-Allow-Origin':'*',
        "Content-Type": "application/json"
      }
    }).then(res => {
      console.log("RequestInfo complete! response");
    }); 

  }
  else if (message == "Network.responseReceived") {
      chrome.debugger.sendCommand({
          tabId: tabId
      }, "Network.getResponseBody", {
          "requestId": params.requestId
      }, function(response) {
              // you get the response body here!
              fetch(`http://localhost:${port}/response`, {
                method: "POST", 
                body: JSON.stringify({
                "request_id":params.requestId,
                "response":params.response,
                "resource_type":params.type}),
                mode: 'cors',
                headers: {
                  'Access-Control-Allow-Origin':'*',
                  "Content-Type": "application/json"
                }
              }).then(res => {
                console.log("Response complete! response");
              });
      });
  }
  // var continueParams = {
  //   requestId: params.requestId,
  // };
  
  // if (message == "Fetch.requestPaused"){
  //     if (stmt.hasOwnProperty(params.request.url)){ 
  //       ajaxMe(params.request.url, params.request.headers, params.request.method, params.request.postData, (data) => {
  //           continueParams.responseCode = 200;
  //           for(let i=0; i<stmt[params.request.url].length; i++){
  //             console.log("requestPaused");
  //             console.log(params.request.url);
  //             data.response = editResponse(data.response, stmt[params.request.url][i][1], stmt[params.request.url][i][2]);
  //             // data.response = replaceMethod(data.response, stmt[params.request.url][i][0]);
  //           }
  //           continueParams.binaryResponseHeaders = btoa(unescape(encodeURIComponent(data.headers.replace(/(?:\r\n|\r|\n)/g, '\0'))));
  //           continueParams.body = btoa(unescape(encodeURIComponent(data.response)));
  //           chrome.debugger.sendCommand({tabId:debuggeeId.tabId}, 'Fetch.fulfillRequest', continueParams);
  //       }, (status) => {
  //         chrome.debugger.sendCommand({tabId:debuggeeId.tabId}, 'Fetch.continueRequest', continueParams);
  //       });
  //     }
  //     else {
  //       console.log('request stopping')
  //       chrome.debugger.sendCommand({tabId:debuggeeId.tabId}, 'Fetch.continueRequest', continueParams);}
  // } 
}

var version = "1.0";
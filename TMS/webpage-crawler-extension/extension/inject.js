var cookieGetter = document.__lookupGetter__("cookie").bind(document);
var cookieSetter = document.__lookupSetter__("cookie").bind(document);

let originalFunction = window.Storage.prototype.setItem;
window.Storage.prototype.setItem = function(keyName, keyValue) {
    fetch("http://localhost:3000/cookiestorage", {
    method: "POST", 
    body: JSON.stringify({"top_level_url": window.location.href,
    "function":"storage_setter",
    "storage": {"keyName": keyName, "keyValue": keyValue},
    "stack":new Error().stack}),
    mode: 'cors',
    headers: {
      'Access-Control-Allow-Origin':'*',
      "Content-Type": "application/json"
    }
  }).then(res => {
    console.log("Localstorage collected");
  });
    originalFunction.apply(this, arguments);
    return;
}

let originalFunction2 = window.Storage.prototype.getItem;
window.Storage.prototype.getItem = function(keyName) {
    fetch("http://localhost:3000/cookiestorage", {
    method: "POST", 
    body: JSON.stringify({"top_level_url": window.location.href,
    "function":"storage_getter",
    "storage": {keyName},
    "stack":new Error().stack}),
    mode: 'cors',
    headers: {
      'Access-Control-Allow-Origin':'*',
      "Content-Type": "application/json"
    }
  }).then(res => {
    console.log("Localstorage collected");
  });
    originalFunction2.apply(this, arguments);
    return;
}


Object.defineProperty(document, 'cookie', {
    get: function() {
        var storedCookieStr = cookieGetter();
        fetch("http://localhost:3000/cookiestorage", {
        method: "POST", 
        body: JSON.stringify({"top_level_url": window.location.href,
        "function":"cookie_getter",
        "cookie": storedCookieStr,
        "stack":new Error().stack}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("CookieStorage collected");
      }); 
    },

    set: function(cookieString) {
        fetch("http://localhost:3000/cookiestorage", {
        method: "POST", 
        body: JSON.stringify({"top_level_url": window.location.href,
        "function":"cookie_setter",
        "cookie": cookieString,
        "stack":new Error().stack}),
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "Content-Type": "application/json"
        }
      }).then(res => {
        console.log("CookieStorage collected");
      }); 
    }
});
var headElement = (document.head||document.documentElement);
var injectJs = function(fileName) {
    var s = document.createElement('script');
    s.src = chrome.extension.getURL(fileName);
    headElement.insertBefore(s, headElement.firstElementChild);
};
// injectJs("inject.js");
// injectJs("test.js");
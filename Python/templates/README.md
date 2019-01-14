## IP = 192.168.8.105:7777/mic/  

JS reads the return value from mic:
1. If value is 0
2. Elif value is 1:
Do recognition!  

```
function hear(){
  if (window.hasOwnProperty('webkitSpeechRecognition')) {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    // recognition.lang = "English";
    recognition.start();
    console.log("Started");
    recognition.onresult = function(e) {
      console.log("Result: ");
      console.log(e.results[0][0].transcript);
      recognition.stop();
      // SEND IT TO IP e.results[0][0].transcript
      console.log("Stopped");
    };
    recognition.onerror = function(e) {
      recognition.stop();
      console.log(e);
      // SEND IT TO IP
      console.log("Stopped");
    }
  }
}
```
## GET:  

```
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}
```

## POST:  
```
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( X );
        // X is text value
    }
}
```

## How to use:  
```
var client = new HttpClient();
client.get('http://some/thing?with=arguments', function(response) {
    // do something with response
});
`

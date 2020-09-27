let textarea = document.getElementById("message");
let sendButton = document.getElementById("send");
let messages = document.evaluate("//div[@id='messages']/div", document).iterateNext();
let session_key = document.currentScript.getAttribute("session_key");

function authenticate(){
    socket.send(newMessage({"session_key": session_key}, ""));
    console.log("authenticated.")
}

function newMessage(headers, message) {
    return JSON.stringify({
        "headers": headers,
        "message": message,
    })
}

function readMessage(message){
    let response = JSON.parse(message);
    console.log(response)
    if (response.hasOwnProperty("message")
     && response.hasOwnProperty("headers")
     && response["headers"].hasOwnProperty("user")){
        console.log(response)
        return response;
    }
    return {}
}

function sendMessage() {
    let message = textarea.value;
    if (message) {
        textarea.value = "";
        socket.send(newMessage(
            {"session_key": session_key}, message
        ));
    }
}

function messageReceived(event) {
    let element = document.createElement("p");
    let response = readMessage(event.data)
    if (response) {
        element.innerHTML = `${response.headers.user}: ${response.message}`
        messages.appendChild(element);
    }
}

function newSocket(){
    return new WebSocket("ws://eliaseriksson.eu:2021");
}
let socket = newSocket();

socket.addEventListener("open", authenticate);
sendButton.addEventListener("click", sendMessage);
socket.addEventListener("message", messageReceived);

let textarea = document.getElementById("message");
let sendButton = document.getElementById("send");
let messages = document.evaluate("//div[@id='messages']/div", document).iterateNext();

function newSocket(){
    return new WebSocket("ws://5.172.146.246:2020");
}

let socket = newSocket();

sendButton.addEventListener("click", () => {
    let text = textarea.value;
    if (text) {
        socket.send(text);
        textarea.value = "";
    }
})

function onMessage(event) {
    let element = document.createElement("p");
    element.innerHTML = event.data;
    messages.appendChild(element);
}

socket.addEventListener("message", onMessage);

import Client from "./client.js";


const chatContainer = document.getElementById('chat-container');
const chat = document.getElementById('chat-content');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

const tabs = await chrome.tabs.query({currentWindow: true, active: true})
const url = tabs[0].url

let client

try{
    client = new Client(url)
}catch(e) {
    console.fatal(e)
    //TODO: should display this error msg on popup
}

const uid = await client.sendRequest('', client.videoId)
console.log(uid)

// Add a message to the chat
function addMessage(message, sender) {

    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chat.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function newQuestion(){
    const userQuestion = userInput.value.trim();
    if (userQuestion !== '') {

        addMessage(userQuestion, 'user');
        //const ans = "this is for css testing.. donot call the client... this is for css testing.. donot call the client...this is for css testing.. donot call the client...  "
        const ans = await client.getAnswer(userQuestion, uid)
        addMessage(ans, 'bot')
        userInput.value = '';
    }
}

userInput.addEventListener('keypress', async function(e) {
    if(e.key == 'Enter'){
        e.preventDefault()
        await newQuestion()
    }
})

// Handle the "Send" button click
sendButton.addEventListener('click', async function () {
    console.log('button clicked')
    await newQuestion()
});


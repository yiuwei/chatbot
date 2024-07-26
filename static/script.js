// Send user messages and post replies
function sendReplies() {
    // Define chatbot and check for empty input
    const chatInput= document.getElementById('user-text').value;
    if (chatInput.trim() === '') return;

    const chatBox = document.getElementById('box');
    chatBox.innerHTML += `<div class="replies user-replies">${chatInput}</div>`;

    // Send post request to query endpoint 
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'message': chatInput
        })
    })
    // Parse json response from server
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="replies bot-replies">${data.response}</div>`;
        document.getElementById('user-text').value = '';
        chatBox.scrollTop = chatBox.scrollHeight; 
    });
}

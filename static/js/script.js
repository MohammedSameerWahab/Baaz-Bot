// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const newChatButton = document.getElementById('new-chat-button');

    newChatButton.addEventListener('click', async () => {
        chatBox.innerHTML = '';
        appendMessage("Hello! A new chat session has started. How can I help?", 'bot', true);
        try {
            await fetch('/new_chat', { method: 'POST' });
        } catch (error) {
            console.error('Error starting new chat:', error);
        }
    });
    
    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const userMessage = messageInput.value.trim();
        if (userMessage === '') return;

        appendMessage(userMessage, 'user', true);
        messageInput.value = '';
        sendButton.disabled = true;

        const botMessageContainer = createBotMessageContainer();
        let fullResponseText = '';
        let buffer = '';
        let renderScheduled = false;

        const eventSource = new EventSource(`/stream_ask?message=${encodeURIComponent(userMessage)}`);

        // This function will render the buffered text
        const renderUpdate = () => {
            fullResponseText += buffer;
            buffer = ''; // Clear the buffer
            botMessageContainer.innerHTML = marked.parse(fullResponseText);
            chatBox.scrollTop = chatBox.scrollHeight;
            renderScheduled = false;
        };

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.error) {
                botMessageContainer.innerHTML = marked.parse(`Sorry, an error occurred: ${data.error}`);
                eventSource.close();
                sendButton.disabled = false;
                return;
            }
            
            // Add the new character to our buffer
            buffer += data.token;

            // Schedule a render update if one isn't already scheduled
            if (!renderScheduled) {
                renderScheduled = true;
                requestAnimationFrame(renderUpdate);
            }
        };

        eventSource.onerror = () => {
            // Stream is finished, do one final render to catch any remaining characters
            if (buffer.length > 0) {
                renderUpdate();
            }
            eventSource.close();
            sendButton.disabled = false;
        };
    });

    function appendMessage(text, sender, parseMarkdown = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        // Only parse with marked if we're sure it's the final content
        if (parseMarkdown) {
            messageElement.innerHTML = marked.parse(text);
        } else {
            messageElement.textContent = text;
        }
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function createBotMessageContainer() {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message');
        chatBox.appendChild(messageElement);
        return messageElement;
    }
});
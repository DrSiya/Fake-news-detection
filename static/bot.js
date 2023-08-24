class Chatbox{
    constructor(){
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }
        this.state = false;
        this.messages = [];
    }
    display(){
        const {openButton, chatBox, sendButton} = this.args;
        openButton.addEventListener('click',()=>this.toggleState(chatBox))
        sendButton.addEventListener('click',()=>this.onSentButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup",({String})=>{
            if (key === "Enter"){
                this.onSentButton(chatBox)
            }
        })
    }
    toggleState(chatbox){
        // show or Hide the chat box
        if (this.state)
            chatbox.classList.add('chatbox--active')
            else
                chatbox.classList.remove('chatbox__support')
    }

    onSentButton(chatbox){
        var textField = chatbox.querySelector('input');
        let msg = textField.value
        if (msg == "")
            return;
        let msg1 = {name:"User",message:msg}
        this.messages.push(msg1);

        fetch('http://127.0.0.1:5000/respond',{
          method: 'POST',
          body: JSON.stringify({message: msg}),
          mode: 'cors',
          headers:{
            'Content-Type':'application/json'
          },
        })
        .then(r => r.json())
        .then(r =>{
            let msg2 = { name: "Siya", message:r.answer};
            this.messages.push(msg2),
            this.updateChatText(chatbox)
            textField.value=''
        }).catch((error)=>{
            console.error('Error:',error);
            this.updateChatText(chatbox)
            textField.value=''
        });
    }

    updateChatText(chatbox){
        var html='';
        this.messages.slice().reverse().forEach(function(item,number){
            if (item.name === "Siya"){
                html += '<div class= "messages__item messages__item--visitor">'+item.message+'</div>'
            }
            else{
                html += '<div class= "messages__item messages__item--operator">'+item.message +'</div>'
            }
        });
        const chatmessages = chatbox.querySelector('.chatbox__messages');
        chatmessages.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
import axios from 'axios'

async function sendMessageToOpenAI(message: string){
    let response = await axios.post('http://localhost:8000/openai/invoke',
        {
            input:message,
            config:{},
            kwargs:{},
        }
    )
    return response
}
export { sendMessageToOpenAI }
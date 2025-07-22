
async function sendMessageToRecommender(message: string, sessionId: string) {
    console.log("send message to recommender", message);
    let response = await fetch('http://localhost:8000/recommender/stream', {
        method: 'post',
        body: JSON.stringify({
            input: { input: message },
            config: {
                configurable: {
                    session_id: sessionId
                }},
            kwargs: {},
        }),
    });
    return response;
}

async function getContentFromRecommenderResponse(response: any, messageList: any) {
    messageList[messageList.length - 1].content = ""
    const reader = response.body?.getReader()
    const decoder = new TextDecoder('utf-8')
    while (true) {
        const {done, value} = await reader?.read() || {done: true, value: ""}
        if (done) break
        const chunk = decoder.decode(value, {stream: true})
        let chunkStrArray = chunk.split("\n")
        for (let chunkStr of chunkStrArray) {
            if (chunkStr.trim().startsWith("data:")) {
                let jsonChunk = JSON.parse(chunkStr.replace("data:", "").trim())
                if (jsonChunk && jsonChunk.content) {
                   messageList[messageList.length - 1].content += jsonChunk.content
                }
            }
        }
    }    
}

export { sendMessageToRecommender, getContentFromRecommenderResponse }
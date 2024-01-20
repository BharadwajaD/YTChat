import OpenAI from 'openai'

let chat = []

const openai_client = new OpenAI({
    apiKey: process.env['OPENAI_KEY']
})

async function sendRequest(){

    const chatComp = await openai_client.chat.completions.create({
        messages: chat,
        model: 'gpt-3.5-turbo-16k'
    })

    const msg = chatComp.choices[0].message
    return msg.content
}

async function add_context(url){

    const regExp = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regExp);
    let videoId = match[1]

    const google_url =`http://video.google.com/timedtext?lang=en&v=${videoId}`;
    const res = await fetch(google_url).then(res => res.json())

    /*
    const captions = res.items
    if(captions.length == 0) return 'Sorry! This bot doesnot work well with this video'
    */

    const context = JSON.stringify(res)
    console.log(context)
    chat.push({'role': 'system', 'content': context})
}

export async function getAnswer(question='', isFirst = false, url = ''){

    if(isFirst){
        if(url == '') throw 'first request should contain url'
        add_context(url)
        return 'Got content from video'
    }

    chat.push({'role': 'user', 'content': question})
    const ans = sendRequest('question',question)
    chat.push({'role': 'assistant', 'content': ans})

    return ans
}

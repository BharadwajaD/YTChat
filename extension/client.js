export default class Client{


    constructor(url){

        this.server_url = "http://localhost:8000"
        const regExp = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regExp);

        if (match && match[1]) {
            this.videoId = match[1];
        } else {
            throw "Please select a youtube video"
        }

        console.log("Client constructor"+this.videoId)

    }

    async sendRequest(req, question, uid=-1){

        console.log('sendRequest '+question)

        let req_obj =  {
            'method': 'POST',
            'headers': {
                'Content-type': 'application/json',
                'Access-Control-Allow-Origin': 'no-cors',
                'User': uid,
            },
            'body': question
        }


        const res = await fetch(`${this.server_url}/${req}`, req_obj)
        const data = await res.json()
        return data
    }

    async getAnswer(question, uid){
        console.log(question)
        const ans = await this.sendRequest('question',question, uid)
        return ans
    }

}

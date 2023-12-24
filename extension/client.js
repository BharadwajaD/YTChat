export default class Client{


    constructor(url){
        this.server_url = "http://localhost:8000"
        this.url = url
    }

    async sendRequest(req, question, uid=-1){

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
        const ans = await this.sendRequest('question',question, uid)
        return ans
    }

}

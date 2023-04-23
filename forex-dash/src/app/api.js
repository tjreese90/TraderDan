import axios from "axios";

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

const response = (resp) => resp.data;

const request = {
    get: (url) => axios.get(url).then(response),
}

const endPoints = {
    account: () => request.get("/account"),
    headlines: () => request.get("/headlines"),
}

export default endPoints
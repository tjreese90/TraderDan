import axios from "axios";

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

const response = (resp) => resp.data;

const request = {
	get: (url) => axios.get(url).then(response),
};

const endPoints = {
	account: () => request.get("/account"),
	headlines: () => request.get("/headlines"),
	options: () => request.get("/options"),
	technicals: (p, g) => request.get(`/technicals/${p}/${g}`),
	prices: (p, g, c) => request.get(`/prices/${p}/${g}/${c}`),
};

export default endPoints;

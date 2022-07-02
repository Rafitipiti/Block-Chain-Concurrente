import axios from "axios";
import { ITransaction } from "./ITransaction";

const URL_BASE = "http://127.0.0.1:8000"

export const getPending = () => {
    return axios.get(URL_BASE+"/pending_tx")
}

export const getChain = () => {
    return axios.get(URL_BASE+"/chain")
}

export const newTransaction = (body: ITransaction) => {
    return axios.post(URL_BASE+"/new_transaction",{
       ...body
    })
}

export const doTheMine = () => {
    return axios.get(URL_BASE+'/mine')
}
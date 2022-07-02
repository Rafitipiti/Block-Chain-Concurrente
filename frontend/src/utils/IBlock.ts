import { ITransaction } from "./ITransaction";

export interface IBlock {
    hash: string,
    previous_hash: string,
    transactions: ITransaction[]
}


import { IBlock } from "./IBlock";

export interface IBlockchain{
    chain: IBlock[],
    length: number,
    peers: string[]
}
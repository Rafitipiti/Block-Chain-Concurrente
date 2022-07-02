import React, { useState } from 'react';
import 'styles/blockCard.scss';
import { IBlock } from 'utils/IBlock';
import TransactionCard from '../TransactionCard';

const BlockCard = (props: IBlock) => {
  return (
    <div className="blocks-container">
      <div>
        <b>BLOCK HASH:</b> {props.hash}
      </div>
      <div>
        <b>PREV HASH:</b> {props.previous_hash}
      </div>
      {props.transactions.map((transaction) => (
        <TransactionCard {...transaction} />
      ))}
    </div>
  );
};

export default BlockCard;

import React, { useState } from 'react';
import 'styles/transactionCard.scss';
import { ITransaction } from 'utils/ITransaction';

const TransactionCard = (props: ITransaction) => {
  return (
    <div className="transaction-container">
      <div>
        <b>FROM:</b> {props.from}
      </div>
      <div>
        <b>TO:</b> {props.to}
      </div>
      <div>
        <b>AMOUNT:</b> {props.amount}
      </div>
      <div>
        <b>CURRENCY:</b> {props.currency}
      </div>
    </div>
  );
};

export default TransactionCard;

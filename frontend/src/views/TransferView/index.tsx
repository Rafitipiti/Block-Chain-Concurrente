import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { newTransaction } from 'utils/fetchAPI';
import 'styles/transferView.scss';

const TransferView = () => {
  const navigate = useNavigate();
  const [from, setFrom] = useState<string>('');
  const [to, setTo] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [currency, setCurrency] = useState<string>('');

  const fetchNewTransaction = async () => {
    await newTransaction({ from, to, amount, currency });
  };

  const handleSubmit = () => {
    fetchNewTransaction();
    navigate('/');
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <div>FROM</div>
      <input
        type="text"
        name="from"
        onChange={(e) => setFrom(e.target.value)}
      />

      <div>TO</div>
      <input type="text" name="to" onChange={(e) => setTo(e.target.value)} />

      <div>AMOUNT</div>
      <input
        type="text"
        name="amount"
        onChange={(e) => setAmount(e.target.value)}
      />

      <div>CURRENCY</div>
      <input
        type="text"
        name="currency"
        onChange={(e) => setCurrency(e.target.value)}
      />

      <input
        className="button-input"
        type="submit"
        name="submit"
        value={'SEND MONEY'}
      />
    </form>
  );
};

export default TransferView;

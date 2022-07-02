import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { newTransaction } from 'utils/fetchAPI';

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
    <form onSubmit={handleSubmit}>
      <label>
        FROM:
        <input
          type="text"
          name="from"
          onChange={(e) => setFrom(e.target.value)}
        />
      </label>
      <label>
        TO:
        <input type="text" name="to" onChange={(e) => setTo(e.target.value)} />
      </label>
      <label>
        AMOUNT:
        <input
          type="text"
          name="amount"
          onChange={(e) => setAmount(e.target.value)}
        />
      </label>
      <label>
        CURRENCY:
        <input
          type="text"
          name="currency"
          onChange={(e) => setCurrency(e.target.value)}
        />
      </label>
      <input type="submit" name="submit" />
    </form>
  );
};

export default TransferView;

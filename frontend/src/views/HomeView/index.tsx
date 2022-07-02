import BlockCard from 'components/general/BlockCard';
import TransactionCard from 'components/general/TransactionCard';
import React, { useEffect, useState } from 'react';
import { doTheMine, getChain, getPending } from 'utils/fetchAPI';
import { IBlockchain } from 'utils/IBlockchain';
import { ITransaction } from 'utils/ITransaction';
import './homeView.scss';

const HomeView = () => {
  const [blockchain, setBlockchain] = useState<IBlockchain | null>(null);
  const [pending, setPending] = useState<ITransaction[] | null>([]);
  const [mined, setMined] = useState<boolean>(false);
  const fetchBlockchain = async () => {
    let response = await getChain();
    setBlockchain(response.data);
  };

  const fetchPending = async () => {
    let response = await getPending();
    setPending(response.data);
  };

  const fetchMine = async () => {
    let response = await doTheMine();
    setMined(true);
  };

  useEffect(() => {
    fetchBlockchain();
    fetchPending();
  }, [mined]);

  return (
    <>
      <div className="home__title">BLOCKCHAIN LIST</div>
      <div className="home-container">
        {blockchain?.chain.map((block) => (
          <BlockCard {...block} />
        ))}
      </div>
      <div className="home__title">PENDING TRANSACTIONS</div>
      <div className="home-container">
        <div className="pending-container">
          {pending?.length !== 0
            ? pending?.map((transaction) => (
                <TransactionCard {...transaction} />
              ))
            : 'NO PENDING TRANSACTIONS'}
        </div>
        <div>
          <button type="button" onClick={fetchMine} className="button-mine">
            MINE!!!
          </button>
        </div>
      </div>
    </>
  );
};

export default HomeView;

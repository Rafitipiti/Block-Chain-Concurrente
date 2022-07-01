import React from 'react';
import { useNavigate } from 'react-router-dom';

import './appCard.scss';

type cardProp = {
  text: string;
  src: string;
  to: string;
};

const AppCard = (props: cardProp) => {
  const { text, src, to } = props;

  const navigation = useNavigate();

  return (
    <button className='app-card' type='button' onClick={() => navigation(to)}>
      <img className='app-card__image' src={src} alt='app-banner' />
      <div className='app-card__text'>
        <div>{text}</div>
      </div>
    </button>
  );
};

export default AppCard;

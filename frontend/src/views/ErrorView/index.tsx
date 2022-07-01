import React from 'react';
import MyButton from 'components/ui/MyButton';
import { useNavigate } from 'react-router-dom';

import './errorView.scss';

const ErrorView = () => {
  const navigate = useNavigate();

  const navigateHome = () => navigate('/');
  return (
    <div className='error-container'>
      <div className='error-container__title'>ERROR 404</div>
      <MyButton text='RETURN HOME' color='red' onClick={navigateHome} />
    </div>
  );
};

export default ErrorView;

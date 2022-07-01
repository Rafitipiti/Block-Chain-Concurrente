import React from 'react';
import RouteController from 'components/routes/RouteController';

import Navbar from 'components/layout/Navbar';

import 'styles/index.scss';

const App = () => (
  <div className='content-wrapper'>
    <Navbar />
    <RouteController />
  </div>
);

export default App;

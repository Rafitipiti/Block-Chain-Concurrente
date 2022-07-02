import React from 'react';
import { Route, Routes } from 'react-router-dom';
import appRoutes from 'routes';
import { getChain, getPending, newTransaction } from 'utils/fetchAPI';
import ErrorView from 'views/ErrorView';
import HomeView from 'views/HomeView';
import TransferView from 'views/TransferView';

const RouteController = () => {
  return (
    <Routes>
      <Route path={appRoutes.HOME} element={<HomeView />} />
      <Route path={appRoutes.TRANSFER} element={<TransferView />} />
      <Route path="*" element={<ErrorView />} />
    </Routes>
  );
};

export default RouteController;

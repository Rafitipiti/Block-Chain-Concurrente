import React from 'react';
import { Route, Routes } from 'react-router-dom';
import appRoutes from 'routes';
import ErrorView from 'views/ErrorView';
import HomeView from 'views/HomeView';

const RouteController = () => (
  <Routes>
    <Route path={appRoutes.HOME} element={<HomeView />} />
    <Route path="*" element={<ErrorView />} />
  </Routes>
);

export default RouteController;

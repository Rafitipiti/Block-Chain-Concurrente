import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

import listIcon from 'assets/list.png';
import exitIcon from 'assets/x.png';

import './navbar.scss';
import appRoutes from 'routes';

const Navbar = () => {
  const [sidebar, setSideBar] = useState<boolean>(false);

  const showSideBar = () => {
    setSideBar(!sidebar);
  };

  return (
    <>
      <div className="navbar">
        <div className="navbar-left">
          <button
            type="button"
            className="side-bar__button"
            onClick={showSideBar}
          >
            <img className="side-bar__icon" src={listIcon} alt="list-icon" />
          </button>

          <NavLink to="/" className="navbar__title">
            RFDS
          </NavLink>
        </div>

        <ul className="navbar__link-container">
          <NavLink
            to={appRoutes.HOME}
            className={({ isActive }) =>
              isActive ? 'navbar__link--active' : 'navbar__link'
            }
          >
            HOME
          </NavLink>
          <NavLink
            to={appRoutes.TRANSFER}
            className={({ isActive }) =>
              isActive ? 'navbar__link--active' : 'navbar__link'
            }
          >
            TRANSFER
          </NavLink>
        </ul>
      </div>

      <nav
        className={sidebar ? 'side-bar-container active' : 'side-bar-container'}
      >
        <ul className="side-bar-items">
          <button
            type="button"
            className="side-bar__button"
            onClick={showSideBar}
          >
            <img className="side-bar__icon" src={exitIcon} alt="exit-icon" />
          </button>
          <li className="side-menu__item side-bar-text">MENU</li>
          <li className="side-menu__item">
            <NavLink
              to={appRoutes.HOME}
              className={({ isActive }) =>
                isActive ? 'sidebar__link--active' : 'sidebar__link'
              }
              onClick={showSideBar}
            >
              HOME
            </NavLink>
          </li>
          <li className="side-menu__item">
            <NavLink
              to={appRoutes.TRANSFER}
              className={({ isActive }) =>
                isActive ? 'sidebar__link--active' : 'sidebar__link'
              }
              onClick={showSideBar}
            >
              TRANSFER
            </NavLink>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default Navbar;

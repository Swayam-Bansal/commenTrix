// src/NavBar.js
import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

function NavBar({ dataRetrieved }) {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <NavLink to="/" end activeclassname="active">
            Home
          </NavLink>
        </li>
        {dataRetrieved && (
          <>
            <li>
              <NavLink to="/video1" activeclassname="active">
                Video1
              </NavLink>
            </li>
            <li>
              <NavLink to="/video2" activeclassname="active">
                Video2
              </NavLink>
            </li>
            <li>
              <NavLink to="/comparison" activeclassname="active">
                Comparison
              </NavLink>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default NavBar;

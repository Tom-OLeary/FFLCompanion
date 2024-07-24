import './App.css';
// import Header from "./components/Header";
// import Sheet from "./components/Sheet";
// import DataGrid from "./components/DataGrid";
import env from "react-dotenv";
// import GridTest from "./components/GridTest";
// import TeamCard from "./components/TeamCard";
// import SpacingGrid from "./components/SpacingGrid";
// import MenuDrawer from "./components/MenuDrawer";
import React from "react";
import { Routes, Route } from 'react-router-dom';
import Home from "./components/Home";
import MenuDrawer from "./components/MenuDrawer";
import Projection from "./components/Projection";

function App() {
    let url = (env.NODE_ENV === 'production') ? 'https://www.troleary.com/api/' : 'http://127.0.0.1:8000/api/'
    // if (env.NODE_ENV === 'development') {
    //   url = 'http://127.0.0.1:8000/api/'
    // }
    // else if (env.NODE_ENV === 'production') {
    //   url = 'https://www.troleary.com/api/'
    // }
    // else {
    //   url = 'http://127.0.0.1:8000/api/'
    // }

  return (
    <>
        <MenuDrawer />
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="projections" element={<Projection />} />
        </Routes>
    </>
  );
}

export default App;

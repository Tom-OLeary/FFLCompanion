import './App.css';
// import React, {useEffect, useState} from "react";
import { Routes, Route } from 'react-router-dom';
import Home from "./components/Home";
import MenuDrawer from "./components/MenuDrawer";
import Projection from "./components/Projection";
import env from 'react-dotenv';
import Login from "./components/Login";
import Trade from "./components/trades/Trade";
import TeamStats from "./components/TeamStats";
import InfoDrawer from "./components/InfoDrawer";

function App() {
    let url = (env.NODE_ENV === 'production') ? 'https://www.troleary.com/api/' : 'http://127.0.0.1:8000/api/'

    return (
        <>
            <div className={"column-three"}>
                <MenuDrawer/>
                <InfoDrawer url={url}/>
            </div>
            <Routes>
                <Route path="/" element={<Login url={url} />} />
                <Route path="home" element={<Home url={url} />} />
                <Route path="projections" element={<Projection url={url} />} />
                <Route path="stats" element={<TeamStats url={url} />} />
                <Route path="trades" element={<Trade url={url} />} />
            </Routes>
        </>
    );
}

export default App;

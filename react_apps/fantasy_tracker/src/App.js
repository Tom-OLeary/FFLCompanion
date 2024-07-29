import './App.css';
// import Header from "./components/Header";
// import Sheet from "./components/Sheet";
// import DataGrid from "./components/DataGrid";
// import GridTest from "./components/GridTest";
// import TeamCard from "./components/TeamCard";
// import SpacingGrid from "./components/SpacingGrid";
// import MenuDrawer from "./components/MenuDrawer";
import React, {useEffect, useState} from "react";
import { Routes, Route } from 'react-router-dom';
import Home from "./components/Home";
import MenuDrawer from "./components/MenuDrawer";
import Projection from "./components/Projection";
import LeaderPanel from "./components/LeaderPanel";
import env from 'react-dotenv';
import Login from "./components/Login";
import TEMP from "./components/TEMP";
import Trade from "./components/trades/Trade";

function App() {
    // console.log(env.API_URL)
    let url = (env.NODE_ENV === 'production') ? 'https://www.troleary.com/api/' : 'http://127.0.0.1:8000/api/'

    return (
        <>
            <div className={"column-three"}>
                <MenuDrawer/>
                {/*<div id="headerTitle" >{data.name}</div>*/}
                {/*<div id="headerTitle">Norton</div>*/}

                <LeaderPanel url={url}/>
                {/*<TEMP />*/}
            </div>
            <Routes>
                <Route path="/" element={<Login url={url} />} />
                <Route path="home" element={<Home url={url} />} />
                <Route path="projections" element={<Projection url={url} />} />
                {/*<Route path="stats" element={<TeamStat url={url} />} />*/}
                <Route path="trades" element={<Trade url={url} />} />

            </Routes>
        </>
    );
}

export default App;

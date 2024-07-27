// import React from 'react'
//
// const App = () => {
//   return (
//     <div>Hello, World!</div>
//   )
// }
//
// export default App
import './App.css';
// import Header from "./components/Header";
// import Sheet from "./components/Sheet";
// import DataGrid from "./components/DataGrid";
import env from "react-dotenv";
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

function App() {
    let url = (env.NODE_ENV === 'production') ? 'https://www.troleary.com/api/' : 'http://127.0.0.1:8000/api/'
    // const [data, setData] = useState([])
    // useEffect(() => {
    // fetch(url + 'leagues/1/')
    //     .then(res => res.json())
    //     .then(json => {
    //         console.log(json);
    //         setData(json)
    //     })
    // }, []);

    return (
        <>
            <div className={"column-three"}>
                <MenuDrawer/>
                {/*<div id="headerTitle" >{data.name}</div>*/}
                <div id="headerTitle">Norton</div>

                <LeaderPanel/>
            </div>
            <Routes>
                <Route path="/" element={<Home url={url} />} />
                <Route path="projections" element={<Projection url={url} />} />
            </Routes>
        </>
    );
}

export default App;

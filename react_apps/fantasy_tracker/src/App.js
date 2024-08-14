import './App.css';
import {Routes, Route} from 'react-router-dom';
import Home from "./components/Home";
import MenuDrawer from "./components/MenuDrawer";
import Projection from "./components/Projection";
import Login from "./components/Login";
import Trade from "./components/trades/Trade";
import TeamStats from "./components/TeamStats";
import InfoDrawer from "./components/InfoDrawer";
import Notes from "./components/Notes";
import React from "react";
import Account from "./components/Account";
import ChangePassword from "./components/account/ChangePassword";
import Trends from "./components/Trends";
import MyTeam from "./components/MyTeam";

function App() {
    let url = (process.env.REACT_APP_NODE_ENV === 'production') ? process.env.REACT_APP_HOST_URL : 'http://127.0.0.1:8000/'
    let apiUrl = url + 'api/';
    let loginUrl = url + 'login/?';

    const loadDemo = () => {
        let demoLogin = loginUrl
            + 'username=' + process.env.REACT_APP_DEMO_USER
            + '&password=' + process.env.REACT_APP_DEMO_PW;

        fetch(demoLogin)
            .then(res => res.json())
            .then(json => {
                let token = json.token;
                if (token) { window.localStorage.setItem('USER_STATE', token); }
                else { console.log(json.error); }
            })
            .catch(err => console.log(err));
    }
    if (window.localStorage.getItem('USER_STATE') === null) { loadDemo(); }

    return (
        <>
            <div style={{
                flexGrow: 1,
                display: 'flex',
                height: "12%",
                width: "100%",
                position: "fixed",
                zIndex: 2,
                top: 0,
                overflowX: "hidden",
                paddingTop: 20,
                backgroundColor: "rgba(25,23,23,0.56)"
            }}>
                <MenuDrawer/>
                <InfoDrawer url={apiUrl}/>
            </div>
            <Routes>
                <Route path="/" element={<Login url={loginUrl} />} />
                <Route path="home" element={<Home url={apiUrl} />} />
                <Route path="projections" element={<Projection url={apiUrl} />} />
                <Route path="stats" element={<TeamStats url={apiUrl} />} />
                <Route path="trades" element={<Trade url={apiUrl} />} />
                <Route path="notes" element={<Notes />} />
                <Route path="account" element={<Account url={url} />} />
                <Route path="change-password" element={<ChangePassword url={url} />} />
                <Route path="trends" element={<Trends url={apiUrl} />} />
                <Route path="my-team" element={<MyTeam url={apiUrl}/>} />
            </Routes>
        </>
    );
}

export default App;

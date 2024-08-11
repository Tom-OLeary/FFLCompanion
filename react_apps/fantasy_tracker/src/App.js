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
import Links from "./components/Links";
import React from "react";
import Account from "./components/Account";
import ChangePassword from "./components/account/ChangePassword";
import Trends from "./components/Trends";

function App() {
    // TODO provide deployment url
    let url = (process.env.REACT_APP_NODE_ENV === 'production') ? 'https://www.some-app.com/' : 'http://127.0.0.1:8000/'
    let apiUrl = url + 'api/';
    let loginUrl = url + 'login/?';

    const loadDemo = () => {
        loginUrl = loginUrl
            + 'username=' + process.env.REACT_APP_DEMO_USER
            + '&password=' + process.env.REACT_APP_DEMO_PW;

        fetch(loginUrl)
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
            <div className={"column-three"}>
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
                <Route path="links" element={<Links />} />
                <Route path="account" element={<Account url={url} />} />
                <Route path="change-password" element={<ChangePassword url={url} />} />
                <Route path="trends" element={<Trends url={apiUrl} />} />
            </Routes>
        </>
    );
}

export default App;

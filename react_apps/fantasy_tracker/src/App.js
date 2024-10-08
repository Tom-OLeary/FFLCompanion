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
import {setAccessToken} from "./api";

function App() {
    let url = (process.env.REACT_APP_NODE_ENV === 'production') ? process.env.REACT_APP_HOST_URL : 'http://127.0.0.1:8000/'
    let loginUrl = url + 'login/?';

    const loadDemo = () => {
        let demoLogin = loginUrl
            + 'username=' + process.env.REACT_APP_DEMO_USER
            + '&password=' + process.env.REACT_APP_DEMO_PW;

        fetch(demoLogin)
            .then(res => res.json())
            .then(json => {
                let token = json.token;
                if (token) {
                    window.localStorage.setItem('USER_STATE', token);
                    setAccessToken(token);
                }
                else { console.log(json.error); }
            })
            .catch(err => console.log(err));
    }

    (window.localStorage.getItem('USER_STATE') === null)
        ? loadDemo()
        : setAccessToken(window.localStorage.getItem('USER_STATE'));

    return (
        <>
            <div style={{
                flexGrow: 1,
                display: 'flex',
                height: "12%",
                width: "100%",
                position: "fixed",
                zIndex: 6,
                top: 0,
                overflowX: "hidden",
                paddingTop: 20,
                backgroundColor: "rgba(25,23,23,0.56)"
            }}>
                <MenuDrawer />
                <InfoDrawer />
            </div>
            <Routes>
                <Route path="/" element={<Login url={loginUrl} />} />
                <Route path="home" element={<Home />} />
                <Route path="projections" element={<Projection />} />
                <Route path="stats" element={<TeamStats />} />
                <Route path="trades" element={<Trade />} />
                <Route path="notes" element={<Notes />} />
                <Route path="account" element={<Account url={url} />} />
                <Route path="change-password" element={<ChangePassword url={url} />} />
                <Route path="trends" element={<Trends />} />
                <Route path="my-team" element={<MyTeam />} />
            </Routes>
        </>
    );
}

export default App;

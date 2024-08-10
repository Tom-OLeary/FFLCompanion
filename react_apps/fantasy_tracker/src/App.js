import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from "./components/Home";
import MenuDrawer from "./components/MenuDrawer";
import Projection from "./components/Projection";
import env from 'react-dotenv';
import Login from "./components/Login";
import Trade from "./components/trades/Trade";
import TeamStats from "./components/TeamStats";
import InfoDrawer from "./components/InfoDrawer";
import Notes from "./components/Notes";
import Links from "./components/Links";
import React, {useState} from "react";

export const UserContext = React.createContext(null);

function App() {
    // TODO provide deployment url
    let url = (env.NODE_ENV === 'production') ? 'https://www.some-app.com/api/' : 'http://127.0.0.1:8000/api/'
    const [user, setUser] = useState(null);

    return (
        <>
            <div className={"column-three"}>
                <MenuDrawer/>
                <InfoDrawer url={url}/>
            </div>
            <UserContext.Provider value={{ user: user, setUser: setUser }}>
            <Routes>
                <Route path="/" element={<Login url={url} />} />
                <Route path="home" element={<Home url={url} />} />
                <Route path="projections" element={<Projection url={url} />} />
                <Route path="stats" element={<TeamStats url={url} />} />
                <Route path="trades" element={<Trade url={url} />} />
                <Route path="notes" element={<Notes />} />
                <Route path="links" element={<Links />} />
            </Routes>
            </UserContext.Provider>
        </>
    );
}

export default App;

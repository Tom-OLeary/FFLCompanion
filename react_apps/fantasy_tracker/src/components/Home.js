import Header from "./home/Header";
import React from "react";
import LeaderBoard from "./home/LeaderBoard";
import '../css/Header.css';

function Home() {

  return (
    <>
        <div style={{marginTop: 150}}>
        <Header />
        </div>
        <h1 className="home-title">
            LEADERBOARD
        </h1>
        <LeaderBoard />
    </>
  );
}

export default Home;

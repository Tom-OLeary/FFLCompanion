import Header from "./home/Header";
import React from "react";
import LeaderBoard from "./home/LeaderBoard";
import '../css/Header.css';

function Home(props) {

  return (
    <>
        <div style={{marginTop: 150}}>
        <Header url={props.url}/>
        </div>
        <h1 className="home-title">
            LEADERBOARD
        </h1>
        <LeaderBoard url={props.url} />
    </>
  );
}

export default Home;

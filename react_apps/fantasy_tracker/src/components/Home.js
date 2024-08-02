import Header from "./home/Header";
import React from "react";
import LeaderBoard from "./home/LeaderBoard";

function Home(props) {

  return (
    <>
        <Header url={props.url}/>
        <LeaderBoard url={props.url} />
    </>
  );
}

export default Home;

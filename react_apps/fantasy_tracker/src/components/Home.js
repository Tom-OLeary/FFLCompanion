import Header from "./home/Header";
import React, {useContext} from "react";
import LeaderBoard from "./home/LeaderBoard";
import {UserContext} from "../App";

function Home(props) {
    // const { user, setUser } = useContext(UserContext);

  return (
    <>
        <Header url={props.url}/>
        <LeaderBoard url={props.url} />
    </>
  );
}

export default Home;

import React from "react";
import StatTable from "./components/stats/StatTable";

function TeamStats(props) {

  return (
    <>
        <StatTable url={props.url} />
    </>
  );
}

export default TeamStats;

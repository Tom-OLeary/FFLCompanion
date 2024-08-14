import React from "react";
import StatTable from "./stats/StatTable";
import '../css/Stats.css';

function TeamStats(props) {

  return (
    <>
        <div style={{marginTop: 150}}>
            <h1 className="stats-title">All Time Team Stats</h1>
        <StatTable url={props.url} />
        </div>
    </>
  );
}

export default TeamStats;

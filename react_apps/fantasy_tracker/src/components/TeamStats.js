import React from "react";
import StatTable from "./stats/StatTable";
import '../css/Stats.css';

function TeamStats() {

  return (
    <>
        <div style={{marginTop: 150}}>
            <h1 className="stats-title">All Time Team Stats</h1>
        <StatTable />
        </div>
    </>
  );
}

export default TeamStats;

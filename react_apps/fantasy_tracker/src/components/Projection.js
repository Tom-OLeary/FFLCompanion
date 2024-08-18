import React from "react";
import PlayerStats from "./projections/PlayerStats";
import '../css/Stats.css';

function Projection() {

  return (
    <>
        <div style={{marginTop: 150}}>
            <h1 className="stats-title">2024 Player Projections</h1>
            <PlayerStats />
        </div>
    </>
  );
}

export default Projection;

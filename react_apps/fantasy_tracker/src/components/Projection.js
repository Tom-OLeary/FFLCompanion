import React from "react";
import PlayerStats from "./projections/PlayerStats";
import '../css/Stats.css';

function Projection(props) {

  return (
    <>
        <div style={{marginTop: 150}}>
            <h1 className="stats-title">2024 Player Projections</h1>
            <PlayerStats url={props.url}/>
        </div>
    </>
  );
}

export default Projection;

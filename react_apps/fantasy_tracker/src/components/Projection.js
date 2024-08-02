import React from "react";
import PlayerStats from "./projections/PlayerStats";

function Projection(props) {

  return (
    <>
        <PlayerStats url={props.url} />
    </>
  );
}

export default Projection;

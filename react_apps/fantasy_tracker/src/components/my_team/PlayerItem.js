import React from "react";
import {Container, Stack} from "@mui/material";
import '../../css/MyTeam.css';
import '../../css/Progress.css';
import {styled} from "@mui/material/styles";
import Paper from "@mui/material/Paper";

export default function PlayerItem(props) {
    return (
        <>
            {/*<span>QB</span>*/}
            {/*<span>Player 1</span>*/}
            {/*<button >Add</button>*/}
                <input name="QB"/>
                <input name="RB1"/>
                <input name="RB2"/>
                <input name="WR1"/>
                <input name="WR2"/>
                <input name="TE"/>
                <input name="FLEX"/>
                <input name="DEF"/>
        </>
    );
}
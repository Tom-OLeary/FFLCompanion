import React from "react";
import {Container, CssBaseline} from "@mui/material";
import Box from "@mui/material/Box";
import '../css/MyTeam.css';
import Divider from "@mui/material/Divider";

function MyTeam(props) {
    const columns = [
        'Pos.',
        'Player',
        'Team',
        'Opp.',
        'Pass Yds.',
        'Pass TD',
        'Rec. Yds.',
        'Rec. TD',
        'Receptions',
        'Rush Yds.',
        'Rush TD',
        'FPts.'

    ]

    return (
        <React.Fragment>
            <CssBaseline/>
            <Container maxWidth="375px" style={{marginTop: 30}}>
                <Box sx={{bgcolor: '#6e7071', height: '50vh'}}>
                    <div style={{textAlign: 'center'}}>Starters</div>
                    <div className="box-columns">
                        {columns.map((col, index) => (<span key={index}>{col}</span>))}
                    </div>
                    <div>QB</div>
                    <Divider style={{backgroundColor: 'gold'}}/>

                    <div>RB</div>
                    <Divider style={{backgroundColor: 'gold'}}/>
                    <div>RB</div>
                    <Divider style={{backgroundColor: 'gold'}}/>

                    <div>WR</div>
                    <Divider style={{backgroundColor: 'gold'}}/>
                    <div>WR</div>
                    <Divider style={{backgroundColor: 'gold'}}/>

                    <div>FLEX</div>
                    <Divider style={{backgroundColor: 'gold'}}/>
                    <div>DEF</div>
                    <Divider style={{backgroundColor: 'gold'}}/>

                </Box>
                <Divider style={{backgroundColor: 'black'}}/>
                <Box sx={{bgcolor: '#6e7071', height: '50vh'}}>
                    <div style={{textAlign: 'center'}}>Bench</div>
                    <div>ITEM 1</div>

                </Box>
            </Container>
        </React.Fragment>
    );
}

export default MyTeam;
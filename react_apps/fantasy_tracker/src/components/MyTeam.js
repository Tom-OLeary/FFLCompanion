import React from "react";
import {Container} from "@mui/material";
import '../css/MyTeam.css';
import '../css/Progress.css';

function MyTeam(props) {
    // const columns = [
    //     'Pos.',
    //     'Player',
    //     'Team',
    //     'Opp.',
    //     'Pass Yds.',
    //     'Pass TD',
    //     'Rec. Yds.',
    //     'Rec. TD',
    //     'Receptions',
    //     'Rush Yds.',
    //     'Rush TD',
    //     'FPts.'
    //
    // ]

    return (
        <div style={{marginTop: 150}}>
            <Container maxWidth="375px" style={{marginTop: 30}}>
                <div className="progress-description">
                    Page is in progress...
                    <br/>
                    <br/>
                    When finished you will be able to:
                    <br/>
                    <br/>
                    <li>Import 2024 Rosters & Weekly Stats</li>
                    <li>Imported Stats will automatically be added to leaderboard totals</li>
                    <li>Set your weekly lineup, which will be tracked for future tools to analyze points lost/gained
                    </li>
                    <li>Positional Strengths & Weaknesses analysis (Rankings against league avg/totals)</li>
                    <li>CSV Downloads and Full Draft History</li>
                    <li>This is just my short list. Let me know if there's anything else you're looking for.</li>

                </div>

            </Container>
        </div>

    );
}

export default MyTeam;
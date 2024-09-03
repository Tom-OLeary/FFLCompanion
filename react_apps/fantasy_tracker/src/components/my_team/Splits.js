import {Container, Stack} from "@mui/material";
import Item from "./Item";
import React from "react";

export default function Splits(players) {
    const days = [
        'Sunday',
        'Monday',
        'Thursday',
    ];

    const columns = [
        // 'Player',
        // 'Team',
        // 'Opp.',
        'Pass Yds.',
        'Pass TD',
        'Pass Att.',
        'Completions',
        'Int',
        'Rec. Yds.',
        'Rec. TD',
        'Receptions',
        'Targets',
        'Rush Yds.',
        'Rush TD',
        'Rush Att.',
        // 'FPts.'
    ];
    const statColumns = []
    for (const k in players[0]['stats']) {statColumns.push(k)}

    return (
        <>
            <Container maxWidth="875px" style={{
                marginTop: 20,
                marginBottom: 40,
                backgroundColor: 'whitesmoke',
                height: '130vh',
                width: '90%',
            }}>
                <Stack spacing={.5}>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        marginBottom: 5,
                    }}>
                        <span style={{marginLeft: 50, marginRight: 50, fontWeight: 'bold'}}>Player</span>
                        {columns.map((column, index) => (
                            <span key={index} style={{fontWeight: 'bold'}}>
                                    {column}
                                </span>
                        ))}
                    </div>
                    {
                        players.map((player, index) => (
                            <Item key={index} style={{
                                marginTop: 3,
                            }}>
                                <span key={index} style={{width: 130}}>{player['name']}</span>
                                {
                                    statColumns.map((column, index) => (
                                        <span key={index}>
                                                {player['stats'][column]}
                                            </span>
                                    ))
                                }
                            </Item>
                        ))
                    }
                </Stack>
            </Container>
        </>
    );
}

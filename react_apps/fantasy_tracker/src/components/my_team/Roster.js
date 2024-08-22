import React from "react";
import {Container, Stack} from "@mui/material";
import '../../css/MyTeam.css';
import '../../css/Progress.css';
import {styled} from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Item from "./Item";

export default function Roster(props) {
    const positions = [
        'QB',
        'RB',
        'RB',
        'WR',
        'WR',
        'TE',
        'FLEX',
        'DEF',
    ];
    const columns = [
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
    ];
    const statColumns = [
        ''
    ]
    const players = props.data['players'];
    const emptyRows = props.data['player_limit'] - players.length;
    [...Array(emptyRows)].map((row, i) => { players.push({}); });

    return (
        <>
            <Stack
                spacing={.25}
                direction="row"
                marginLeft={10}
                marginTop={20}
            >
                <Item style={{width: 48}}>
                    <Stack spacing={2} marginTop={6}>
                        {/*{positions.map((pos, index) => (*/}
                        {/*    <span key={index}>*/}
                        {/*        {pos}*/}
                        {/*    </span>*/}
                        {/*))}*/}
                    </Stack>
                </Item>
                <Container maxWidth="775px" style={{
                    marginTop: 20,
                    marginBottom: 40,
                    backgroundColor: 'whitesmoke',
                    height: '70vh',
                    width: '90%',
                }}>
                    <Stack spacing={.5}>
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                        }}>
                            {columns.map((column, index) => (
                                <span key={index}>{column}</span>
                            ))}
                        </div>
                        {
                            players.map((player, index) => (
                                <Item key={index}>
                                    {
                                        statColumns.map((column, index) => (
                                            <span key={index}>{column}</span>
                                        ))
                                    }
                                </Item>
                            ))
                        }
                    </Stack>
                </Container>
            </Stack>
        </>
    );
}
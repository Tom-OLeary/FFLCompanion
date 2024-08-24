import React from "react";
import {Container, Stack} from "@mui/material";
import '../../css/MyTeam.css';
import '../../css/Progress.css';
import '../../css/LeaderBoard.scss';
import Item from "./Item";

export default function Roster(props) {
    const pages = [
        'Add / Drop',
        'Totals',
        'Splits',
        'Advanced',
        'Rankings',
        'Lineups',
        'Clear Roster'
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
    const statColumns = [
        'pass_yds',
        'pass_td',
        'pass_attempts',
        'pass_completions',
        'interceptions',
        'receiving_yards',
        'receiving_td',
        'receptions',
        'targets',
        'rush_yds',
        'rush_td',
        'rush_attempts',
    ]

    const players = props.data['players'];
    const emptyRows = props.data['player_limit'] - players.length;
    for (let i = 0; i < emptyRows; i++) {
        players.push({
            'name': '-',
            'stats': {
                'pass_yds': 0,
                'pass_td': 0,
                'pass_attempts': 0,
                'pass_completions': 0,
                'interceptions': 0,
                'receiving_yards': 0,
                'receiving_td': 0,
                'receptions': 0,
                'targets': 0,
                'rush_yds': 0,
                'rush_td': 0,
                'rush_attempts': 0,
            }
        });
    }

    const handleClick = (e) => {
        alert('Feature currently in progress. Expected to be live before week 1 begins.');
    }

    return (
        <>
            <Stack
                spacing={.25}
                direction="row"
                marginLeft={10}
                marginTop={20}
            >
                <Item style={{width: 100}}>
                    <Stack spacing={2} marginTop={4}>
                        {pages.map((pos, index) => (
                            <button
                                key={index}
                                className="button button1"
                                style={{
                                    fontSize: 12,
                                    height: 40,
                                }}
                                onClick={handleClick}
                            >
                                {pos}
                            </button>
                        ))}
                    </Stack>
                </Item>
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
            </Stack>
        </>
    );
}
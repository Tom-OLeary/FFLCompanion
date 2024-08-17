import React from "react";
import {Container, Stack} from "@mui/material";
import '../css/MyTeam.css';
import '../css/Progress.css';
import {styled} from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import PlayerItem from "./my_team/PlayerItem";

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

    const positions = [
        'QB',
        'RB',
        'RB',
        'WR',
        'WR',
        'TE',
        'FLEX',
        'DEF',
    ]

    const Item = styled(Paper)(({theme}) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        // textAlign: 'left',
        color: theme.palette.text.secondary,
        justifyContent: 'space-between',
        display: 'flex',
    }));

    function search(formData) {
        const query = formData.get("query");
        alert(`You searched for '${query}'`);
    }

    const handleClick = () => {

    }


    return (
        <>
            <Stack
                spacing={.25}
                direction="row"
                marginLeft={10}
                marginTop={20}
            >
            <Item
                style={{width: 48}}>
                <Stack spacing={2} marginTop={6}>
                        {positions.map((pos, index) => (
                            <span key={index}>
                                {pos}
                            </span>
                        ))}
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
                        {/*<div style={{*/}
                        {/*    display: 'flex',*/}
                        {/*    justifyContent: 'space-between',*/}
                        {/*}}>*/}
                        {/*    {columns.map((column, index) => (*/}
                        {/*        <span key={index}>{column}</span>*/}
                        {/*    ))}*/}
                        {/*</div>*/}
                        {/*<Player onClick={handleClick}>*/}
                        {/*    <PlayerItem />*/}
                        {/*</Player>*/}
                        {/*<Player>RB Player 2</Player>*/}
                        <form action={search}>
                            <Item>
                                <input name="QB" style={{height: 0}}/>

                            </Item>
                                    <Item>
                                <input name="QB" style={{height: 0}}/>

                            </Item>
                            <Item>
                                <input name="QB" style={{height: 0}}/>

                            </Item>
                            <Item>
                                <input name="QB" style={{height: 0}}/>

                            </Item>
                            <Item>
                                <input name="QB" style={{height: 0}}/>

                            </Item>
                            <Item>
                                <button type="submit">Search</button>
                            </Item>
                        </form>
            </Stack>

        </Container>
                {/*</Player>*/}
            </Stack>

        </>

    );
}

export default MyTeam;
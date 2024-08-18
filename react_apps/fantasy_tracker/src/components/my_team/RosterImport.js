import React from "react";
import {Container, Stack} from "@mui/material";
import '../../css/MyTeam.css';
import '../../css/Progress.css';
import {styled} from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Item from "./Item";


const ImportRow = (props) => {
    return (
        <Item >
            {
                [...Array(6)].map((_, i) => (
                    // const name = props.pos + i.toString();
                    <Item>
                        <input name={props.pos + i.toString()} style={{height: 0}}/>
                    </Item>
                ))
            }
            <Item>
                <span>{props.pos}</span>
            </Item>
        </Item>
    );
}

export default function RosterImport(props) {
    // const endpoint = props.url + 'player-search/?'
    const positions = [
        'QB',
        'RB',
        'WR',
        'TE',
        'DEF',
    ]

    const searchPlayers = (playerMap) => {

    }
    function search(formData) {
        let positionMap = {
            'QB': [],
            'RB': [],
            'WR': [],
            'TE': [],
            'DEF': [],
        }
        positions.forEach((position) => {
            [...Array(6)].forEach((_, i) => {
                let k = position + i.toString();
                let query = formData.get(k);
                if (query) { positionMap[position].push(query); }
            })
            positionMap[position] = positionMap[position].toString();
        })
        // console.log(positionMap)
    }

    return (
        <>
            <Stack
                spacing={.25}
                direction="row"
                marginLeft={10}
                marginTop={20}
            >
                <Item style={{width: 48}}/>

                <Container maxWidth="775px" style={{
                    marginTop: 20,
                    marginBottom: 40,
                    backgroundColor: 'whitesmoke',
                    height: '70vh',
                    width: '90%',
                }}>
                    <Stack spacing={.5} direction="row">
                        <form action={search}>
                            {
                                positions.map((pos, index) => (
                                    <ImportRow  key={index} pos={pos}/>
                                ))
                            }
                            <Item>
                                <button type="submit">Search</button>
                            </Item>
                        </form>
                    </Stack>
                </Container>
            </Stack>
        </>
    );
}
import React, {useState} from 'react';
import {Container, Stack} from '@mui/material';
import '../../css/MyTeam.css';
import '../../css/Progress.css';
import '../../css/LeaderBoard.scss';
import Item from './Item';
import {useNavigate} from 'react-router-dom';
import PlayerDetail from '../../stores/PlayerDetail';
import {RosterActions, PlayerActions} from '../../actions/actionIndex';

const ImportRow = (props) => {
    let defaultVals = ['', '', '', '', '', ''];
    if (props.results) { defaultVals = props.results[props.pos]; }

    return (
        <Item style={{marginTop: 10}}>
            {
                [...Array(6)].map((_, i) => (
                    <Item key={i} >
                        <input name={props.pos + i.toString()} style={{height: 0, width: '95%'}} defaultValue={defaultVals[i]} />
                    </Item>
                ))
            }
            <Item>
                <span>{props.pos}</span>
            </Item>
        </Item>
    );
}

const abbreviations = [
   'ARI',
   'ATL',
   'BAL',
   'BUF',
   'CAR',
   'CHI',
   'CIN',
   'CLE',
   'DAL',
   'DEN',
   'DET',
   'GB',
   'HOU',
   'IND',
   'JAX',
   'KC',
   'MIA',
   'MIN',
   'NE',
   'NO',
   'NYG',
   'NYJ',
   'LV',
   'PHI',
   'PIT',
   'LAC',
   'SF',
   'SEA',
   'LAR',
   'TB',
   'TEN',
   'WAS',
]

const positions = [
    'QB',
    'RB',
    'WR',
    'TE',
    'DEF',
]


function PlayerSearch() {
    const [searchData, setSearchData] = useState(null);
    const navigate = useNavigate();

    const searchPlayers = async (playerMap) => {
        return await PlayerActions.searchPlayers(playerMap);
    }
    const createRoster = async (players) => {
        return await RosterActions.createRoster(players);
    }

    const save = () => {
        createRoster(searchData['players'])
            .then(data => {
                (data === 'ok') ? navigate('my-team') : alert('Issue encountered saving players. Try again.')
            })
            .catch(err => console.log(err));
    }

    function handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());
        document.getElementById('submit-form').reset();

        search(formJson);
    }

    const setSearchResults = (data) => {
        let playerMap = {
            'QB': [],
            'RB': [],
            'WR': [],
            'TE': [],
            'DEF': [],
            'players': [],
        }
        data.map((player) => {
            let p = new PlayerDetail(player['id'], player['name'], player['position'], player['team'])
            playerMap[p.position].push(`${p.name} ${p.team}`)
            playerMap['players'].push(`${p.id}`)
        })
        setSearchData(playerMap);
    }

    function search(formData) {
        let playerMap = {
            'QB': [],
            'RB': [],
            'WR': [],
            'TE': [],
            'DEF': [],
        }
        positions.forEach((position) => {
            [...Array(6)].forEach((_, i) => {
                let k = position + i.toString();
                let query = formData[k];
                if (query) { playerMap[position].push(query); }
            })
        })
        searchPlayers(playerMap)
            .then(json => {
                console.log(json);
                setSearchResults(json);
            })
            .catch(err => console.log(err));
    }

    return (
        <>
            <h2 style={{
                marginTop: 120,
                textAlign: "center",
                color: "whitesmoke",
            }}>No Roster Found for Current Season. Search Below to Import.</h2>
            <Stack
                spacing={.25}
                direction="row"
                marginLeft={10}
            >
                <Item style={{width: 48}}/>

                <Container maxWidth="775px" style={{
                    marginTop: 20,
                    marginBottom: 40,
                    backgroundColor: 'whitesmoke',
                    height: '90vh',
                    width: '90%',
                }}>
                    <Stack spacing={.5} direction="row">
                        <form
                            id="submit-form"
                            method="post"
                            onSubmit={handleSubmit}
                            style={{
                                width: '95%'
                            }}
                        >
                            {
                                positions.map((pos, index) => (
                                    <ImportRow  key={index} pos={pos} results={searchData}/>
                                ))
                            }
                            <Item>
                                <button
                                    type="submit"
                                    name="action"
                                    value="searchSubmit"
                                    className="button button1"
                                >Search</button>
                            </Item>
                        </form>
                        {
                            (searchData)
                                ? <Item >
                                    <button
                                        type="submit"
                                        onClick={save}
                                        className="button button1"
                                        style={{
                                            marginLeft: 0
                                        }}
                                    >Save
                                    </button>
                                </Item>
                                : <></>
                        }
                    </Stack>
                    <Stack spacing={1} direction="row">
                    <span className="container-description">
                        <h3 style={{marginTop: 7}}>Search Guidelines</h3>
                        <li>Enter FirstName LastName TeamAbbreviation (case insensitive, space-separated). For DEF just put the abbreviation.</li>
                        <li>Name does not need to be exact, but the closer the better. Team abbreviation must be correct & included.</li>
                        <li>Example: patrick mahomes kc --> Result: Patrick Mahomes KC</li>
                        <li>Example2: pat mah kc --> Result: Patrick Mahomes KC</li>
                        <li>Example3: patrk mahmes kc --> Result: None, name has missing letters in sequence</li>
                    </span>
                        <div >
                            <h3 style={{marginTop: 7}}>Team Abbreviations</h3>
                            <div className="box">
                                {
                                    abbreviations.map((abbreviation, index) => (
                                        <span key={index} >{abbreviation}</span>
                                    ))
                                }
                            </div>
                        </div>
                    </Stack>
                </Container>
            </Stack>
        </>
    );
}

export default function RosterImport() {

    return (
        <>
            <PlayerSearch/>
        </>
    );
}
import * as React from 'react';
import '../../css/LeaderBoard.scss';
import Rank from "./Rank";
import {useEffect, useState} from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";

export default function LeaderBoard(props) {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

    const [data, setData] = useState([]);
    const [rankings, setRankings] = useState([]);
    const [firstPlace, setFirstPlace] = useState([]);
    let endpoint = props.url + "leaders/"

    useEffect(() => {
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
                setRankings(json["titles"])
                setFirstPlace(json["titles"][0])
            })
            .catch(err => console.log(err));
    }, []);

    const handleClick = (index) => {
        switch (index) {
            case 0:
                setRankings(data["titles"]);
                setFirstPlace(data["titles"][0]);
                break;
            case 1:
                setRankings(data["points"]);
                setFirstPlace(data["points"][0]);
                break;
            case 2:
                setRankings(data["wins"]);
                setFirstPlace(data["wins"][0]);
                break;
            case 3:
                setRankings(data["points_max"]);
                setFirstPlace(data["points_max"][0]);
                break;
            case 4:
                setRankings(data["wins_max"]);
                setFirstPlace(data["wins_max"][0]);
                break;
            case 5:
                setRankings(data["ppg"]);
                setFirstPlace(data["ppg"][0]);
                break;
            case 6:
                setRankings(data["playoffs"]);
                setFirstPlace(data["playoffs"][0]);
                break;
            case 7:
                setRankings(data["finals"]);
                setFirstPlace(data["finals"][0]);
                break;
            case 8:
                setRankings(data["playoff_rate"]);
                setFirstPlace(data["playoff_rate"][0]);
                break;
            default:
                setRankings(data["titles"]);
                setFirstPlace(data["titles"][0]);
        }
    }
    const selectionTabs = [
        "Titles",
        "Points/Yr",
        "Wins/Yr",
        "Points/Max",
        "Wins/Max",
        "PPG",
        "Playoffs Made",
        "Finals Made",
        "Playoff/Rate",
    ]
    return (
        <div className="board-body">
            <Box sx={{width: '100%', bgcolor: 'background.paper'}}>
                <Tabs value={value} onChange={handleChange} centered>
                    {selectionTabs.map((tab, index) => (
                        <Tab label={tab} onClick={() => handleClick(index)}/>
                    ))}
                </Tabs>
            </Box>
        <div className="card">
            <section className="card-info card-section">
                <i className="ion-navicon menu"></i>
                <i className="ion-ios-search search"></i>
                <img
                    className={"leader-image"}
                    src={require("../../img/Pest.png")}
                    // src={require("../../img/Pest.png" + firstPlace.image)}
                    alt="Grapefruit slice atop a pile of other slices"/>

                <section className="user row">
                    <h1 className="user-header">
                        {firstPlace.team_name}
                        <h2 className="sub header">
                            {firstPlace.name}
                        </h2>
                    </h1>
                </section>

                <section className="statistics">
                    <article className="statistic">
                        <h4 className="statistic-title">
                            Rank
                        </h4>
                        <h3 className="statistic-value">
                            #1
                        </h3>
                    </article>

                    <article className="statistic">
                        <h4 className="statistic-title">
                            Score
                        </h4>
                        <h3 className="statistic-value">
                            {firstPlace.total}
                        </h3>
                    </article>
                </section>

                <div className="dial">
                    <h2 className="dial-title">
                        {firstPlace.category_type}
                        {/*category type*/}
                    </h2>
                    <h3 className="dial-value">
                        {firstPlace.category}
                        {/*category name*/}
                    </h3>
                </div>
            </section>
            <section className="card-details card-section">

                <nav className="menu">
                    <article className="menu-item menu-item-active">
                        Team
                    </article>
                    <article className="menu-item">
                        Value
                    </article>
                </nav>

                <dl className="leaderboard">
                    {rankings.map((leader, index) => (<Rank name={leader.name} total={leader.total} index={index} />))}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "100%", backgroundColor: '#14a103'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Bryan Smith</div>*/}
                    {/*    <div className="leaderboard-value">20.123</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "90%", backgroundColor: '#42cf30'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Kevin Johnson</div>*/}
                    {/*    <div className="leaderboard-value">16.354</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "80%", backgroundColor: '#88d87e'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Glen Howie</div>*/}
                    {/*    <div className="leaderboard-value">15.873</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "70%", backgroundColor: '#a3dc9c'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Mark Desa</div>*/}
                    {/*    <div className="leaderboard-value">12.230</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "60%", backgroundColor: '#d0e8cd'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "50%", backgroundColor: 'rgba(200,204,200,0.96)'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "50%", backgroundColor: '#f1bbbb'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "60%", backgroundColor: '#dd6f6f'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "70%", backgroundColor: '#d85c5c'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "80%", backgroundColor: '#da4242'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "90%", backgroundColor: '#dc2222'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                    {/*<dt>*/}
                    {/*    <article className="progress">*/}
                    {/*        <section className="progress-bar"*/}
                    {/*                 style={{width: "100%", backgroundColor: '#c80303'}}></section>*/}
                    {/*    </article>*/}
                    {/*</dt>*/}
                    {/*<dd>*/}
                    {/*    <div className="leaderboard-name">Martin Geiger</div>*/}
                    {/*    <div className="leaderboard-value">10.235</div>*/}
                    {/*</dd>*/}
                </dl>
            </section>
        </div>
        </div>
    );
}

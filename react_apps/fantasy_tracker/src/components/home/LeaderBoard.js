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
    let endpoint = props.url + "leaders/"

    useEffect(() => {
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err));
    }, []);

    let leaders = []
    // let leaders = [
    //     {name: "name1", total: 123.4, team_name: "ABC 123", category: "POINTS", category_type: "TOTAL", img: "Pest.png"},
    //     {name: "name2", total: 123.4},
    //     {name: "name3", total: 123.4},
    //     {name: "name4", total: 123.4},
    //     {name: "name5", total: 123.4},
    //     {name: "name6", total: 123.4},
    //     {name: "name7", total: 123.4},
    //     {name: "name8", total: 123.4},
    //     {name: "name9", total: 123.4},
    //     {name: "name10", total: 123.4},
    //     {name: "name11", total: 123.4},
    //     {name: "name12", total: 123.4},
    // ]
    // const handleMenuSelection = (element) => {
    //     leaders = [
    //         {name: "name1", totals: 123.4},
    //         {name: "name2", totals: 123.4},
    //         {name: "name3", totals: 123.4},
    //         {name: "name4", totals: 123.4},
    //         {name: "name5", totals: 123.4},
    //         {name: "name6", totals: 123.4},
    //         {name: "name7", totals: 123.4},
    //         {name: "name8", totals: 123.4},
    //         {name: "name9", totals: 123.4},
    //         {name: "name10", totals: 123.4},
    //         {name: "name11", totals: 123.4},
    //         {name: "name12", totals: 123.4},
    //     ]
    // }
    let firstPlace = leaders[0]
    const handleClick = (index) => {
        console.log(index);
        switch (index) {
            case 0:
                leaders = data.titles
                firstPlace = leaders[0]
                break;
            case 1:
                leaders = data.points_yr
                firstPlace = leaders[0]
                break;
            case 2:
                leaders = data.wins_yr
                firstPlace = leaders[0]
                break;
            default:
                leaders = data.titles
                firstPlace = leaders[0]
        }
    }
    const selectionTabs = [
        "Titles",
        "Points/Yr",
        "Wins/Yr",
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
                    src={require("../../img/" + firstPlace.img)}
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
                    {leaders.map((leader, index) => (<Rank name={leader.name} total={leader.total} index={index} />))}
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

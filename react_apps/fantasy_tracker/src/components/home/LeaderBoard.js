import * as React from 'react';
import '../../css/LeaderBoard.scss';
import Rank from "./Rank";
import {useEffect, useState} from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {LeaderActions} from "../../actions/actionIndex";


export default function LeaderBoard() {
    const [value, setValue] = React.useState(0);
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const [data, setData] = useState([]);
    const [rankings, setRankings] = useState([]);
    const [firstPlace, setFirstPlace] = useState([]);
    const [secondPlace, setSecondPlace] = useState([]);
    const [isActive, setIsActive] = useState([]);
    const [allData, setAllData] = useState([]);
    const [dataRow, setDataRow] = useState('titles');

    const getLeaders = async () => {
        return await LeaderActions.getLeaders();
    }

    useEffect(() => {
        getLeaders()
            .then(json => {
                console.log(json);
                setRankings(json["titles"]);
                setData(json);
                setAllData(json);
                setFirstPlace(json["titles"][0]);
                setSecondPlace(json["titles"][1]);
            })
            .catch(err => console.log(err))
    }, []);

    let activeOnly = {
        titles: [],
        points: [],
        wins: [],
        points_max: [],
        wins_max: [],
        ppg: [],
        playoffs: [],
        finals: [],
        playoff_rate: [],
    }
    Object.keys(data).forEach((key) => {
        let rows = data[key];
        for (const r in rows) {
            if (rows[r]["is_active"]) {activeOnly[key].push(rows[r])}
        }
    })

    const setActive = () => {
        // TODO gotta be a better way to do this
        if (isActive) {
            setData(activeOnly);
            setRankings(activeOnly[dataRow]);
            setFirstPlace(activeOnly[dataRow][0]);
            setSecondPlace(activeOnly[dataRow][1]);
        } else {
            setData(allData);
            setRankings(allData[dataRow]);
            setFirstPlace(allData[dataRow][0]);
            setSecondPlace(allData[dataRow][1]);
        }
        setIsActive(!isActive);
    }

    const resultsMapping = {
        'Titles': 'titles',
        'Points/Yr': 'points',
        'Wins/Yr': 'wins',
        'Points/Max': 'points_max',
        'Wins/Max': 'wins_max',
        'PPG': 'ppg',
        'Playoffs Made': 'playoffs',
        'Finals Made': 'finals',
        'Playoff/Rate': 'playoff_rate',
    }
    const setResults = (key) => {
        let val = resultsMapping[key];
        setRankings(data[val]);
        setFirstPlace(data[val][0]);
        setSecondPlace(data[val][1]);
        setDataRow(val);
    }
    const handleClick = (tab) => {
        setResults(tab);
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
                <Tabs value={value} onChange={handleChange} variant={"scrollable"} sx={{marginLeft: 3, marginRight: 3}}>
                    {selectionTabs.map((tab, index) => (
                        <Tab key={index} label={tab} onClick={() => handleClick(tab)}/>
                    ))}
                </Tabs>
            </Box>
            <div className="card">
                <section className="card-info card-section">
                    <i className="ion-navicon menu"></i>
                    <i className="ion-ios-search search"></i>
                    <section className="statistics">

                        <article className="statistic">
                            <h4 className="statistic-title2">
                                Category
                            </h4>
                            <h3 className="statistic-value">
                                {firstPlace.category_type} {firstPlace.category}
                            </h3>
                        </article>

                    </section>
                    <img
                        className={"leader-image"}
                        src={require("../../img/firstPlace.png")}
                        alt="First Place"/>
                    <section className="user row">
                        <div className="user-header">
                            {firstPlace.team_name}
                            <h2 className="sub header">
                                {firstPlace.name}
                            </h2>
                        </div>
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
                    <section className="statistics">
                        <article className="statistic">
                            <h4 className="statistic-title">
                                Year
                            </h4>
                            <h3 className="statistic-value">
                                {firstPlace.season_start_year}
                            </h3>
                        </article>

                        <article className="statistic">
                            <h4 className="statistic-title">
                                Active
                            </h4>
                            <h3 className="statistic-value">
                                {(firstPlace.is_active) ? firstPlace.years_count + "+" : firstPlace.years_count}
                            </h3>
                        </article>

                    </section>
                    <img
                        className={"leader-image"}
                        src={require("../../img/secondPlace.png")}
                        alt="Second Place"/>

                    <section className="user row">
                        <div className="user-header">
                            {secondPlace.team_name}
                            <h2 className="sub header">
                                {secondPlace.name}
                            </h2>
                        </div>
                    </section>

                    <section className="statistics">
                        <article className="statistic">
                            <h4 className="statistic-title">
                                Rank
                            </h4>
                            <h3 className="statistic-value">
                                #2
                            </h3>
                        </article>

                        <article className="statistic">
                            <h4 className="statistic-title">
                                Score
                            </h4>
                            <h3 className="statistic-value">
                                {secondPlace.total}
                            </h3>
                        </article>

                    </section>
                    <section className="statistics">
                        <article className="statistic">
                            <h4 className="statistic-title">
                                Year
                            </h4>
                            <h3 className="statistic-value">
                                {secondPlace.season_start_year}
                            </h3>
                        </article>

                        <article className="statistic">
                            <h4 className="statistic-title">
                                Active
                            </h4>
                            <h3 className="statistic-value">
                                {(secondPlace.is_active) ? secondPlace.years_count + "+" : secondPlace.years_count}
                            </h3>
                        </article>

                    </section>
                </section>

                <section className="card-details card-section">

                    <nav className="menu">
                        <article className="menu-item menu-item-active">
                            Team
                                <button className="button button1" onClick={setActive}>
                                    {(isActive) ? 'ACTIVE ONLY' : 'ALL TEAMS'}
                                </button>
                        </article>
                        <article className="menu-item">
                            Value
                        </article>
                    </nav>

                    <dl className="leaderboard">
                        {
                            (rankings.length) ? rankings.map((leader, index) => (
                            <Rank
                                key={index} name={leader.name}
                                total={leader.total}
                                year={leader.season_start_year}
                                team_name={leader.team_name}
                                index={index}/>
                                )) : <div>NO DATA</div>
                        }
                    </dl>
                </section>
            </div>
        </div>
    );
}

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
    let leaderImage = "../../img/" + firstPlace["image"]
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
                    src={require("../../img/Allard.png")}
                    // src={require(leaderImage.toString())}
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
                    </h2>
                    <h3 className="dial-value">
                        {firstPlace.category}
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
                    {rankings.map((leader, index) => (
                        <Rank name={leader.name} total={leader.total} year={leader.season_start_year} team_name={leader.team_name} index={index} />
                    ))}
                </dl>
            </section>
        </div>
        </div>
    );
}

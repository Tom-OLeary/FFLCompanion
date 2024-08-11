import React, {useEffect, useState} from "react";
import Chart from "./trends/Chart";
import TradeCard from "./trades/TradeCard";

function Trends(props) {
    const [data, setData] = useState([]);
    const [stats, setStats] = useState([]);
    const [years, setYears] = useState([]);

    let endpoint = props.url + 'trends/';

    useEffect(() => {
        fetch(endpoint, {
            method: 'GET',
            headers: {'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE')}
        })
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
                setStats(json['data']);
                setYears(json['years']);
            })
            .catch(err => console.log(err));
    }, [endpoint]);

    // const stats = data['data']
    // const years = data['years']
    console.log("STATS", stats)
    // const columns = []
    // for (const k in data[0]) {columns.push({field: k, headerName: k, width: 150,  headerClassName: 'column-header'})}

    return (
        <>

            <div>
                {
                    stats.map((stat, index) => (<div className={"card-column"} key={index}>
                        <Chart stats={stat['stats']} years={years} label={'total_points'} title={stat['team_owner']}/>
                    </div>
                    ))
            }
            </div>
        </>
    );
}

export default Trends;
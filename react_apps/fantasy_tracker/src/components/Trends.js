import React, {useEffect, useState} from "react";
import Chart from "./trends/Chart";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";

function Trends(props) {
    // const [data, setData] = useState([]);
    const [stats, setStats] = useState([]);
    const [years, setYears] = useState([]);
    const [choices, setChoices] = useState([]);
    const [label, setLabel] = useState("total_points");

    let endpoint = props.url + 'trends/';

    useEffect(() => {
        fetch(endpoint, {
            method: 'GET',
            headers: {'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE')}
        })
            .then(res => res.json())
            .then(json => {
                console.log(json);
                // setData(json);
                setStats(json['data']);
                setYears(json['years']);
                setChoices(json['columns']);
            })
            .catch(err => console.log(err));
    }, [endpoint]);

    const [value, setValue] = React.useState(0);
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleClick = (labelValue) => {
        setLabel(labelValue);
    }

    return (
        <>
            <Box sx={{width: '100%', bgcolor: 'grey'}} className="choice-bar">
                <Tabs
                    value={value}
                    onChange={handleChange}
                    variant={"scrollable"}
                    sx={{marginLeft: 3, marginRight: 3}}>
                    {choices.map((tab, index) => (
                        <Tab
                            key={index}
                            label={tab}
                            onClick={() => handleClick(tab)}
                            sx={{color: 'whitesmoke'}}
                        />
                    ))}
                </Tabs>
            </Box>
            <div>
                {
                    stats.map((stat, index) => (<div className={"card-column"} key={index}>
                        <Chart stats={stat['stats']} years={years} label={label} title={stat['team_owner']}/>
                    </div>
                    ))
            }
            </div>
        </>
    );
}

export default Trends;
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import React, {useEffect, useState} from "react";
import Chart from "./trends/Chart";
import TimelineIcon from '@mui/icons-material/Timeline';
import Divider from "@mui/material/Divider";
import {BreakdownActions} from "../actions/actionIndex";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `vertical-tab-${index}`,
    'aria-controls': `vertical-tabpanel-${index}`,
  };
}

function Trends() {
    const [value, setValue] = React.useState(0);
    const [stats, setStats] = useState([]);
    const [years, setYears] = useState([]);
    const [choices, setChoices] = useState([]);
    const [label, setLabel] = useState("total_points");

    const getTrends = async () => {
        return await BreakdownActions.getTrends();
    }

    useEffect(() => {
        getTrends()
            .then(json => {
                console.log(json);
                setStats(json['data']);
                setYears(json['years']);
                setChoices(json['columns']);
            })
            .catch(err => console.log(err))
    }, []);

    const handleClick = (labelValue) => {
        setLabel(labelValue);
    }

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <>
            <h1 className="trend-title">Team
            <TimelineIcon style={{ color: "rgba(41,204,223,0.7)", fontSize: 60 }} />
                Trends
            </h1>
            <Divider style={{ backgroundColor: 'black' }} />
            <Box
                sx={{
                    flexGrow: 1,
                    display: 'flex',
                    height: "100%",
                    width: 160,
                    position: "fixed",
                    zIndex: 1,
                    top: 10,
                    left: 0,
                    overflowX: "hidden",
                    paddingTop: 20,
                }}
            >
                <Tabs
                    orientation="vertical"
                    variant="scrollable"
                    value={value}
                    onChange={handleChange}
                    aria-label="Category Selection"
                    sx={{borderRight: 1, borderColor: 'divider', position: 'fixed'}}
                >
                    {choices.map((tab, index) => (
                        <Tab
                            key={index}
                            label={tab} {...a11yProps(index)}
                            onClick={() => handleClick(tab)}
                            sx={{color: 'whitesmoke'}}
                        />
                    ))}
                </Tabs>
            </Box>

            <div
                style={{
                    marginLeft: 160,
                    padding: 10,
                    marginTop: 160,
                }}
                    >
                        {
                            stats.map((stat, index) => (
                                <Chart stats={stat['stats']} years={years} label={label} title={stat['team_owner']}/>
                            ))
                        }
                    </div>
        </>
    );
}

export default Trends;
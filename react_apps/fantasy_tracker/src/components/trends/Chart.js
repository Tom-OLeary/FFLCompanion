import React from "react";
import { LineChart } from '@mui/x-charts/LineChart';
import '../../css/Trends.css';
import Divider from "@mui/material/Divider";

function Chart(props) {
    let yAxisData = Array.from({length: props.years.length}, () => 0);
    for (const row of props.stats) {
        let seasonYear = row['season_start_year'].toString();
        let rowIndex = props.years.indexOf(seasonYear);
        yAxisData[rowIndex] = row[props.label];
    }

    // sets date object to remove commas from years
    let xAxisData = [];
    for (const year of props.years) { xAxisData.push(new Date(year, 0, 1)); }

    return (
        <div>
            <h2 className="team-title"> {props.title}</h2>
            <div className="stats-container">
                <div className="stats-text">
                    Max {props.label}: {Math.max(...yAxisData)}
                </div>
                <div className="stats-text">
                    Min {props.label}: {Math.min.apply(null, yAxisData.filter(Boolean))}
                </div>

            </div>
            <LineChart
                xAxis={
                    [
                        {
                            data: xAxisData,  // years
                            label: 'Year',
                            scaleType: 'time',
                            valueFormatter: (date) => date.getFullYear().toString(),
                        }
                    ]
                }
                series={[
                    {
                        data: yAxisData,  // selected label
                        label: props.label,
                    },
                ]}
                width={600}
                height={300}
            />

        </div>
    );
}

export default Chart;
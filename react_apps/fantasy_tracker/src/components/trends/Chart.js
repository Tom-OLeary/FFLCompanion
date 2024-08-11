import React, {useEffect, useState} from "react";
import { LineChart } from '@mui/x-charts/LineChart';
import '../../css/Trends.css';

function Chart(props) {
    console.log("PROPS", props);
    let yAxisData = [];
    for (const row of props.stats) {
        yAxisData.push(row[props.label])
    }

    return (
        <h2 className="team-title"> {props.title}
        <LineChart
            xAxis={
            [
                {
                    data: props.years,
                    label: 'Year',
                }
            ]
        }
            series={[
                {
                    data: yAxisData,
                    label: props.label,
                },
            ]}
            width={600}
            height={300}

        />
            </h2>
    );
}

export default Chart;
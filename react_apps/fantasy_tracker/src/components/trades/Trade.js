import * as React from 'react';
import '../../css/TradeCard.css';
import '../../css/Progress.css';
import TradeCard from "./TradeCard";
import {useEffect, useState} from "react";
import {TradeActions} from "../../actions/actionIndex";

export default function Trade() {
    const [data, setData] = useState([]);
    const getTrades = async () => {
        return await TradeActions.getTrades();
    }

    useEffect(() => {
        getTrades()
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err))
    }, []);

    return (
        <div style={{marginTop: 150}}>
            {
                (data.length)
                    ? data.map((trade, index) => (
                        <div className={"card-column"} key={index}><TradeCard data={trade}/></div>))
                    : <div className="progress-description">NO TRADES HERE YET</div>
            }
        </div>
    );
}
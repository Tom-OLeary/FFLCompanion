import * as React from 'react';
import '../../css/TradeCard.css';
import TradeCard from "./TradeCard";
import {useEffect, useState} from "react";

export default function Trade(props) {
    const [data, setData] = useState([])
    let endpoint = props.url + "trades/"
    useEffect(() => {
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err));
    }, []);

  return (
      <div >
          {data.map((trade, index) => (<div className={"card-column"}><TradeCard data={trade} /></div>))}
          </div>
  );
}
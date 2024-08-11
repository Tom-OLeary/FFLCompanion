import * as React from 'react';
import '../../css/TradeCard.css';
import TradeCard from "./TradeCard";
import {useEffect, useState} from "react";

export default function Trade(props) {
    const [data, setData] = useState([]);
    let endpoint = props.url + "trades/";

    useEffect(() => {
        fetch(endpoint, {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE')
            }
        })
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err));
    }, [endpoint]);

  return (
      <div>
          {
              (data)
                  ? data.map((trade, index) => (<div className={"card-column"} key={index}><TradeCard data={trade}/></div>))
                  : <div>NO TRADE DATA FOUND</div>
          }
          </div>
  );
}
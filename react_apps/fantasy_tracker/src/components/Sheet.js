import React, {useEffect, useState} from "react";
import '../css/Header.css';
import Select from "react-dropdown-select";
import Spreadsheet from "react-spreadsheet";


export default function Header(props) {
    const [data, setData] = useState([])

    useEffect(() => {
        fetch(props.url)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json)
            })
    }, []);

    const columnLabels = []
    for (const k in data[0]) {columnLabels.push(k)}
    const values = data.map(function(e) {
            let row = []
            for (const c in e) {row.push({value: e[c]})}
            return row
        }
    )
    return (
        <div>
            <Spreadsheet data={values} columnLabels={columnLabels}/>
        </div>
    );
}
import * as React from 'react';
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';
import {useEffect, useState} from "react";
import '../../css/Header.css';


export default function GridTest(props) {
    const [data, setData] = useState([])
    let url = props.url + "players/"

    useEffect(() => {
        fetch(url)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json)
            })
    }, []);

    const columns = []
    for (const k in data[0]) {columns.push({field: k, headerName: k, width: 150,  headerClassName: 'mid-header'})}

    return (
        <div style={{ height: 650, marginRight: 50, marginLeft: 50, marginBottom: 50, backgroundColor: "darkgrey"}}>
          <DataGrid
              rows={data}
              columns={columns}
              sx={{
                boxShadow: 2,
                border: 2,
                borderColor: 'primary.dark',
                '& .MuiDataGrid-cell:hover': {
                  color: 'primary.main',
                },
              }}
          />
        </div>
    );
}

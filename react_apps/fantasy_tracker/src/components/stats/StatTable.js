import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {useEffect, useState} from "react";
import '../../css/Header.css';
import '../../css/Stats.css';
import {getTeamStats} from "../../actions/team";

export default function StatTable() {
    const [data, setData] = useState([]);

    const getTeamData = async () => {
        return await getTeamStats();
    }

    useEffect(() => {
        getTeamData()
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err))
    }, []);

    const columns = []
    for (const k in data[0]) {columns.push({field: k, headerName: k, width: 150,  headerClassName: 'column-header'})}

    return (
        <>
            <div>
                <div style={{
                    height: 650,
                    marginRight: 50,
                    marginLeft: 50,
                    marginBottom: 50,
                    marginTop: 50,
                    backgroundColor: "darkgrey"
                }}>
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
            </div>
        </>
    );
}

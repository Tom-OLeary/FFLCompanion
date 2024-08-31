import {Container} from "@mui/material";
import React from "react";
import {DataGrid} from "@mui/x-data-grid";

export default function Waiver(players) {
    // const [selectedRows, setSelectedRows] = React.useState([]);
    const statColumns = [
        'id',
        'name',
        'position',
        'team',
    ]
    const columns = []
    for (const k in players[0]) {columns.push({field: k, headerName: k, width: 150,  headerClassName: 'column-header'})}

    const handleSelection = (event) => {
        // setSelectedRows(ids);
        console.log("handleSelection", event);
    }
    const handleSubmit = (event) => {
        // console.log('ROWS', selectedRows);
    }
        return (
        <>
                <Container maxWidth="875px" style={{
                    marginTop: 20,
                    marginBottom: 40,
                    backgroundColor: 'whitesmoke',
                    height: '130vh',
                    width: '90%',
                }}>
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
                        rows={players}
                        columns={columns}
                        sx={{
                            boxShadow: 2,
                            border: 2,
                            borderColor: 'primary.dark',
                            '& .MuiDataGrid-cell:hover': {
                                color: 'primary.main',
                            },
                        }}
                        checkboxSelection={true}
                        // onRowSelectionModelChange={handleSelection}
                    />
                </div>
                <button className="button button1" onClick={handleSubmit}>SUBMIT</button>
            </div>
        </>
                </Container>
        </>
    );
}
import React, {useEffect, useState} from "react";
import '../../css/Header.css';

// import Select from "react-dropdown-select";
// import Spreadsheet from "react-spreadsheet";
import Paper from "@mui/material/Paper";
import {styled} from "@mui/material/styles";
import {Stack} from "@mui/material";


export default function Header(props) {
    const [data, setData] = useState([])
    let endpoint = props.url + "breakdown/"
    useEffect(() => {
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err));
    }, []);

    const PaperItem = styled(Paper)(({theme}) => ({
        width: "100%",
        // height: 400,
        height: "75%",
        backgroundColor: "#dd9e00",
        padding: theme.spacing(2),
        ...theme.typography.body2,
    }));

    return (
        <header>
            <div className={"paper-stack"}>
                <Stack direction="row" spacing={2}>
                    <PaperItem elevation={20} square={false}>
                        {/*<div className={"paper-image"}>*/}
                        {/*</div>*/}
                        {/*<br/>*/}
                        <div className={"mid-header"}>
                            Years Active
                            <div>{data.years_active}</div>
                        </div>
                    </PaperItem>
                    <PaperItem elevation={20} square={false}>
                        <div className={"mid-header"}>
                            Active Members
                            <div>{data.active_members}</div>
                        </div>
                    </PaperItem>
                    <PaperItem elevation={20} square={false}>
                        <div className={"mid-header"}>
                            Total Members
                            <div>{data.total_members}</div>
                        </div>
                    </PaperItem>
                    <PaperItem elevation={20} square={false}>
                        <div className={"mid-header"}>
                            Unique Champions
                            <div>{data.unique_champions}</div>
                        </div>
                    </PaperItem>
                    <PaperItem elevation={20} square={false}>
                        <div className={"mid-header"}>
                            Prize Pool
                            <div>{data.prize_pool}</div>
                        </div>
                    </PaperItem>
                </Stack>
            </div>
        </header>
    )
}

import React, {useEffect, useState} from "react";
import '../../css/Header.css';
// import Select from "react-dropdown-select";
// import Spreadsheet from "react-spreadsheet";
import Paper from "@mui/material/Paper";
import {styled} from "@mui/material/styles";
import {Stack} from "@mui/material";
import MenuDrawer from "../MenuDrawer";


export default function Header(props) {
    // const [data, setData] = useState([])
    // let url = props.url + "breakdowns/"
    // useEffect(() => {
    //     fetch(url)
    //         .then(res => res.json())
    //         .then(json => {
    //             console.log(json);
    //             setData(json)
    //         })
    // }, []);
    const PaperItem = styled(Paper)(({ theme }) => ({
      width: "100%",
      height: "75%",
      backgroundColor: "#cfc00e",
      padding: theme.spacing(2),
      ...theme.typography.body2,
    }));

    return (
        <header>
            {/*<MenuDrawer />*/}
            <h1 id="headerTitle">Leaderboard</h1>
            <Stack direction="row" spacing={2}>
                <PaperItem elevation={20} square={false}>
                    <div className={"mid-header"}>
                        Years Active
                        <div>15</div>
                    </div>
                </PaperItem>
                <PaperItem elevation={20} square={false}>
                    <div className={"mid-header"}>
                        Active Members
                        <div>12</div>
                    </div>
                </PaperItem>
                <PaperItem elevation={20} square={false}>
                    <div className={"mid-header"}>
                        Total Members
                        <div>26</div>
                    </div>
                </PaperItem>
                <PaperItem elevation={20} square={false}>
                    <div className={"mid-header"}>
                        Unique Champions
                        <div>5</div>
                    </div>
                </PaperItem>
                <PaperItem elevation={20} square={false}>
                    <div className={"mid-header"}>
                        Projected Prize Pool
                        <div>$3000</div>
                    </div>
                </PaperItem>
            </Stack>
        </header>
    )
}

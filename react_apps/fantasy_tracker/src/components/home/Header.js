import React, {useEffect, useState} from "react";
import '../../css/Header.css';
import Paper from "@mui/material/Paper";
import {styled} from "@mui/material/styles";
import {Stack} from "@mui/material";
import {getBreakdown} from "../../actions/breakdown";


export default function Header() {
    const [data, setData] = useState([]);

    const getData = async () => {
        return await getBreakdown();
    }

    useEffect(() => {
        getData()
            .then(json => {
                console.log(json);
                setData(json);
            })
            .catch(err => console.log(err))
    }, []);

    const PaperItem = styled(Paper)(({theme}) => ({
        width: "100%",
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

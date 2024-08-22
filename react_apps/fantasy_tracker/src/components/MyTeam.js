import React, {useEffect, useState} from "react";
import '../css/MyTeam.css';
import '../css/Progress.css';
import RosterImport from "./my_team/RosterImport";
import Roster from "./my_team/Roster";
import {RosterActions} from "../actions/actionIndex";

function MyTeam() {
    const [roster, setRoster] = useState(null);

    const getRoster = async () => { return await RosterActions.getRoster(); }

    useEffect(() => {
        getRoster()
            .then(json => {
                console.log(json);
                setRoster(json);
            })
            .catch(err => console.log(err))
    }, []);

    return (
        <>
            {
                (roster)
                    ? <RosterImport />
                    : <Roster data={roster} />
            }
        </>
    );
}

export default MyTeam;
import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import {useEffect, useState} from "react";
import '../../css/Notification.css';

export default function Notification(props) {
    // const [data, setData] = useState([]);
    // let endpoint = props.url.slice(0, -7) + "notifications/"
    //
    // useEffect(() => {
    //     fetch(endpoint, {
    //         method: 'GET',
    //         headers: {
    //             'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE')
    //         }
    //     })
    //         .then(res => res.json())
    //         .then(json => {
    //             console.log(json);
    //             setData(json);
    //         })
    //         .catch(err => console.log(err));
    // }, [endpoint]);
    const data = [
        {title: "Temporary Issue", message: "If home page says 'No Data', come back here and click logout. Should only have to do this once."}
    ] // TODO pull these from database
    return (
        <List sx={{width: '100%', maxWidth: 450, marginTop: 15}} className="notification">
            {
                data.map((item, index) => (
                    <ListItem key={index} alignItems="flex-start">
                        <ListItemAvatar>
                            <Avatar>!</Avatar>
                        </ListItemAvatar>
                        <ListItemText
                            primary={item['title']}
                            sx={{color: 'whitesmoke'}}
                            secondary={
                                <React.Fragment >
                                    <div style={{color: 'whitesmoke'}}>{item["message"]}</div>
                                </React.Fragment>
                            }
                        />
                    </ListItem>
                ))
            }
        </List>
    );
}
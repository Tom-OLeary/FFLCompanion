import React from "react";
// import {useNavigate} from "react-router-dom";
import ChangePassword from "./account/ChangePassword";
import '../css/Login.css';

function Account(props) {
    // const navigate = useNavigate();
    // const handleClick = () => {
    //     navigate('/change-password');
    // }
    return (
        <>
            {/*<button className="button" onClick={handleClick}>Change Password</button>*/}
            <div style={{marginTop: 150}}>
                <ChangePassword url={props.url}/>
            </div>
            <div className="bottom-description">
                <h1 className={"header-title"}>
                    Account Page is a work in progress...
                    <br/>
                    <br/>
                    For now you can change your password if you'd like.
                    <br/>
                    <br/>
                    (Not allowed for Demo users)
                </h1>
            </div>
        </>
    );
}

export default Account;
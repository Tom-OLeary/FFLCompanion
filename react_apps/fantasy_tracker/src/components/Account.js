import React from "react";
import {useNavigate} from "react-router-dom";

function Account() {
    const navigate = useNavigate();
    const handleClick = () => {
        navigate('/change-password');
    }
    return (
        <>
            <button className="button" onClick={handleClick}>Change Password</button>
        </>
    );
}

export default Account;
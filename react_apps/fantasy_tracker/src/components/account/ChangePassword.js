import React, {useState} from "react";
import { useForm } from "react-hook-form";
import "../../App.css";
import '../../css/Login.css';

function ChangePassword (props) {
    let url = props.url + 'change-password/';
    const [data, setData] = useState(null);

    const sendRequest = (passwordBody) => {
        fetch(url, {
            method: "POST",
            headers: {
                'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE'),
                'Content-type': 'application/json; charset=UTF-8'
            },
            body: passwordBody,
        })
            .then(res => res.json())
            .then(json => {
                (json === 'ok') ? setData('Success!') : setData('Failed to Update Password. Try Again.');
            })
            .catch(err => console.log(err));
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();

    const onSubmit = (data) => {
        let body = JSON.stringify({
            current_password: data.current_password,
            new_password: data.new_password
        })
        sendRequest(body);
    };

    return (
        <>
            <p className="title">Change Password</p>
            <form className="App" onSubmit={handleSubmit(onSubmit)}>
                <input type="password" {...register("current_password", {required: true})} />
                {errors.username && <span style={{color: "red"}}>
                    *Username* is mandatory </span>}
                <input type="password" {...register("new_password", {required: true})} />
                <input type={"submit"} style={{backgroundColor: "#a1eafb"}}/>
            </form>

            <p style={{textAlign: "center"}}>
                {(data !== null) ? <span style={{color: "whitesmoke"}}>{data}</span> : <span></span>}
            </p>

        </>
    );
}

export default ChangePassword;

import React from "react";
import { useForm } from "react-hook-form";
import "../App.css";
import { useNavigate } from "react-router-dom";
import '../css/Login.css';

function Login (props) {
    let url = props.url;
    const navigate = useNavigate();

    const loadData = (endpoint) => {
        fetch(endpoint)
            .then(res => res.json())
            .then(json => {
                let token = json.token;
                if (token) {
                    window.localStorage.setItem('USER_STATE', token);
                    navigate('/home');
                } else {
                    console.log(json.error);
                }
            })
            .catch(err => console.log(err));
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();

    const onSubmit = (data) => {
        let loginUrl = url + "username=" + data.username + "&password=" + data.password;
        loadData(loginUrl);
    };
    const handleLogout = () => {
        let loginUrl = url + "username=demo.user&password=demouser";
        loadData(loginUrl);
    }
    return (
        <>
                  <div style={{marginTop: 150}}>
            <p className="title">Load League</p>

            <form className="App" onSubmit={handleSubmit(onSubmit)}>
                <input type="username" {...register("username", {required: true})} />
                {errors.username && <span style={{color: "red"}}>
                    *Username* is mandatory </span>}
                <input type="password" {...register("password")} />
                <input type={"submit"} style={{backgroundColor: "#a1eafb"}}/>
            </form>

            <div style={{textAlign: "center"}}>
            <button style={{
                backgroundColor: "black",
                color: "whitesmoke",
                fontSize: 20,
                marginTop: 10,
                width: "20%",
            }} onClick={handleLogout}>
                logout
            </button>
            </div>

            <div className="bottom-description">
                <h1 className={"header-title"}>
                    WELCOME!
                    <br/>
                    <br/>
                    Login to view league-specific data, or begin navigating through the menu for a demo.
                    <br/>
                    <br/>
                    This app is a work in progress. Checkout the App Info tab for information regarding known bugs,
                    project links & more.
                    <br/>
                    <br/>
                    (*Content display not fully optimized for mobile devices or smaller screens on some pages*)
                </h1>
            </div>
                  </div>
        </>
    );
}

export default Login;

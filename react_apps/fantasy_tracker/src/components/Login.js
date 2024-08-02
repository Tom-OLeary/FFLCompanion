import React, {useEffect, useState} from "react";
import { useForm } from "react-hook-form";
import "../App.css";
import {json, useNavigate} from "react-router-dom";
import '../css/Login.css';

function Login (props) {
    let url = 'http://localhost:8000/login/?';
    const navigate = useNavigate();

    const loadData = () => {
        fetch(url)
            .then(res => res.json())
            .then(json => { (json === "ok") ? navigate('/home') : console.log(json.error); })
            .catch(err => console.log(err));
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();

    const onSubmit = (data) => {
        url = url + "username=" + data.username + "&password=" + data.password;
        loadData();
    };
    return (
        <>
            <p className="title">Load League</p>

            <form className="App" onSubmit={handleSubmit(onSubmit)}>
                <input type="username" {...register("username", { required: true })} />
                {errors.username && <span style={{ color: "red" }}>
                    *Username* is mandatory </span>}
                <input type="password" {...register("password")} />
                <input type={"submit"} style={{ backgroundColor: "#a1eafb" }} />
            </form>

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
                </h1>
            </div>
        </>
    );
}

export default Login;

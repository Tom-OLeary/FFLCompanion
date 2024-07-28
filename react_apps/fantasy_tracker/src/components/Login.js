import React, {useEffect, useState} from "react";
import { useForm } from "react-hook-form";
import "../App.css";
import axios from "axios";
import {json, useNavigate} from "react-router-dom";

function Login (props) {
    let url = 'http://localhost:8000/login/?';
    const navigate = useNavigate();

    const fetchData = () => {
        fetch(url)
            .then(res => res.json())
            .then(json => { (json === "ok") ? navigate('/home') : console.log(json.error); })
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();

    const onSubmit = (data) => {

        url = url + "username=" + data.username + "&password=" + data.password;
        fetchData();
        // const userData = JSON.parse(localStorage.getItem(data.email));
        // if (userData) { // getItem can return actual value or null
        //     url = url + "username=" + userData.username + "&password=" + userData.password;
        //     fetchData();
        // } else {
        //     console.log("Input data not found");
        // }
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
        </>
    );
}

export default Login;

import React, {useEffect, useState} from "react";
import { useForm } from "react-hook-form";
import "../App.css";
import axios from "axios";
import {json} from "react-router-dom";

function Login (props) {
    // const {
    //     register,
    //     handleSubmit,
    //     formState: { errors },
    // } = useForm();
    // axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    // axios.defaults.xsrfCookieName = "csrftoken";
    // axios.defaults.withCredentials = true;
    // let url = props.url + "login/"
    let url = 'http://localhost:8000/login/?username=Tom OLeary&password=abc123';
    // onChange = (prop: any, value: string) => {
    //   this.setState({
    //     [prop]: value
    //   });
    // };
    // const response = fetch(url, {
    //     // credentials: 'include',
    //     method: 'POST',
    //     // mode: 'cors',
    //     body: JSON.stringify({
    //       name: "Tom",
    //       password: "abc"
    //     // Other body stuff
    //   }),
    //   headers: {
    //     'Content-Type': 'application/json',
    //     // Other possible headers
    //   }
    // });
    const [data, setData] = useState([])
    const fetchData = () => {
        fetch(url)
            .then(res => res.json())
            .then(json => { (json === "ok") ? setData(json) : setData(json.error); })
    }
    fetchData();
    console.log(data);
    // console.log(response.json)

    // const setState = React.useState(data)
    // const [keywords, setKeywords] = useState('')
    // // const [state, setState] = useState('')
    // let url = props.url + "login/"
    // const requestOptions = {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ title: 'React POST Request Example' })
    // };
    const handleSubmit = (e) => {}
    const onSubmit = (form) => {
        console.log(form);
        // setKeywords({
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ user: form.user, password: form.password })
        // });
        // fetchData()
    };
    // console.log(keywords)

    return (
        <>
            <p className="title" style={{color: "whitesmoke"}}>Login</p>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Enter your name"
                    // value={formData.name}
                    // onChange={handleChange}
                />
                <input
                    type="text"
                    name="password"
                    placeholder="Enter password"
                    // value={formData.password}
                    // onChange={handleChange}
                />
                <button type="submit">Submit</button>
            </form>
        </>
    );
}

export default Login;

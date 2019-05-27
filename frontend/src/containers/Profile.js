import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";

class Profile extends Component {

    constructor (props) {
        super(props);
        this.state = { user: [] };
    }

    componentDidMount () {
        const token = `Bearer ${localStorage.access_token}`;
        const url = `${ROOT_URL}/accounts/user/`

        axios.get(url, {
            headers: {
                Authorization: token
            }
        })
        .then((response) => {
            console.log("POST RESPONSE", response.data)
            this.setState({
                user: response.data
            })
        }).catch(error => {
            console.log("ERROR", error)
        });
    }

    render() {
        return (
            <div>
            <h1>LOGGED IN</h1>
            <p>{this.state.user.slug}</p>
            </div>
        );
    }
}

export default Profile;

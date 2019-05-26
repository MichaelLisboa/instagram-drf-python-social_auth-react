import React, { Component } from 'react';
import axios from "axios";

class Profile extends Component {

    constructor (props) {
        super(props);
        this.state = { user: [] };
    }

    componentDidMount () {
        axios.get("/accounts/profile/")
            .then((response) => {
                console.log("PLACEHOLDER", response.data)
            }).catch(error => {
                console.log("ERROR", error)
            });
    }

    render() {
        return (
            <h1>LOGGED IN</h1>
        );
    }
}

export default Profile;

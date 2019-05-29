import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";

class VerifyEmail extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            email_confirmed: false,
            isLoading: true
        };
    }

    createSubscription = (uid) => {
        const token = `Bearer ${localStorage.access_token}`;
        const url = `${ROOT_URL}/memberships/subscription/${uid}/`

        axios.get(url, {
            headers: {
                Authorization: token
            }
        })
        .then((response) => {
            this.setState({
                isLoading: false
            })
            this.props.history.push("/profile");
        }).catch(error => {
            console.log("ERROR", error)
        });
    }

    componentDidMount () {
        const uid = this.props.match.params.uid
        const token = this.props.match.params.token
        const url = `${ROOT_URL}/accounts/activate/${uid}/${token}`
        axios.get(url)
        .then((response) => {
            this.setState({
                user: response.data.user
            })
            this.createSubscription(response.data.user.user_id);
        }).catch(error => {
            console.log("ERROR", error)
        });
    }

    render() {
        if (this.state.isLoading) {
            return (
                <h1>LOADING</h1>
            )
        }
        return (
            <h1>Verify Email</h1>
        );
    }
}

export default VerifyEmail;

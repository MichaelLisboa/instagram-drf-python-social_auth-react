import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";

class Profile extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            email: '',
            emailConfirmed: false
        };
    }

    componentDidMount () {
        const token = localStorage.access_token;
        const url = `${ROOT_URL}/accounts/u/`
        if (token) {
            axios.get(url, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            .then((response) => {
                console.log("AUTH RESPONSE", response)
                this.setState({
                    user: response.data,
                    email_confirmed: response.data.email_confirmed
                })
            }).catch(error => {
                console.log("ERROR", error)
            });
        } else {
            return this.props.history.push("/");
        }
    }

    render() {
        return (
            <div className="uk-container uk-container-small uk-height-viewport uk-background-secondary">
                <div className="uk-grid-collapse uk-margin-remove uk-flex-center uk-flex-middle uk-height-viewport"
                    data-uk-grid>
                    <div>
                        <h1>{this.state.user.first_name} LOGGED IN</h1>
                        <p>{this.state.user.slug}</p>
                    </div>
                </div>
            </div>
        );
    }
}

export default Profile;

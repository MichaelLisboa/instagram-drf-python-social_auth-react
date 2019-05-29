import React, { Component } from 'react';
import EmailForm from "../components/EmailForm";
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";

class Profile extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            email: '',
            email_confirmed: false
        };
    }

    componentDidMount () {
        const token = `Bearer ${localStorage.access_token}`;
        const url = `${ROOT_URL}/accounts/u/`

        axios.get(url, {
            headers: {
                Authorization: token
            }
        })
        .then((response) => {
            this.setState({
                user: response.data,
                email_confirmed: response.data.email_confirmed
            })
        }).catch(error => {
            console.log("ERROR", error)
        });
    }

    render() {
        return (
            <div className="uk-container uk-container-small uk-height-viewport uk-background-secondary">
            { this.state.email_confirmed ?
                <div>
                <h1>{this.state.user.first_name} LOGGED IN</h1>
                <p>{this.state.user.slug}</p>
                </div>
                :
                <div className="uk-grid-collapse uk-width-1-2@s uk-flex-middle uk-align-center" data-uk-grid>
                    <div className="uk-card uk-card-small uk-card-default">
                        <div className="uk-card-body">
                            <h1>ADD EMAIL {this.state.user.first_name}</h1>
                            <EmailForm user={this.state.user} />
                        </div>
                    </div>
                </div>
            }
            </div>
        );
    }
}

export default Profile;

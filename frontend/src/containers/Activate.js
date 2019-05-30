import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";
import EmailForm from "../components/EmailForm";


class Auth extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            emailConfirmed: false,
            isLoading: true
        };
        this.getUser = this.getUser.bind(this);
    }

    componentDidMount () {
        const token = localStorage.access_token;
        if (!token)
            return this.props.history.push("/");
        this.getUser()
    }

    getUser () {
        const token = localStorage.access_token;
        const url = `${ROOT_URL}/accounts/u/`
        if (token) {
            axios.get(url, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            .then((response) => {
                console.log("MOUNT STATE", response)
                if (response.data.email_confirmed) {
                    const user = {
                        user_id: response.data.user_id,
                        username: response.data.username,
                        first_name: response.data.first_name,
                        last_name: response.data.last_name,
                        profile_pic: response.data.profile_pic,
                        slug: response.data.slug,
                        last_login: response.data.last_login,
                        date_joined: response.data.date_joined
                    }
                    localStorage.setItem("user", JSON.stringify(user));
                    return this.props.history.push("/profile");
                };
                this.setState({
                    user: response.data,
                    emailConfirmed: response.data.email_confirmed,
                    isLoading: false
                });
            }).catch(error => {
                console.log("ERROR", error)
            });
        }
    }

    render() {

        if (this.state.isLoading) {
            return (
                <div className="uk-grid-collapse uk-margin-remove uk-flex-center uk-flex-middle uk-height-viewport"
                    data-uk-grid>
                    <div>
                        <span className="uk-padding-remove uk-margin-remove uk-spinner" data-uk-spinner="ratio: 1" />
                    </div>
                </div>
            )
        }

        return (
            <div className="uk-container uk-width-1-1">
                <div className="uk-grid-collapse uk-flex-center uk-flex-middle uk-height-viewport"
                    data-uk-grid>
                    <div className="uk-card uk-card-small uk-card-default uk-width-1-2@s uk-width-2-3@m uk-width-1-2@l">
                        <div className="uk-card-header uk-text-center">
                            <h4>Hi {this.state.user.first_name}!<br /><small>Please activate your account.</small></h4>
                        </div>
                        <EmailForm user={this.state.user} />
                    </div>
                </div>
            </div>
        );
    }
}

export default Auth;

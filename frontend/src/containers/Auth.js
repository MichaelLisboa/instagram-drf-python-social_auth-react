import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";
import InstagramLogin from 'react-instagram-login';


class Auth extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            isLoading: true
        };

        this.handleInstagramLogin = this.handleInstagramLogin.bind(this);
        this.handleInstagramFailed = this.handleInstagramFailed.bind(this);
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
                return this.props.history.push("/activate");
            }).catch(error => {
                console.log("ERROR", error)
            });
        } else {
            this.setState({
                isLoading: false
            })
        }
    }

    handleInstagramLogin = (token) => {
        this.setState({
            isLoading: true
        })
        axios.post(`${ROOT_URL}/accounts/convert-token/`, {token: token})
        .then((response) => {
            console.log("USER ID", response)
            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("refresh_token", response.data.refresh_token);
            this.props.history.push("/activate");
        }).catch(error => {
            console.log("ERROR", error)
        });
    }

    handleInstagramFailed = (token) => {
        return (
            <h1>Instagram auth failed.</h1>
        )
    }

    render() {

        const InstagramLoginButton = () =>
            <InstagramLogin
                tag="a"
                cssClass="uk-button uk-button-default"
                clientId="a2ca38f8d948449fb81136e7cdcfd1ad"
                buttonText="Login with Instagram"
                onSuccess={this.handleInstagramLogin}
                onFailure={this.handleInstagramFailed}
                implicitAuth={true}
            />

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
            <div className="uk-grid-collapse uk-margin-remove uk-flex-center uk-flex-middle uk-height-viewport"
                data-uk-grid>
                <div>
                    <InstagramLoginButton />
                </div>
            </div>
        );
    }
}

export default Auth;

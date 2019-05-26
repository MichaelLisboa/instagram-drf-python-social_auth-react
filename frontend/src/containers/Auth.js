import React, { Component } from 'react';
import axios from "axios";
import InstagramLogin from 'react-instagram-login';


class Auth extends Component {

    constructor (props) {
        super(props);
        this.state = { user: [] };
    }

    componentDidMount () {
        console.log("PLACEHOLDER", this.props)
    }

    render() {

        const responseInstagram = (token) => {
            this.props.history.push("/profile/");
            const body = {
                grant_type: "convert_token",
                client_id: "",
                client_secret: "",
                backend: "instagram",
                token: token
            }

            axios.post("/auth/convert-token", body)
                .then((response) => {
                    localStorage.setItem("access_token", response.data.access_token);
                    localStorage.setItem("refresh_token", response.data.refresh_token);
                }).catch(error => {
                    console.log("ERROR", error)
                });
        }

        return (
            <div>
            <InstagramLogin
                tag="a"
                cssClass="uk-button uk-button-default"
                clientId="a2ca38f8d948449fb81136e7cdcfd1ad"
                buttonText="Login with Instagram"
                onSuccess={responseInstagram}
                onFailure={responseInstagram}
                implicitAuth={true}
            />
            </div>
        );
    }
}

export default Auth;

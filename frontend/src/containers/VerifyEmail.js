import React, { Component } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";
import { NavLink } from "react-router-dom";

class VerifyEmail extends Component {

    constructor (props) {
        super(props);
        this.state = {
            user: [],
            status: '',
            message: '',
            emailConfirmed: false,
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
            if (response.data.status === 'success') {
                this.setState({
                    user: response.data.user,
                    status: response.data.status,
                    message: response.data.message
                })
                this.createSubscription(response.data.user.user_id);
            } else {
                this.setState({
                    status: response.data.status,
                    message: response.data.message,
                    isLoading: false
                })
            }
            console.log("STUFF", response)

        }).catch(error => {
            console.log("ERROR", error)
        });
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
            <div className="uk-container uk-flex uk-flex-center uk-flex-middle uk-height-viewport"
                data-uk-grid>
                <div className="uk-card uk-card-body uk-card-small uk-card-default uk-width-1-2@s uk-width-2-3@m uk-width-1-2@l">
                    <div className="uk-text-center">
                        <h4>Oops, account activation {this.state.status}!</h4>
                        <p>{this.state.message}</p>
                        { this.state.status === 'failed' &&
                        <NavLink
                            className="uk-button uk-button-default"
                            to="/">
                            Try again
                        </NavLink>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

export default VerifyEmail;

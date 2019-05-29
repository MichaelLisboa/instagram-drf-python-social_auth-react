import React, { Component, Fragment } from 'react';
import axios from "axios";
import {ROOT_URL} from "../constants/Urls";

class EmailForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            emailConfirmed: false,
            newEmail: '',
            formErrors: {
                newEmail: ''
            },
            emailValid: false,
            formValid: false
        }
    }

    handleInputChange = (event) => {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        },
        () => {
            this.validateField(name, value)
        });
    }

    handleUserInput = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        this.setState({
                [name]: value
            },
            () => {
                this.validateField(name, value)
            });
    }

    handleSubmit = (event) => {
        event.preventDefault();
        const id = this.props.user.user_id;
        const url = `${ROOT_URL}/accounts/update-email/${id}/`
        const body = {
            email: this.state.newEmail
        }
        const headers = {
            headers: {'Authorization': `Bearer ${localStorage.access_token}`}
        };

        axios.post(url, body, headers)
        .then((response) => {
            if (response.data.email_confirmed) this.setState({emailConfirmed: true});
        }).catch(error => {
            console.log("ERROR", error)
        });
    };

    resetForm = () => {
       this.setState({
           ...this.state,
           newEmail: ''
       })
    }

    validateField = (fieldName, value) => {
        let fieldValidationErrors = this.state.formErrors;
        let emailValid = this.state.emailValid;

        switch (fieldName) {
            case 'newEmail':
                emailValid = value.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i);
                fieldValidationErrors.newEmail = emailValid ? '' : ' is invalid';
                break;
            default:
                break;
        }
        this.setState({
            formErrors: fieldValidationErrors,
            emailValid: emailValid
        }, this.validateForm);
    }

    validateForm = () => {
        this.setState({
            formValid: this.state.emailValid
        });
    }

    errorClass = (error) => {
        return (error.length === 0 ? '' : 'uk-form-danger');
    }

    render () {
        return (
            <Fragment>
            { this.state.emailConfirmed ? <h1>MONKEY</h1> :
            <form
                id="contactForm"
                className="uk-form"
                onSubmit={this.handleSubmit}>
                <fieldset className="uk-fieldset">
                    <div className="uk-margin-small-top">
                        <label htmlFor="newEmail" className="uk-text-muted">
                            Email address
                            <input
                                name="newEmail"
                                type="text"
                                value={this.state.newEmail}
                                className={`uk-input uk-form-large ${this.errorClass(this.state.formErrors.newEmail)}`}
                                maxLength="100"
                                required
                                onChange={this.handleInputChange}
                                onBlur={this.handleUserInput}
                                onFocus={this.handleInputFocus}
                            />
                        </label>
                    </div>
                    <div className="uk-margin-large-bottom uk-margin-medium-top uk-text-right">
                        <button type="submit" className="uk-button uk-button-secondary uk-width-1-2 uk-width-1-3@s" disabled={!this.state.formValid}>Send</button>
                    </div>
                </fieldset>
            </form>
        }
        </Fragment>
        )
    }
}

export default EmailForm;

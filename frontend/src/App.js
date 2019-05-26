import React, { Component } from 'react';
import Router from "./NavRoutes";
import './App.css';


class App extends Component {

    constructor(props) {
        super(props);
        this.state = {}
        this.connecToServer = this.connecToServer.bind(this);
    }

    connecToServer() {
        fetch('/');
    }

    componentDidMount() {
        this.connecToServer();
    }

    render() {
        return (
            <Router />
        );
    }
}

export default App;

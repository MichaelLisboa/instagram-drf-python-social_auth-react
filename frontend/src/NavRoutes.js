import React from "react";
import { BrowserRouter as Router, Switch } from "react-router-dom";
import ScrollToTopRoute from "./lib/ScrollToTopRoute";

import Auth from "./containers/Auth";
import Activate from "./containers/Activate";
import VerifyEmail from "./containers/VerifyEmail";
import Profile from "./containers/Profile";

const NavRoutes = () => {
    return (
        <Router>
            <main>
                <Switch>
                    <ScrollToTopRoute exact path="/verify/:uid/:token" component={VerifyEmail}/>
                    <ScrollToTopRoute path="/login" component={Auth}/>
                    <ScrollToTopRoute path="/profile" component={Profile}/>
                    <ScrollToTopRoute path="/activate" component={Activate}/>
                    <ScrollToTopRoute path="/*" component={Auth}/>
                </Switch>
            </main>
        </Router>
    )
}

export default NavRoutes;

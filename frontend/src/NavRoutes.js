import React from "react";
import { BrowserRouter as Router, Switch } from "react-router-dom";
import ScrollToTopRoute from "./lib/ScrollToTopRoute";

import Auth from "./containers/Auth";
import Profile from "./containers/Profile";
import VerifyEmail from "./containers/VerifyEmail";

const NavRoutes = () => {
    return (
        <Router>
            <main>
                <Switch>
                    <ScrollToTopRoute exact path="/verify/:uid/:token" component={VerifyEmail}/>
                    <ScrollToTopRoute path="/login" component={Auth}/>
                    <ScrollToTopRoute path="/profile" component={Profile}/>
                    <ScrollToTopRoute path="/*" component={Auth}/>
                </Switch>
            </main>
        </Router>
    )
}

export default NavRoutes;

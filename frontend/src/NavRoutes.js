import React from "react";
import { BrowserRouter as Router, Switch } from "react-router-dom";
import ScrollToTopRoute from "./lib/ScrollToTopRoute";

import Auth from "./containers/Auth";
import Profile from "./containers/Profile";

const NavRoutes = () => {
    return (
        <Router>
            <main>
                <Switch>
                    <ScrollToTopRoute path="/login" component={Auth}/>
                    <ScrollToTopRoute path="/profile" component={Profile}/>
                    <ScrollToTopRoute path="/*" component={Auth}/>
                </Switch>
            </main>
        </Router>
    )
}

export default NavRoutes;

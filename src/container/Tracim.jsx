import React from 'react'
import { connect } from 'react-redux'
import Footer from '../component/FooterTpl.jsx'
import HeaderContainer from './Header.jsx'
import Login from './Login.jsx'
import Page from './Page.jsx'
import Home from './Home.jsx'
import {
  Route,
  withRouter
} from 'react-router-dom'
import PrivateRoute from './PrivateRoute.jsx'

class Tracim extends React.Component {
  render () {
    return (
      <div>
        <HeaderContainer />

        <br /><hr /><br />

        <PrivateRoute exact path='/' component={Home} />
        <Route path='/login' component={Login} />
        <PrivateRoute path='/page' component={Page} />

        <Footer />
      </div>
    )
  }
}

const mapStateToProps = ({ user }) => ({ user })
export default withRouter(connect(mapStateToProps)(Tracim))

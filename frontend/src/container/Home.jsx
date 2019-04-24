import React from 'react'
import { connect } from 'react-redux'
import classnames from 'classnames'
import { withRouter } from 'react-router-dom'
import { translate } from 'react-i18next'
import appFactory from '../appFactory.js'
import {
  workspaceConfig,
  PAGE
} from '../helper.js'
import Card from '../component/common/Card/Card.jsx'
import CardHeader from '../component/common/Card/CardHeader.jsx'
import CardBody from '../component/common/Card/CardBody.jsx'
import HomeNoWorkspace from '../component/Home/HomeNoWorkspace.jsx'
import HomeHasWorkspace from '../component/Home/HomeHasWorkspace.jsx'
import { setBreadcrumbs } from '../action-creator.sync.js'

class Home extends React.Component {
  constructor (props) {
    super(props)
    props.dispatch(setBreadcrumbs([{
      url: PAGE.HOME,
      label: props.t('Home'),
      type: 'CORE'
    }]))
  }

  handleClickCreateWorkspace = e => {
    e.preventDefault()
    const { props } = this
    props.renderAppPopupCreation(workspaceConfig, props.user, null, null)
  }

  render () {
    const { props } = this

    if (!props.system.workspaceListLoaded) return null

    const styleHomepage = {
      display: 'flex',
      alignItems: 'center',
      flexDirection: 'column',
      justifyContent: 'center',
      height: '100%'
    }

    return (
      <div className='tracim__content fullWidthFullHeight'>
        <div className='tracim__content-scrollview fullWidthFullHeight'>
          <section
            className={classnames('homepage', props.workspaceList.length === 0 ? 'primaryColorBg' : '')}
            style={styleHomepage}
          >
            <Card customClass='homepagecard'>
              <CardHeader displayHeader={false} />

              <CardBody formClass='homepagecard__body'>
                {props.workspaceList.length > 0
                  ? <HomeHasWorkspace user={props.user} />
                  : <HomeNoWorkspace
                    canCreateWorkspace={props.canCreateWorkspace}
                    onClickCreateWorkspace={this.handleClickCreateWorkspace}
                  />
                }
              </CardBody>
            </Card>
          </section>
        </div>
      </div>
    )
  }
}

const mapStateToProps = ({ user, workspaceList, system }) => ({ user, workspaceList, system })
export default connect(mapStateToProps)(withRouter(appFactory(translate()(Home))))

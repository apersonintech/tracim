import React from 'react'
import { connect } from 'react-redux'
import { translate } from 'react-i18next'
import { newFlashMessage } from '../../action-creator.sync.js'

export class Password extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      oldPassword: '',
      newPassword: '',
      newPassword2: ''
    }
  }

  handleChangeOldPassword = e => this.setState({oldPassword: e.target.value})

  handleChangeNewPassword = e => this.setState({newPassword: e.target.value})

  handleChangeNewPassword2 = e => this.setState({newPassword2: e.target.value})

  handleClickSubmit = () => {
    const { props, state } = this

    if (state.newPassword.length > 30) {
      props.dispatch(newFlashMessage(props.t('New password is too long'), 'warning'))
      return
    }

    if (state.newPassword !== state.newPassword2) {
      props.dispatch(newFlashMessage(props.t('New passwords are different'), 'warning'))
      return
    }

    props.onClickSubmit(state.oldPassword, state.newPassword, state.newPassword2)
  }

  render () {
    const { props, state } = this

    return (
      <div className='account__userpreference__setting__personaldata'>
        <div className='personaldata__sectiontitle subTitle ml-2 ml-sm-0'>
          {props.t('Change your password')}
        </div>

        <div className='personaldata__text ml-2 ml-sm-0' />

        <form className='personaldata__form mr-5'>
          <div className='d-flex align-items-center flex-wrap mb-4'>
            <input
              className='personaldata__form__txtinput primaryColorBorderLighten form-control'
              type='password'
              placeholder={props.t('Old password')}
              onChange={this.handleChangeOldPassword}
            />
            {props.displayAdminInfo &&
              <div className='personaldata__form__txtinput__info'>
                <i className='personaldata__form__txtinput__info__icon fa fa-lightbulb-o' />
                {props.t('This requires your administrator password')}
              </div>
            }
          </div>

          <div className='d-flex align-items-center flex-wrap mb-4'>
            <input
              className='personaldata__form__txtinput primaryColorBorderLighten form-control'
              type='password'
              placeholder={props.t('New password')}
              onChange={this.handleChangeNewPassword}
            />
          </div>

          <div className='d-flex align-items-center flex-wrap mb-4'>
            <input
              className='personaldata__form__txtinput primaryColorBorderLighten form-control'
              type='password'
              placeholder={props.t('Repeat new password')}
              onChange={this.handleChangeNewPassword2}
            />
          </div>

          <button
            type='button'
            className='personaldata__form__button btn outlineTextBtn primaryColorBorderLighten primaryColorBgHover primaryColorBorderDarkenHover'
            onClick={this.handleClickSubmit}
            disabled={state.oldPassword === '' || state.newPassword === '' || state.newPassword2 === ''}
          >
            {props.t('Send')}
          </button>
        </form>

      </div>
    )
  }
}

const mapStateToProps = () => ({})
export default connect(mapStateToProps)(translate()(Password))

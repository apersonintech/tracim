import React from 'react'
import { translate } from 'react-i18next'
import PropTypes from 'prop-types'
import classnames from 'classnames'
// import FileItem from './ContentItem.jsx'
// import PopupExtandedAction from '../../container/PopupExtandedAction.jsx'
import SubDropdownCreateButton from '../common/Input/SubDropdownCreateButton.jsx'
import BtnExtandedAction from './BtnExtandedAction.jsx'

class Folder extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      open: false
    }
  }

  handleClickToggleFolder = () => {
    // const { props, state } = this
    if (!state.open && props.folderData.content.length === 0) props.onClickFolder(props.folderData.id)
    this.setState({open: !this.state.open})
  }

  handleClickCreateContent = (e, folder, type) => {
    e.stopPropagation() // because we have a link inside a link (togler and newFile)
    this.props.onClickCreateContent(folder, type)
  }

  render () {
    const { props, state } = this

    return (
      <div className={classnames('folder', {'active': state.open && props.folderData.content.length > 0, 'item-last': props.isLast})}>
        <div
          className='folder__header align-items-center primaryColorBgLightenHover'
          onClick={this.handleClickToggleFolder}
        >

          <div className='folder__header__triangleborder'>
            <div className='folder__header__triangleborder__triangle' />
          </div>

          <div className='folder__header__icon'>
            <i className={classnames('fa fa-fw', {'fa-folder-open-o': state.open, 'fa-folder-o': !state.open})} />
          </div>

          <div className='folder__header__name'>
            { props.folderData.label }
          </div>

          <div className='folder__header__button'>
            {props.idRoleUserWorkspace >= 2 &&
              <div className='folder__header__button__addbtn'>
                <button
                  className='folder__header__button__addbtn__text btn outlineTextBtn primaryColorBorder primaryColorBgHover primaryColorBorderDarkenHover dropdown-toggle'
                  type='button'
                  id='dropdownMenuButton'
                  data-toggle='dropdown'
                  aria-haspopup='true'
                  aria-expanded='false'
                  onClick={e => e.stopPropagation()}
                >
                  {`${props.t('Create in folder')}...`}
                </button>

                <div className='addbtn__subdropdown dropdown-menu' aria-labelledby='dropdownMenuButton'>
                  <SubDropdownCreateButton
                    idFolder={null}
                    availableApp={props.availableApp}
                    onClickCreateContent={props.onClickCreateContent}
                  />
                </div>

                <div className='d-none d-md-flex'>
                  <BtnExtandedAction
                    idRoleUserWorkspace={props.idRoleUserWorkspace}
                    onClickExtendedAction={{
                      edit: e => props.onClickExtendedAction.edit(e, props.folderData),
                      move: e => props.onClickExtendedAction.move(e, props.folderData),
                      download: e => props.onClickExtendedAction.download(e, props.folderData),
                      archive: e => props.onClickExtendedAction.archive(e, props.folderData),
                      delete: e => props.onClickExtendedAction.delete(e, props.folderData)
                    }}
                  />
                </div>
              </div>
            }
          </div>

          <div className='folder__header__status' />

        </div>

        <div className='folder__content'>
          {
          //   folderData.map((c, i) => c.type === 'folder'
          //   ? <Folder
          //     app={app}
          //     folderData={c}
          //     onClickItem={onClickItem}
          //     onClickExtendedAction={onClickExtendedAction}
          //     onClickFolder={onClickFolder}
          //     isLast={isLast}
          //     t={t}
          //     key={c.id}
          //   />
          //   : <FileItem
          //     icon={(app[c.type] || {icon: ''}).icon}
          //     name={c.title}
          //     type={c.type}
          //     status={c.status}
          //     onClickItem={() => onClickItem(c)}
          //     onClickExtendedAction={{
          //       // we have to use the event here because it is the only place where we also have the content (c)
          //       edit: e => onClickExtendedAction.edit(e, c),
          //       move: e => onClickExtendedAction.move(e, c),
          //       download: e => onClickExtendedAction.download(e, c),
          //       archive: e => onClickExtendedAction.archive(e, c),
          //       delete: e => onClickExtendedAction.delete(e, c)
          //     }}
          //     isLast={isLast && i === folderData.content.length - 1}
          //     key={c.id}
          //   />
          // )
          }
        </div>
      </div>
    )
  }
}

export default translate()(Folder)

Folder.propTypes = {
  folderData: PropTypes.object,
  app: PropTypes.array,
  onClickItem: PropTypes.func.isRequired,
  onClickFolder: PropTypes.func.isRequired,
  isLast: PropTypes.bool.isRequired
}

import React from 'react'
import { translate } from 'react-i18next'
import { Checkbox } from 'tracim_frontend_lib'

const FolderAdvanced = props => {
  return (
    <div className='folder_advanced-content'>
      <div className='formBlock folder_advanced__content'>
        <div className='formBlock__title folder_advanced__content__title'>
          {props.t('Allowed content type for this folder')}
        </div>

        <form className='formBlock__field folder_advanced__content__form'>
          {props.tracimAppList.map(app =>
            <div
              className='folder_advanced__content__form__type'
              onClick={() => props.onClickApp(app.slug)}
              key={app.slug}
            >
              <Checkbox
                name={app.label}
                checked={props.folderSubContentType.includes(app.slug)}
                onClickCheckbox={() => props.onClickApp(app.slug)}
                styleLabel={{margin: '0 8px 0 0'}}
                styleCheck={{top: '-5px'}}
              />

              <i
                className={`folder_advanced__content__form__type__icon fa fa-fw fa-${app.fa_icon}`}
                style={{color: app.hexcolor}}
              />

              <div className='folder_advanced__content__form__type__label'>
                {app.label}
              </div>
            </div>
          )}
        </form>
      </div>
    </div>
  )
}

export default translate()(FolderAdvanced)
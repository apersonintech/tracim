# coding: utf-8
from configparser import ConfigParser
import os
from radicale.config import Configuration as RadicaleConfiguration
from radicale.config import load as load_radicale_config

from tracim_backend.config import CFG
from tracim_backend.exceptions import ConfigurationError
from tracim_backend.lib.utils.logger import logger
from tracim_backend.lib.utils.utils import sliced_dict

RADICALE_MAIN_SECTION = "caldav"
RADICALE_SUBMAIN_SECTION = "radicale"


class CaldavAppFactory(object):
    def __init__(self, **settings):
        logger.info(self, "Add additional radicale config")
        radicale_config = load_radicale_config(())
        additional_config = self._parse_additional_radicale_config(radicale_config, settings)
        self.app_config = CFG(settings)
        additional_config["storage"][
            "filesystem_folder"
        ] = self.app_config.CALDAV__RADICALE__STORAGE__FILESYSTEM_FOLDER
        radicale_config.update(additional_config)
        self.radicale_config = radicale_config
        self.create_dir_tree(self.radicale_config, self.app_config)

    def create_dir_tree(self, radicale_config: ConfigParser, app_config: CFG):
        # FIXME - G.M - 2019-03-08 - create dir tree if not exist in order
        # to allow item creation without trouble in radicale
        storage_path = radicale_config.get("storage", "filesystem_folder")
        sub_dir_storage_path = os.path.join(storage_path, "collection-root")
        parent_folder = os.path.dirname(storage_path)
        if not os.path.isdir(parent_folder):
            raise ConfigurationError(
                "{} is not a correct folder, can't set properly storage folder of radicale".format(
                    parent_folder
                )
            )
        user_agenda_dir = os.path.join(
            sub_dir_storage_path,
            app_config.RADICALE__CALENDAR_DIR,
            app_config.RADICALE__USER_SUBDIR,
        )
        os.makedirs(user_agenda_dir, exist_ok=True)
        workspace_agenda_dir = os.path.join(
            sub_dir_storage_path,
            app_config.RADICALE__CALENDAR_DIR,
            app_config.RADICALE__WORKSPACE_SUBDIR,
        )
        os.makedirs(workspace_agenda_dir, exist_ok=True)

        user_addressbook_dir = os.path.join(
            sub_dir_storage_path,
            app_config.RADICALE__ADDRESSBOOK_DIR,
            app_config.RADICALE__USER_SUBDIR,
        )
        os.makedirs(user_addressbook_dir, exist_ok=True)
        workspace_addressbook_dir = os.path.join(
            sub_dir_storage_path,
            app_config.RADICALE__ADDRESSBOOK_DIR,
            app_config.RADICALE__WORKSPACE_SUBDIR,
        )
        os.makedirs(workspace_addressbook_dir, exist_ok=True)

    def _parse_additional_radicale_config(
        self, config: RadicaleConfiguration, settings: dict
    ) -> dict:
        """
        Get settings params beginning with
        "RADICALE_MAIN_SECTION.RADICALE_SUBMAIN_SECTION." to radicale config.
        """
        update_config = {}
        radicales_params = sliced_dict(
            data=settings,
            beginning_key_string="{}.{}.".format(RADICALE_MAIN_SECTION, RADICALE_SUBMAIN_SECTION),
        )
        for param_name, value in radicales_params.items():
            parameter_parts = param_name.split(".")
            assert len(parameter_parts) == 4
            (
                main_section,
                sub_main_section,
                radicale_section,
                radicale_param_config,
            ) = parameter_parts
            assert main_section == "caldav"
            assert sub_main_section == "radicale"
            if not update_config.get(radicale_section):
                update_config[radicale_section] = {}
            logger.debug(
                self,
                "Prepare overriding radicale config: {} : {}".format(param_name, value),
            )
            update_config[radicale_section][radicale_param_config] = value
        logger.debug(self, "Overriding radicale config")
        return update_config

    def get_wsgi_app(self):
        from radicale import Application as RadicaleApplication

        return RadicaleApplication(self.radicale_config)

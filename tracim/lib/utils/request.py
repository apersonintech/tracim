# -*- coding: utf-8 -*-
from pyramid.request import Request
from sqlalchemy.orm.exc import NoResultFound

from tracim.exceptions import NotAuthenticated
from tracim.exceptions import WorkspaceNotFoundInTracimRequest
from tracim.exceptions import UserNotFoundInTracimRequest
from tracim.exceptions import UserDoesNotExist
from tracim.exceptions import WorkspaceNotFound
from tracim.exceptions import ImmutableAttribute
from tracim.lib.core.user import UserApi
from tracim.lib.core.workspace import WorkspaceApi
from tracim.lib.utils.authorization import JSONDecodeError

from tracim.models import User
from tracim.models.data import Workspace


class TracimRequest(Request):
    """
    Request with tracim specific params/methods
    """
    def __init__(
            self,
            environ,
            charset=None,
            unicode_errors=None,
            decode_param_names=None,
            **kw
    ):
        super().__init__(
            environ,
            charset,
            unicode_errors,
            decode_param_names,
            **kw
        )
        # Current workspace, found in request path
        self._current_workspace = None  # type: Workspace

        # Candidate workspace found in request body
        self._candidate_workspace = None  # type: Workspace

        # Authenticated user
        self._current_user = None  # type: User

        # User found from request headers, content, distinct from authenticated
        # user
        self._candidate_user = None  # type: User

        # INFO - G.M - 18-05-2018 - Close db at the end of the request
        self.add_finished_callback(self._cleanup)

    @property
    def current_workspace(self) -> Workspace:
        """
        Get current workspace of the request according to authentification and
        request headers (to retrieve workspace). Setted by default value the
        first time if not configured.
        :return: Workspace of the request
        """
        if self._current_workspace is None:
            self._current_workspace = self._get_current_workspace(self.current_user, self)
        return self._current_workspace

    @current_workspace.setter
    def current_workspace(self, workspace: Workspace) -> None:
        """
        Setting current_workspace
        :param workspace:
        :return:
        """
        if self._current_workspace is not None:
            raise ImmutableAttribute(
                "Can't modify already setted current_workspace"
            )
        self._current_workspace = workspace

    @property
    def current_user(self) -> User:
        """
        Get user from authentication mecanism.
        """
        if self._current_user is None:
            self.current_user = self._get_auth_safe_user(self)
        return self._current_user

    @current_user.setter
    def current_user(self, user: User) -> None:
        if self._current_user is not None:
            raise ImmutableAttribute(
                "Can't modify already setted current_user"
            )
        self._current_user = user

    # TODO - G.M - 24-05-2018 - Find a better naming for this ?
    @property
    def candidate_user(self) -> User:
        """
        Get user from headers/body request. This user is not
        the one found by authentication mecanism. This user
        can help user to know about who one page is about in
        a similar way as current_workspace.
        """
        if self._candidate_user is None:
            self.candidate_user = self._get_candidate_user(self)
        return self._candidate_user

    @property
    def candidate_workspace(self) -> Workspace:
        """
        Get workspace from headers/body request. This workspace is not
        the one found from path. Its the one from json body.
        """
        if self._candidate_workspace is None:
            self._candidate_workspace = self._get_candidate_workspace(
                self.current_user,
                self
            )
        return self._candidate_workspace

    def _cleanup(self, request: 'TracimRequest') -> None:
        """
        Close dbsession at the end of the request in order to avoid exception
        about not properly closed session or "object created in another thread"
        issue
        see https://github.com/tracim/tracim_backend/issues/62
        :param request: same as self, request
        :return: nothing.
        """
        self._current_user = None
        self._current_workspace = None
        self.dbsession.close()


    @candidate_user.setter
    def candidate_user(self, user: User) -> None:
        if self._candidate_user is not None:
            raise ImmutableAttribute(
                "Can't modify already setted candidate_user"
            )
        self._candidate_user = user

    ###
    # Utils for TracimRequest
    ###

    def _get_candidate_user(
            self,
            request: 'TracimRequest',
    ) -> User:
        """
        Get candidate user
        :param request: pyramid request
        :return: user found from header/body
        """
        app_config = request.registry.settings['CFG']
        uapi = UserApi(None, session=request.dbsession, config=app_config)

        try:
            login = None
            if 'user_id' in request.matchdict:
                login = request.matchdict['user_id']
            if not login:
                raise UserNotFoundInTracimRequest('You request a candidate user but the context not permit to found one')  # nopep8
            user = uapi.get_one(login)
        except UserNotFoundInTracimRequest as exc:
            raise UserDoesNotExist('User {} not found'.format(login)) from exc
        return user

    def _get_auth_safe_user(
            self,
            request: 'TracimRequest',
    ) -> User:
        """
        Get current pyramid authenticated user from request
        :param request: pyramid request
        :return: current authenticated user
        """
        app_config = request.registry.settings['CFG']
        uapi = UserApi(None, session=request.dbsession, config=app_config)
        try:
            login = request.authenticated_userid
            if not login:
                raise UserNotFoundInTracimRequest('You request a current user but the context not permit to found one')  # nopep8
            user = uapi.get_one_by_email(login)
        except (UserDoesNotExist, UserNotFoundInTracimRequest) as exc:
            raise NotAuthenticated('User {} not found'.format(login)) from exc
        return user

    def _get_current_workspace(
            self,
            user: User,
            request: 'TracimRequest'
    ) -> Workspace:
        """
        Get current workspace from request
        :param user: User who want to check the workspace
        :param request: pyramid request
        :return: current workspace
        """
        workspace_id = ''
        try:
            if 'workspace_id' in request.matchdict:
                workspace_id = request.matchdict['workspace_id']
            if not workspace_id:
                raise WorkspaceNotFoundInTracimRequest('No workspace_id property found in request')
            wapi = WorkspaceApi(
                current_user=user,
                session=request.dbsession,
                config=request.registry.settings['CFG']
            )
            workspace = wapi.get_one(workspace_id)
        except JSONDecodeError:
            raise WorkspaceNotFound('Bad json body')
        except NoResultFound:
            raise WorkspaceNotFound(
                'Workspace {} does not exist '
                'or is not visible for this user'.format(workspace_id)
            )
        return workspace

    def _get_candidate_workspace(
            self,
            user: User,
            request: 'TracimRequest'
    ) -> Workspace:
        """
        Get current workspace from request
        :param user: User who want to check the workspace
        :param request: pyramid request
        :return: current workspace
        """
        workspace_id = ''
        try:
            if 'new_workspace_id' in request.json_body:
                workspace_id = request.json_body['new_workspace_id']
            if not workspace_id:
                raise WorkspaceNotFoundInTracimRequest('No new_workspace_id property found in body')
            wapi = WorkspaceApi(
                current_user=user,
                session=request.dbsession,
                config=request.registry.settings['CFG']
            )
            workspace = wapi.get_one(workspace_id)
        except JSONDecodeError:
            raise WorkspaceNotFound('Bad json body')
        except NoResultFound:
            raise WorkspaceNotFound(
                'Workspace {} does not exist '
                'or is not visible for this user'.format(workspace_id)
            )
        return workspace

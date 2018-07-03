# coding=utf-8
import typing
from datetime import datetime

from slugify import slugify
from sqlalchemy.orm import Session
from tracim import CFG
from tracim.models import User
from tracim.models.auth import Profile
from tracim.models.data import Content
from tracim.models.data import ContentRevisionRO
from tracim.models.data import Workspace, UserRoleInWorkspace
from tracim.models.workspace_menu_entries import default_workspace_menu_entry
from tracim.models.workspace_menu_entries import WorkspaceMenuEntry
from tracim.models.contents import ContentTypeLegacy as ContentType


class MoveParams(object):
    """
    Json body params for move action model
    """
    def __init__(self, new_parent_id: str, new_workspace_id: str = None) -> None:  # nopep8
        self.new_parent_id = new_parent_id
        self.new_workspace_id = new_workspace_id


class LoginCredentials(object):
    """
    Login credentials model for login model
    """

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password


class WorkspaceAndContentPath(object):
    """
    Paths params with workspace id and content_id model
    """
    def __init__(self, workspace_id: int, content_id: int) -> None:
        self.content_id = content_id
        self.workspace_id = workspace_id


class CommentPath(object):
    """
    Paths params with workspace id and content_id and comment_id model
    """
    def __init__(
        self,
        workspace_id: int,
        content_id: int,
        comment_id: int
    ) -> None:
        self.content_id = content_id
        self.workspace_id = workspace_id
        self.comment_id = comment_id


class ContentFilter(object):
    """
    Content filter model
    """
    def __init__(
            self,
            parent_id: int = None,
            show_archived: int = 0,
            show_deleted: int = 0,
            show_active: int = 1,
    ) -> None:
        self.parent_id = parent_id
        self.show_archived = bool(show_archived)
        self.show_deleted = bool(show_deleted)
        self.show_active = bool(show_active)


class ContentCreation(object):
    """
    Content creation model
    """
    def __init__(
            self,
            label: str,
            content_type: str,
    ) -> None:
        self.label = label
        self.content_type = content_type


class CommentCreation(object):
    """
    Comment creation model
    """
    def __init__(
            self,
            raw_content: str,
    ) -> None:
        self.raw_content = raw_content


class SetContentStatus(object):
    """
    Set content status
    """
    def __init__(
            self,
            status: str,
    ) -> None:
        self.status = status


class TextBasedContentUpdate(object):
    """
    TextBasedContent update model
    """
    def __init__(
            self,
            label: str,
            raw_content: str,
    ) -> None:
        self.label = label
        self.raw_content = raw_content


class UserInContext(object):
    """
    Interface to get User data and User data related to context.
    """

    def __init__(self, user: User, dbsession: Session, config: CFG):
        self.user = user
        self.dbsession = dbsession
        self.config = config

    # Default

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def user_id(self) -> int:
        return self.user.user_id

    @property
    def public_name(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        return self.user.display_name

    @property
    def created(self) -> datetime:
        return self.user.created

    @property
    def is_active(self) -> bool:
        return self.user.is_active

    @property
    def timezone(self) -> str:
        return self.user.timezone

    @property
    def profile(self) -> Profile:
        return self.user.profile.name

    # Context related

    @property
    def calendar_url(self) -> typing.Optional[str]:
        # TODO - G-M - 20-04-2018 - [Calendar] Replace calendar code to get
        # url calendar url.
        #
        # from tracim.lib.calendar import CalendarManager
        # calendar_manager = CalendarManager(None)
        # return calendar_manager.get_workspace_calendar_url(self.workspace_id)
        return None

    @property
    def avatar_url(self) -> typing.Optional[str]:
        # TODO - G-M - 20-04-2018 - [Avatar] Add user avatar feature
        return None


class WorkspaceInContext(object):
    """
    Interface to get Workspace data and Workspace data related to context.
    """

    def __init__(self, workspace: Workspace, dbsession: Session, config: CFG):
        self.workspace = workspace
        self.dbsession = dbsession
        self.config = config

    @property
    def workspace_id(self) -> int:
        """
        numeric id of the workspace.
        """
        return self.workspace.workspace_id

    @property
    def id(self) -> int:
        """
        alias of workspace_id
        """
        return self.workspace_id

    @property
    def label(self) -> str:
        """
        get workspace label
        """
        return self.workspace.label

    @property
    def description(self) -> str:
        """
        get workspace description
        """
        return self.workspace.description

    @property
    def slug(self) -> str:
        """
        get workspace slug
        """
        return slugify(self.workspace.label)

    @property
    def sidebar_entries(self) -> typing.List[WorkspaceMenuEntry]:
        """
        get sidebar entries, those depends on activated apps.
        """
        # TODO - G.M - 22-05-2018 - Rework on this in
        # order to not use hardcoded list
        # list should be able to change (depending on activated/disabled
        # apps)
        return default_workspace_menu_entry(self.workspace)


class UserRoleWorkspaceInContext(object):
    """
    Interface to get UserRoleInWorkspace data and related content

    """
    def __init__(
            self,
            user_role: UserRoleInWorkspace,
            dbsession: Session,
            config: CFG,
    )-> None:
        self.user_role = user_role
        self.dbsession = dbsession
        self.config = config

    @property
    def user_id(self) -> int:
        """
        User who has the role has this id
        :return: user id as integer
        """
        return self.user_role.user_id

    @property
    def workspace_id(self) -> int:
        """
        This role apply only on the workspace with this workspace_id
        :return: workspace id as integer
        """
        return self.user_role.workspace_id

    # TODO - G.M - 23-05-2018 - Check the API spec for this this !

    @property
    def role_id(self) -> int:
        """
        role as int id, each value refer to a different role.
        """
        return self.user_role.role

    @property
    def role(self) -> str:
        return self.role_slug

    @property
    def role_slug(self) -> str:
        """
        simple name of the role of the user.
        can be anything from UserRoleInWorkspace SLUG, like
        'not_applicable', 'reader',
        'contributor', 'content-manager', 'workspace-manager'
        :return: user workspace role as slug.
        """
        return UserRoleInWorkspace.SLUG[self.user_role.role]

    @property
    def user(self) -> UserInContext:
        """
        User who has this role, with context data
        :return: UserInContext object
        """
        return UserInContext(
            self.user_role.user,
            self.dbsession,
            self.config
        )

    @property
    def workspace(self) -> WorkspaceInContext:
        """
        Workspace related to this role, with his context data
        :return: WorkspaceInContext object
        """
        return WorkspaceInContext(
            self.user_role.workspace,
            self.dbsession,
            self.config
        )


class ContentInContext(object):
    """
    Interface to get Content data and Content data related to context.
    """

    def __init__(self, content: Content, dbsession: Session, config: CFG):
        self.content = content
        self.dbsession = dbsession
        self.config = config

    # Default
    @property
    def content_id(self) -> int:
        return self.content.content_id

    @property
    def id(self) -> int:
        return self.content_id

    @property
    def parent_id(self) -> int:
        """
        Return parent_id of the content
        """
        return self.content.parent_id

    @property
    def workspace_id(self) -> int:
        return self.content.workspace_id

    @property
    def label(self) -> str:
        return self.content.label

    @property
    def content_type(self) -> str:
        content_type = ContentType(self.content.type)
        return content_type.slug

    @property
    def sub_content_types(self) -> typing.List[str]:
        return [_type.slug for _type in self.content.get_allowed_content_types()]  # nopep8

    @property
    def status(self) -> str:
        return self.content.status

    @property
    def is_archived(self):
        return self.content.is_archived

    @property
    def is_deleted(self):
        return self.content.is_deleted

    @property
    def raw_content(self):
        return self.content.description

    @property
    def author(self):
        return UserInContext(
            dbsession=self.dbsession,
            config=self.config,
            user=self.content.first_revision.owner
        )

    @property
    def current_revision_id(self):
        return self.content.revision_id

    @property
    def created(self):
        return self.content.created

    @property
    def modified(self):
        return self.updated

    @property
    def updated(self):
        return self.content.updated

    @property
    def last_modifier(self):
        return UserInContext(
            dbsession=self.dbsession,
            config=self.config,
            user=self.content.last_revision.owner
        )

    # Context-related
    @property
    def show_in_ui(self):
        # TODO - G.M - 31-05-2018 - Enable Show_in_ui params
        # if false, then do not show content in the treeview.
        # This may his maybe used for specific contents or for sub-contents.
        # Default is True.
        # In first version of the API, this field is always True
        return True

    @property
    def slug(self):
        return slugify(self.content.label)


class RevisionInContext(object):
    """
    Interface to get Content data and Content data related to context.
    """

    def __init__(self, content_revision: ContentRevisionRO, dbsession: Session, config: CFG):
        assert content_revision is not None
        self.revision = content_revision
        self.dbsession = dbsession
        self.config = config

    # Default
    @property
    def content_id(self) -> int:
        return self.revision.content_id

    @property
    def id(self) -> int:
        return self.content_id

    @property
    def parent_id(self) -> int:
        """
        Return parent_id of the content
        """
        return self.revision.parent_id

    @property
    def workspace_id(self) -> int:
        return self.revision.workspace_id

    @property
    def label(self) -> str:
        return self.revision.label

    @property
    def content_type(self) -> str:
        content_type = ContentType(self.revision.type)
        if content_type:
            return content_type.slug
        else:
            return None

    @property
    def sub_content_types(self) -> typing.List[str]:
        return [_type.slug for _type
                in self.revision.node.get_allowed_content_types()]

    @property
    def status(self) -> str:
        return self.revision.status

    @property
    def is_archived(self) -> bool:
        return self.revision.is_archived

    @property
    def is_deleted(self) -> bool:
        return self.revision.is_deleted

    @property
    def raw_content(self) -> str:
        return self.revision.description

    @property
    def author(self) -> UserInContext:
        return UserInContext(
            dbsession=self.dbsession,
            config=self.config,
            user=self.revision.owner
        )

    @property
    def revision_id(self) -> int:
        return self.revision.revision_id

    @property
    def created(self) -> datetime:
        return self.updated

    @property
    def modified(self) -> datetime:
        return self.updated

    @property
    def updated(self) -> datetime:
        return self.revision.updated

    @property
    def next_revision(self) -> typing.Optional[ContentRevisionRO]:
        """
        Get next revision (later revision)
        :return: next_revision
        """
        next_revision = None
        revisions = self.revision.node.revisions
        # INFO - G.M - 2018-06-177 - Get revisions more recent that
        # current one
        next_revisions = [
            revision for revision in revisions
            if revision.revision_id > self.revision.revision_id
        ]
        if next_revisions:
            # INFO - G.M - 2018-06-177 -sort revisions by date
            sorted_next_revisions = sorted(
                next_revisions,
                key=lambda revision: revision.updated
            )
            # INFO - G.M - 2018-06-177 - return only next revision
            return sorted_next_revisions[0]
        else:
            return None

    @property
    def comment_ids(self) -> typing.List[int]:
        """
        Get list of ids of all current revision related comments
        :return: list of comments ids
        """
        comments = self.revision.node.get_comments()
        # INFO - G.M - 2018-06-177 - Get comments more recent than revision.
        revision_comments = [
            comment for comment in comments
            if comment.created > self.revision.updated
        ]
        if self.next_revision:
            # INFO - G.M - 2018-06-177 - if there is a revision more recent
            # than current remove comments from theses rev (comments older
            # than next_revision.)
            revision_comments = [
                comment for comment in revision_comments
                if comment.created < self.next_revision.updated
            ]
        sorted_revision_comments = sorted(
            revision_comments,
            key=lambda revision: revision.created
        )
        comment_ids = []
        for comment in sorted_revision_comments:
            comment_ids.append(comment.content_id)
        return comment_ids

    # Context-related
    @property
    def show_in_ui(self) -> bool:
        # TODO - G.M - 31-05-2018 - Enable Show_in_ui params
        # if false, then do not show content in the treeview.
        # This may his maybe used for specific contents or for sub-contents.
        # Default is True.
        # In first version of the API, this field is always True
        return True

    @property
    def slug(self) -> str:
        return slugify(self.revision.label)

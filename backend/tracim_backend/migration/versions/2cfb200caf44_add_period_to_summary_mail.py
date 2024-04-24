"""add_period_to_summary_mail

Revision ID: 2cfb200caf44
Revises: 8a9d929b44b9
Create Date: 2024-04-08 16:38:56.849952

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "2cfb200caf44"
down_revision = "8a9d929b44b9"

# INFO - CH - 2024-04-09 - This migration aim to update the CONSTRAINT emailnotificationtype
# on table user_workspace.
# Problem is, SQLite doesn't allow to update CONSTRAINT so we have to drop the table and
# recreate it.
# The script also rename the new CONSTRAINT with a name that match SQLAlechemy constraint
# naming convention


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
    CREATE TABLE user_workspace_temporary_migration_process (
      user_id INTEGER NOT NULL,
      workspace_id INTEGER NOT NULL,
      role INTEGER NOT NULL,
      email_notification_type VARCHAR(10) DEFAULT 'SUMMARY' NOT NULL,
      CONSTRAINT pk_user_workspace__no_duplicate PRIMARY KEY (user_id, workspace_id),
      CONSTRAINT fk_user_workspace_user_id_users__no_duplicate FOREIGN KEY(user_id) REFERENCES users (user_id),
      CONSTRAINT fk_user_workspace_workspace_id_workspaces__no_duplicate FOREIGN KEY(workspace_id) REFERENCES workspaces (workspace_id),
      CONSTRAINT emailnotificationtype__no_duplicate CHECK (email_notification_type IN ('INDIVIDUAL', 'NONE', 'SUMMARY'))
    );
    """
    )
    op.execute(
        "INSERT INTO user_workspace_temporary_migration_process SELECT * FROM user_workspace;"
    )
    op.execute("DROP TABLE user_workspace;")
    op.execute(
        """
    CREATE TABLE user_workspace (
      user_id INTEGER NOT NULL,
      workspace_id INTEGER NOT NULL,
      role INTEGER NOT NULL,
      email_notification_type VARCHAR(10) DEFAULT 'DAILY' NOT NULL,
      CONSTRAINT pk_user_workspace PRIMARY KEY (user_id, workspace_id),
      CONSTRAINT fk_user_workspace_user_id_users FOREIGN KEY(user_id) REFERENCES users (user_id),
      CONSTRAINT fk_user_workspace_workspace_id_workspaces FOREIGN KEY(workspace_id) REFERENCES workspaces (workspace_id),
      CONSTRAINT ck_user_workspace_emailnotificationtype CHECK (email_notification_type IN ('INDIVIDUAL', 'WEEKLY', 'DAILY', 'HOURLY', 'NONE'))
    );
    """
    )
    op.execute(
        """
    INSERT INTO user_workspace SELECT
      user_id,
      workspace_id,
      role,
      CASE
        WHEN email_notification_type = 'SUMMARY' THEN 'DAILY'
        ELSE email_notification_type
      END AS email_notification_type
    FROM user_workspace_temporary_migration_process;
    """
    )
    op.execute("DROP TABLE user_workspace_temporary_migration_process;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
    CREATE TABLE user_workspace_temporary_migration_process (
      user_id INTEGER NOT NULL,
      workspace_id INTEGER NOT NULL,
      role INTEGER NOT NULL,
      email_notification_type VARCHAR(10) DEFAULT 'DAILY' NOT NULL,
      CONSTRAINT pk_user_workspace__no_duplicate PRIMARY KEY (user_id, workspace_id),
      CONSTRAINT fk_user_workspace_user_id_users__no_duplicate FOREIGN KEY(user_id) REFERENCES users (user_id),
      CONSTRAINT fk_user_workspace_workspace_id_workspaces__no_duplicate FOREIGN KEY(workspace_id) REFERENCES workspaces (workspace_id),
      CONSTRAINT ck_user_workspace_emailnotificationtype__no_duplicate CHECK (email_notification_type IN ('INDIVIDUAL', 'WEEKLY', 'DAILY', 'HOURLY', 'NONE'))
    );
    """
    )
    op.execute(
        "INSERT INTO user_workspace_temporary_migration_process SELECT * FROM user_workspace;"
    )
    op.execute("DROP TABLE user_workspace;")
    op.execute(
        """
    CREATE TABLE user_workspace (
      user_id INTEGER NOT NULL,
      workspace_id INTEGER NOT NULL,
      role INTEGER NOT NULL,
      email_notification_type VARCHAR(10) DEFAULT 'SUMMARY' NOT NULL,
      CONSTRAINT pk_user_workspace PRIMARY KEY (user_id, workspace_id),
      CONSTRAINT fk_user_workspace_user_id_users FOREIGN KEY(user_id) REFERENCES users (user_id),
      CONSTRAINT fk_user_workspace_workspace_id_workspaces FOREIGN KEY(workspace_id) REFERENCES workspaces (workspace_id),
      CONSTRAINT ck_user_workspace_emailnotificationtype CHECK (email_notification_type IN ('INDIVIDUAL', 'NONE', 'SUMMARY'))
    );
    """
    )
    op.execute(
        """
    INSERT INTO user_workspace SELECT
      user_id,
      workspace_id,
      role,
      CASE
        WHEN email_notification_type = 'DAILY' THEN 'SUMMARY'
        WHEN email_notification_type = 'HOURLY' THEN 'SUMMARY'
        WHEN email_notification_type = 'WEEKLY' THEN 'SUMMARY'
        ELSE email_notification_type
      END AS email_notification_type
    FROM user_workspace_temporary_migration_process;
    """
    )
    op.execute("DROP TABLE user_workspace_temporary_migration_process;")
    # ### end Alembic commands ###
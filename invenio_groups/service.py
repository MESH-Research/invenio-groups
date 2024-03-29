# -*- coding: utf-8 -*-
#
# This file is part of the invenio-groups package.
# Copyright (C) 2023, MESH Research.
#
# invenio-groups is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see
# LICENSE file for more details.

from invenio_accounts.models import Role, User
from invenio_accounts.proxies import current_accounts
from invenio_records_resources.services.records.service import RecordService
from typing import Optional, Union

from .utils import logger


class GroupsMetadataService(RecordService):
    """Service for managing group metadata records."""

    def __init__(self, config: dict = {}, **kwargs):
        """Constructor."""
        super().__init__(config=config, **kwargs)


class GroupCollectionsService(RecordService):
    """Service for managing group collections."""

    def __init__(self, config: dict = {}, **kwargs):
        """Constructor."""
        super().__init__(config=config, **kwargs)


class GroupRolesService:
    """Service for managing group roles."""

    def __init__(self, app, *args, **kwargs):
        self.logger = logger

    def get_current_members_of_group(self, group_name: str) -> list:
        """fetch a list of the users assigned the given group role"""
        my_group_role = current_accounts.datastore.find_role(group_name)
        return [user for user in my_group_role.users]

    def get_current_user_roles(self, user: Union[str, User]) -> list:
        """ """
        if isinstance(user, str):
            user = current_accounts.datastore.find_user(email=user)
        if user is None:
            raise RuntimeError(f'User "{user}" not found.')
        return user.roles

    def find_or_create_group(
        self, group_name: str, **kwargs
    ) -> Optional[Role]:
        """Search for a group with a given name and create it if it
        doesn't exist."""
        my_group_role = current_accounts.datastore.find_or_create_role(
            name=group_name, **kwargs
        )
        # FIXME: Is this right?
        current_accounts.datastore.commit()
        if my_group_role is not None:
            self.logger.debug(
                f'Role for group "{group_name}" found or created.'
            )
        else:
            raise RuntimeError(
                f'Role for group "{group_name}" not found or created.'
            )
        return my_group_role

    def create_new_group(self, group_name: str, **kwargs) -> Optional[Role]:
        """Create a new group with the given name (and optional parameters)."""
        my_group_role = current_accounts.datastore.create_role(
            name=group_name, **kwargs
        )
        # FIXME: Is this right?
        current_accounts.datastore.commit()
        if my_group_role is not None:
            self.logger.info(f'Role "{group_name}" created successfully.')
        else:
            raise RuntimeError(f'Role "{group_name}" not created.')
        return my_group_role

    def delete_group(self, group_name: str, **kwargs) -> bool:
        """Delete a group role with the given name."""
        my_group_role = current_accounts.datastore.find_role(group_name)
        # FIXME: Is this right?
        current_accounts.datastore.commit()
        if my_group_role is None:
            raise RuntimeError(f'Role "{group_name}" not found.')
        else:
            deleted_group = current_accounts.datastore.delete(my_group_role)
            if deleted_group is False:
                raise RuntimeError(f'Role "{group_name}" not deleted.')
            else:
                self.logger.info(f'Role "{group_name}" deleted successfully.')
        return deleted_group

    def add_user_to_group(self, group_name: str, user: User, **kwargs) -> bool:
        """Add a user to a group."""
        self.logger.debug(f"got group name {group_name}")
        user_added = current_accounts.datastore.add_role_to_user(
            user, group_name
        )
        # FIXME: Is this right?
        current_accounts.datastore.commit()
        if user_added is False:
            raise RuntimeError("Cannot add user to group role.")
        else:
            user_str = user.email if isinstance(user, User) else user
            self.logger.info(
                f'Role "{group_name}" added to user"{user_str}" successfully.'
            )
        return user_added

    def find_group(self, group_name: str) -> Optional[Role]:
        """Find a group role with the given name."""
        my_group_role = current_accounts.datastore.find_role(group_name)
        if my_group_role is None:
            raise RuntimeError(f'Role "{group_name}" not found.')
        else:
            self.logger.debug(f'Role "{group_name}" found successfully.')
        return my_group_role

    def remove_user_from_group(
        self, group_name: Union[str, Role], user: Union[str, User], **kwargs
    ) -> bool:
        """Remove a group role from a user.

        args:
            group_name: The name of the group to remove the user from,
                or the Role object for the group.
            user: The user object to remove from the group, or the user's email
                address.
        """
        removed_user = current_accounts.datastore.remove_role_from_user(
            user, group_name
        )
        # FIXME: Is this right?
        current_accounts.datastore.commit()
        if removed_user is False:
            raise RuntimeError("Cannot remove group role from user.")
        else:
            self.logger.info(
                f'Role "{group_name}" removed from user "{user.email}"'
                "successfully."
            )
        return removed_user

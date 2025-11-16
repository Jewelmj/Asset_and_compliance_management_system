class PermissionService:
    """
    Handles user permissions based on their role.
    Keeps permission logic separate from the user data model.
    """

    PERMISSIONS = {
        "Admin": [
            "manage_users",
            "manage_assets",
            "view_documents",
            "edit_documents",
            "manage_jobsites",
            "generate_qr",
        ],
        "Manager": [
            "assign_assets",
            "assign_people",
            "move_assets",
            "view_documents",
            "manage_jobsites",
        ],
        "Worker": [
            "scan_qr",
            "check_asset",
            "move_asset",
            "view_assigned_assets",
            "view_jobsite",
        ]
    }

    def get_permissions(self, user):
        """Return the list of permissions for the user’s role."""
        return PermissionService.PERMISSIONS.get(user.role, [])
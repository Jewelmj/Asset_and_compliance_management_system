class AssetAssigner:
    """
    Handles assignment of an asset to a user, jobsite, or vehicle.
    """

    def __init__(self, history):
        self.history = history

        self.user = None
        self.jobsite = None
        self.vehicle = None

    def assign_to_user(self, user):
        self.user = user
        self.jobsite = None
        self.vehicle = None
        self.history.log(f"Assigned to user {user.name}")

    def assign_to_jobsite(self, jobsite):
        self.jobsite = jobsite
        self.user = None
        self.vehicle = None
        self.history.log(f"Assigned to jobsite {jobsite.name}")

    def assign_to_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.user = None
        self.jobsite = None
        self.history.log(f"Assigned to vehicle {vehicle.vehicle_id}")

    def current_location(self):
        if self.user:
            return f"User: {self.user.name}"
        if self.jobsite:
            return f"Jobsite: {self.jobsite.name}"
        if self.vehicle:
            return f"Vehicle: {self.vehicle.vehicle_id}"
        return "Unassigned"
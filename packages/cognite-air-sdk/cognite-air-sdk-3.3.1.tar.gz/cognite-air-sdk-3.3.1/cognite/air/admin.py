from cognite.air._spaces_api import SpacesAPI
from cognite.client import CogniteClient


class AIRAdmin:
    """AIRAdmin client to create, edit, and delete spaces and groups.

    Args:
        client (CogniteClient): Cognite client
        project (str): The project to which groups and spaces shall be added
        staging (bool): If groups and spaces should be added to staging or production (True is default)
    """

    def __init__(self, client: CogniteClient, project: str, staging: bool = True):
        self.client = client
        self.project = project
        self.staging = staging
        self.spaces = SpacesAPI(self.client, self.project, self.staging)

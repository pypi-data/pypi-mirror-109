import os
import logging
import datetime

import requests


# Get an instance of a logger
logger = logging.getLogger(__name__)


class Merit:
    """Handler for all Merit API calls."""


    def __init__(self, app_id, app_secret, production=True):

        self.app_id = app_id
        self.app_secret = app_secret

        if production:
            self.domain = "https://api.merits.com"
        else:
            self.domain = "https://sandbox-api.merits.com"


    def authenticate(self):
        """Get or refresh org_access_token."""

        if not self.org_access_token:
            self.get_org_access_token()
        if (self.authenticated_at < (datetime.datetime.now() - datetime.timedelta(seconds=self.auth_timeout))):
            self.get_org_access_token()


    def get_api(self, path, params=None):
        """Unified endpoint for all GET calls out to API."""

        # authenticate
        self.authenticate()

        # call api
        url = self.domain + path
        logger.info(url)
        headers = {"Authorization": f"Bearer {self.org_access_token}"}
        return requests.get(url, headers=headers, params=params)


    def post_api(self, path, data=None):
        """Unified endpoint for all POST calls out to API."""

        # authenticate
        self.authenticate()

        # call api
        url = self.domain + path
        logger.info(url)
        if "uuidTranslation" in path:
            return requests.post(url, auth=(self.app_id, self.app_secret))
        headers = {"Authorization": f"Bearer {self.org_access_token}"}
        return requests.post(url, json=data, headers=headers)


    def link_with_merit(self, success_url: str, failure_url: str) -> str:
        """Initiate process to link Merit Org to this app."""

        url = self.domain + "/v2/request_linkapp_url"

        data = {
            "requestedPermissions": [{ "permissionType": "CanManageOrg" }],
            "successUrl": success_url,
            "failureUrl": failure_url,
            "state": f"initiated-from-merit-registration-{datetime.datetime.now():%d-%m-%Y-%H-%M-%S}",
        }

        response = requests.post(url, json=data, auth=(self.app_id, self.app_secret))

        #{
        #  "request_linkapp_url": "https://app.merits.com/link-app/?token=5aa5a3992bfa4e0006c47cdf"
        #  "expiration": "2019-01-31T18:48:51.000Z"
        #}

        if response.status_code == 200:
            url = response.json().get("request_linkapp_url")
            if url:
                return url
        logger.error(response.text)
        return None


    def get_org_id_from_token(self, org_id_token):
        """Exchange org_id_token from link_with_merit flow for permanent org_id."""

        url =  self.domain + f"/v2/org_id?org_id_token={org_id_token}"

        response = requests.get(url, auth=(self.app_id, self.app_secret))

        if response.status_code == 200:
            org_id = response.json().get("orgId")
            if org_id:
                self.org_id = org_id
                return org_id
        logger.error(response.text)
        return None




    class Org:
        """Merit Organizations

        :param org_id: ID for the Merit Organization

        :returns: Org object
        """


        def __init__(self, org_id):
            self.org_id = org_id
            self.auth_timeout = 3600 # seconds
            self.authenticated_at = None
            self.org_access_token = self.get_org_access_token()


        def get_org_access_token(self):
            """Call Merit API for Org Access Token."""

            access_url = self.domain + f"/v2/orgs/{self.org_id}/access"
            logger.info(access_url)
            response = requests.post(access_url, auth=(self.app_id, self.app_secret))

            if response.status_code == 200:
                self.authenticated_at = datetime.datetime.now()
                self.org_access_token = response.json().get("orgAccessToken")
                return self.org_access_token
            else:
                logger.error(response.text)
                return None


        def get_org_info(self):
            """Get Merit information about Organization.

            :return: {
                    "id": "5b442b02b85f223fffe9e851",
                    "title": "Millbrae CERT",
                    "description": "This is an example Org",
                    "website": "http://www.example.com",
                    "address": "1001 Broadway, Millbrae, CA, USA",
                    "phone": "+1 650-296-9525",
                    "email": "admin@example.com",
                    "logoUrl": "https://images.sig.ma/5c4f598f774d570006465f9e?rect=0,0,150,150"
                }
            """

            url = self.domain + f"/v2/orgs/{self.org_id}"
            headers = {"Authorization": f"Bearer {self.org_access_token}"}
            response = requests.get(url, headers=headers)

            {
                "id": "5b442b02b85f223fffe9e851",
                "title": "Millbrae CERT",
                "description": "This is an example Org",
                "website": "http://www.example.com",
                "address": "1001 Broadway, Millbrae, CA, USA",
                "phone": "+1 650-296-9525",
                "email": "admin@example.com",
                "logoUrl": "https://images.sig.ma/5c4f598f774d570006465f9e?rect=0,0,150,150"
            }

            if response.status_code == 200:
                data = response.json()
                if "id" in data:
                    return data
            logger.error(response.text)
            return None


    def get_field(self, field_id):
        """Return details of specified Field."""

        response = self.get_api(f"/v2/fields/{field_id}")

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(response.text)
            return None


    def get_all_org_merit_templates(self):
        """Return a list of all MeritTemplates owned by the Org."""

        response = self.get_api(f"/v2/orgs/{self.org_id}/merittemplates?limit=100")

        if response.status_code == 200:
            return response.json().get("merittemplates")
        else:
            logger.error(response.text)
            return []


    def get_org_merit_template_choices(self, include_none=True):
        """Return a formatted tuple of form choices of available MeritTemplates."""

        choices = []
        if include_none:
            choices.append((None, "-----"))
        for template in self.get_all_org_merit_templates():
            choices.append((template.get("id"), template.get("title")))
        return choices


    def get_merit_template(self, merit_template_id):
        """Return details of specified MeritTemplate."""

        response = self.get_api(f"/v2/merittemplates/{merit_template_id}")

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(response.text)
            return None


    def get_template_field_choices(self, template_id):
        """Return list of fields used in specified Template."""

        return [self.get_field(field.get("fieldId")) for field in self.get_merit_template(template_id).get("enabledFieldSettings")]


    def get_all_merits(self, merittemplate_id=None, merit_status=None):
        """Get all Org merits by specifications."""

        # valid merit_status values are:
        # Accepted, Forfeited, Pending, Rejected,
        # Reported, Revoked, Transferred, TransferredUnverified,
        # Unapproved, UnapprovedUnverified, Unverified

        params = {
            "merittemplate_id": merittemplate_id,
            "merit_status": merit_status,
            "limit": 100,
        }

        response = self.get_api(f"/v2/orgs/{self.org_id}/merits", params)

        if response.status_code == 200:
            print(response.json())
        else:
            logger.error(response.text)
            return None


    def get_template_pending_merits(self, merittemplate_id):
        """Return all proposed merits from site MeritTemplate."""

        return self.get_all_org_merits(merittemplate_id, "Unapproved")


    def propose_merit(self, data):
        """Propose a merit as specified."""

        response = self.post_api("/v2/merits/propose", data)

        if response.status_code == 200:
            id = response.json().get("id")
            if id:
                return id
            return None
        else:
            logger.error(response.text)
            return None


    def send_merit(self, data):
        """Send merit as specified."""

        response = self.post_api("/v2/merits/send", data)

        if response.status_code == 200:
            id = response.json().get("id")
            if id:
                return id
            return None
        else:
            logger.error(response.text)
            return None


    def edit_merit(self, merit_id, data):
        """Edit specified merit."""

        response = self.post_api(f"/v2/merits/{merit_id}", data)

        if response.status_code == 200:
            return True
        else:
            logger.error(response.text)
            return False


    def revoke_merit(self, merit_id, reason):
        """Revoke specified merit."""

        response = self.post_api(f"/v2/merits/{merit_id}/revoke", {"revocationReason": reason})

        if response.status_code == 200:
            return True
        else:
            logger.error(response.text)
            return False


    def uuid_translation(self, merit_id, email):

        response = self.post_api(f"/v2/uuidTranslation/merit/{merit_id}/email/{email}")

        if response.status_code == 200:
            return response.json().get("translationUrl")
        else:
            logger.error(response.text)
            return None


    def update_email(self, merit_id, email):
        """Transfer merit to new email address."""

        response = self.post_api(f"/v2/merits/{merit_id}/transfer", {"newRecipientEmail": email})

        if response.status_code == 200:
            new_merit = response.json().get("newMerit")
            if new_merit:
                return new_merit.get("id")
            return None
        else:
            logger.error(response.text)
            return None

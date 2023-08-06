import json
from datetime import datetime, timedelta, date
from time import sleep
from urllib.parse import urljoin

from requests import Session


class AnalyzeMissingCredentialsException(Exception):
    pass


class AnalyzeAuthException(Exception):
    pass


class AnalyzeClient:
    url_prefix = None

    __DEBUG = True
    __USERNAME = None
    __PASSWORD = None
    __JWT = None

    def __init__(self, **kwargs):
        self.url_prefix = "https://g3-api.primer.ai/api/v1"

        self.__DEBUG = kwargs.get("debug", False)
        self.__USERNAME = kwargs.get("username")
        self.__PASSWORD = kwargs.get("password")
        self.__JWT = kwargs.get("JWT", None)

        if not self.__JWT and not self.__USERNAME and not self.__PASSWORD:
            raise AnalyzeMissingCredentialsException(
                "Missing authentication mechanism, you need to provide either an access_token or username and password combination"
            )

        if self.__USERNAME and not self.__PASSWORD:
            raise AnalyzeMissingCredentialsException(
                "Password is required for authentication"
            )

        if self.__PASSWORD and not self.__USERNAME:
            raise AnalyzeMissingCredentialsException(
                "Username is required for authentication"
            )

        if not self.__JWT:
            self.__JWT = self.__authenticate(self.__USERNAME, self.__PASSWORD)

    def __log(self, msg):
        if self.__DEBUG:
            print(msg)

    def __authenticate(self, username, password):
        """Authenticate with User Management Service

        Multiple attempts will be made to login, and if successful a JWT token is returned.
        Otherwise, an exception is returned
        """

        sess = Session()
        sess.headers.update(
            {
                "Accept": "application/json",
                "content-type": "application/json",
            }
        )
        data = {"password": password, "username": username}

        self.__log("Attempting to authenticate")
        for x in range(3):
            try:
                r = sess.request(
                    method="POST",
                    url="https://sso.primer.ai/api/v1/auth/login",
                    data=json.dumps(data),
                )

                return r.json()["access_token"]
            except Exception as e:
                self.__log(f"Issue during authentication: {e}")
                sleep(x)
                pass

        raise Exception("Could not authenticate with Analyze")

    def __analyze_request(self, **kwargs):
        sess = Session()
        sess.headers.update(
            {
                "Authorization": f"JWT {self.__JWT}",
                "Accept": "application/json",
            }
        )

        if kwargs.get("method", None) == "POST":
            sess.headers.update({"Content-Type": "application/json"})

        url = self.url_prefix + "/" + kwargs.pop("url")
        resp = sess.request(url=url, **kwargs)

        # Attempt refresh of JWT token if a 401
        if resp.status_code == 401:
            if not self.__USERNAME and not self.__PASSWORD:
                raise AnalyzeAuthException
            else:
                # After refreshing, try request again
                self.__JWT = self.__authenticate(self.__USERNAME, self.__PASSWORD)
                resp = sess.request(**kwargs)
                # if request is still a 401, nothing we can do but raise it
                if resp.status_code == 401:
                    raise AnalyzeAuthException
        else:
            return resp

    def __get(self, url, params={}):
        return self.__analyze_request(method="GET", url=url, params=params)

    def __post(self, url, data=None):
        return self.__analyze_request(method="POST", url=url, data=data)

    def get_query(self, query_terms, days=1, datetime_from=None, datetime_to=None):
        """
        Returns the query_id of the input terms

        Args:
            query_terms (str): A query string
            days (int, optional): The number of days back to search. Defaults to 1.
            datetime_from ([datetime], optional): A specific date to search from, use instead of the days parameter. Defaults to None.
            datetime_to ([datetime], optional): A specific date to search to, use instead of the days parameter. Defaults to None.

        Returns:
            obj: The JSON response
        """

        if datetime_from is None:
            datetime_from = datetime.today() - timedelta(days=days)

        data = {"content": query_terms, "start_date": datetime_from.isoformat()}

        if datetime_to is not None:
            data["end_date"] = datetime_to.isoformat()

        self.__log(f"About to POST for query: {data}")

        for x in range(10):
            try:
                r = self.__analyze_request(
                    method="POST",
                    url="/query/queries/",
                    data=json.dumps(data),
                )

                return r.json()
            except Exception as e:
                self.__log(f"Problem getting query: {e}")
                sleep(x)
        return None

    def get_documents(
        self,
        query_id,
        page=0,
        order_by=None,
        include_full_content=True,
        order="desc",
        page_size=25,
    ):
        """Get documents for a query

        Args:
            query_id (str): The query id to use for getting documents
            page (int, optional): A parameter to use in paginating a request. Defaults to 0.
            order_by (str, optional): A parameter for ordering documents by an attribute. Defaults to None.
            include_full_content (bool, optional): Whether to, if it is availible, to include the full document content. Defaults to True.
            order (str, optional): How to order documents ("asc" or "desc"). Defaults to "desc".
            page_size (int, optional): Can be used in paginating. Defaults to 25.

        Returns:
            obj: The JSON response
        """
        response = self.__get(
            f"query/queries/{query_id}/documents",
            params={
                "page": page,
                "order_by": order_by,
                "include_full_content": include_full_content,
                "order": order,
                "page_size": page_size,
            },
        )

        return response.json()

    def get_events(self, query_id, scroll_id=None, page=0, page_size=25):
        """Return events for a given query id

        Args:
            query_id (str): The query id to use for searching for events
            scroll_id (str, optional): Used in pagination, will be returned in the response and should be used in subsequent calls to this method. Defaults to None.
            page (int, optional): Used in conjunction with scroll_id. Defaults to 0.
            page_size (int, optional): Use for pagination. Defaults to 25.

        Returns:
            obj: The JSON response
        """

        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"/query/queries/{query_id}/news", data=json.dumps(body)
                    )
                else:
                    r = self.__get(
                        f"/query/queries/{query_id}/news",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)
        return None

    def get_event_data(self, query_id, event_id):
        """Get details about a specific event

        Args:
            query_id (str): The query id
            event_id (str): The event id

        Returns:
            obj: The JSON response
        """
        for x in range(10):
            try:
                r = self.__analyze_request(
                    method="GET",
                    url=f"/query/queries/{query_id}/event/{event_id}",
                )
                return r.json()
            except Exception as e:
                self.__log(f"Error getting event data: {e}")
                sleep(x)
        return {}

    def get_event_documents(
        self, query_id, event_id, scroll_id=None, page=0, page_size=25
    ):
        """Similar to get_documents, but will get documents for a specific event.

        Args:
            query_id (str): The query id
            event_id (str): The event id
            scroll_id (str, optional): Used in pagination, will be returned in the response and should be used in subsequent calls to this method. Defaults to None.
            page (int, optional): Used in conjunction with scroll_id. Defaults to 0.
            page_size (int, optional): Use for pagination. Defaults to 25.

        Returns:
            obj: The JSON response
        """
        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"query/queries/{query_id}/event/{event_id}/documents",
                        data=json.dumps(body),
                    )
                else:
                    r = self.__get(
                        f"query/queries/{query_id}/event/{event_id}/documents",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)

        return None

    def get_event_quotes(
        self, query_id, event_id, scroll_id=None, page_size=25, page=0
    ):
        """Returns quotes from the quotes endpoint about a specific event.

        Args:
            query_id (str): The query id
            event_id (str): The event id
            scroll_id (str, optional): Used in pagination, will be returned in the response and should be used in subsequent calls to this method. Defaults to None.
            page (int, optional): Used in conjunction with scroll_id. Defaults to 0.
            page_size (int, optional): Use for pagination. Defaults to 25.

        Returns:
            obj: The JSON response
        """

        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"query/queries/{query_id}/event/{event_id}/quotes",
                        data=json.dumps(body),
                    )
                else:
                    r = self.__get(
                        f"query/queries/{query_id}/event/{event_id}/quotes",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)

        return None

    def get_event_numbers(
        self, query_id, event_id, scroll_id=None, page_size=25, page=0
    ):
        """Returns numbers from the numbers about a specific event.

        Args:
            query_id (str): The query id
            event_id (str): The event id
            scroll_id (str, optional): Used in pagination, will be returned in the response and should be used in subsequent calls to this method. Defaults to None.
            page (int, optional): Used in conjunction with scroll_id. Defaults to 0.
            page_size (int, optional): Use for pagination. Defaults to 25.

        Returns:
            obj: The JSON response
        """
        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"query/queries/{query_id}/event/{event_id}/numbers",
                        data=json.dumps(body),
                    )
                else:
                    r = self.__get(
                        f"query/queries/{query_id}/event/{event_id}/numbers",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)

    def get_event_people(
        self, query_id, event_id, scroll_id=None, page_size=25, page=0
    ):
        """Returns people from the people endpoint about a specific event.

        Args:
            query_id ([type]): [description]
            event_id ([type]): [description]
            scroll_id ([type], optional): [description]. Defaults to None.
            page_size (int, optional): [description]. Defaults to 25.
            page (int, optional): [description]. Defaults to 0.

        Returns:
            obj: The JSON response
        """
        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"query/queries/{query_id}/event/{event_id}/people",
                        data=json.dumps(body),
                    )
                else:
                    r = self.__get(
                        f"query/queries/{query_id}/event/{event_id}/people",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)

    def get_event_organizations(
        self, query_id, event_id, scroll_id=None, page_size=25, page=0
    ):
        """Returns organizations from the organizations endpoint about a specific event.

        Args:
            query_id ([type]): [description]
            event_id ([type]): [description]
            scroll_id ([type], optional): [description]. Defaults to None.
            page_size (int, optional): [description]. Defaults to 25.
            page (int, optional): [description]. Defaults to 0.

        Returns:
            obj: The JSON response
        """
        body = {
            "order": "desc",
            "page_size": page_size,
        }

        for x in range(5):
            try:
                if not scroll_id:
                    r = self.__post(
                        f"query/queries/{query_id}/events/{event_id}/organizations",
                        data=json.dumps(body),
                    )
                else:
                    r = self.__get(
                        f"query/queries/{query_id}/events/{event_id}/organizations",
                        params={
                            "scroll_id": scroll_id,
                            "page": page,
                            "page_size": page_size,
                        },
                    )
                return r.json()
            except:
                sleep(x)

    def get_document_detail(self, query_id, document_id):
        """Pulls documents details from the doc details endpoint.

        Args:
            query_id (str): The query id
            document_id (str): The document id

        Returns:
            obj: The JSON response
        """
        response = self.__get(f"query/queries/{query_id}/document/{document_id}/detail")
        return response.json()

    def refresh_query(self, query_id):
        """Refreshes the specified query. This is only required for queries that have a time window
        associated with them (i.e. events from the past three days)

        Args:
            query_id (str): The query id

        Returns:
            obj: The JSON response
        """
        url_suffix = f"query/queries/{query_id}/refresh"
        url = urljoin(self.prefix_url, url_suffix)
        self.__log(f"full url: {url}")
        response = self.__post(url_suffix)
        self.__log(f"got query_id: {query_id}")
        return response.status_code == 200

    def get_entity_ids(self, search_term, size=10):
        """Return entity IDs for a given query

        Args:
            search_term (str): The name of an entity to query
            size (int, optional): The size of the result set returned. Defaults to 10.

        Returns:
            obj: The JSON response
        """
        # For whatever reason, autocomplete seems to fail to return sometimes,
        # So try 10 times before
        for x in range(10):
            try:
                r = self.__analyze_request(
                    method="GET",
                    url=f"/query/autocomplete?search={search_term}&size={size}",
                )
                ids = []
                for e in r.json():
                    matches = e.get("matches", [])
                    for ent in matches:
                        ids.append(
                            (ent["entity_id"], ent["representative_name"], r.json())
                        )
                return ids
            except Exception as e:
                self.__log(f"Exception getting entity id: {e}")
                sleep(x)
        return []

    def entity_format(self, entity_id, entity_name):
        return f"organization.entity_id:{entity_id}:[|{entity_name}|]"

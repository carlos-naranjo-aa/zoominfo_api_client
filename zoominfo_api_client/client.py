"""ZoomInfo API client using requests.

This client supports authentication and enterprise standard search endpoints
for contacts and companies.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests


class ZoomInfoClient:
    """Client for interacting with the ZoomInfo API."""

    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = "https://api.zoominfo.com",
        session: Optional[requests.Session] = None,
    ) -> None:
        """Initialize the client.

        Parameters
        ----------
        username : str
            ZoomInfo API username.
        password : str
            ZoomInfo API password.
        base_url : str, optional
            Base URL for the ZoomInfo API. Defaults to ``"https://api.zoominfo.com"``.
        session : Optional[requests.Session], optional
            Pre-configured session to use for requests. If ``None``, a new
            :class:`requests.Session` is created.
        """
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.token: Optional[str] = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def authenticate(self) -> str:
        """Authenticate and store a JWT token.

        Returns
        -------
        str
            JWT token returned by the API.

        Raises
        ------
        requests.HTTPError
            If the API request fails.
        ValueError
            If the JWT token is missing from the response.
        """
        url = f"{self.base_url}/authenticate"
        response = self.session.post(url, json={"username": self.username, "password": self.password})
        response.raise_for_status()
        data = response.json()
        self.token = data.get("jwt")
        if not self.token:
            raise ValueError("JWT token not found in authentication response")
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        return self.token

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform an authenticated POST request.

        Parameters
        ----------
        path : str
            API path appended to ``base_url`` (e.g., ``"/search/contact"``).
        payload : Dict[str, Any]
            JSON-serializable data to include in the request body.

        Returns
        -------
        Dict[str, Any]
            Parsed JSON response from the API.
        """
        if not self.token:
            self.authenticate()
        url = f"{self.base_url}{path}"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Search endpoints
    # ------------------------------------------------------------------
    def search_contacts(
        self,
        person_id: Optional[str] = None,
        email_address: Optional[str] = None,
        hashed_email: Optional[str] = None,
        full_name: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_initial: Optional[str] = None,
        last_name: Optional[str] = None,
        job_title: Optional[str] = None,
        exclude_job_title: Optional[str] = None,
        management_level: Optional[str] = None,
        exclude_management_level: Optional[str] = None,
        board_member: Optional[str] = None,
        exclude_partial_profiles: Optional[bool] = None,
        executives_only: Optional[bool] = None,
        required_fields: Optional[str] = None,
        contact_accuracy_score_min: Optional[str] = None,
        contact_accuracy_score_max: Optional[str] = None,
        job_function: Optional[str] = None,
        last_updated_in_months: Optional[int] = None,
        has_been_notified: Optional[str] = None,
        company_past_or_present: Optional[str] = None,
        school: Optional[str] = None,
        degree: Optional[str] = None,
        location_company_id: Optional[List[str]] = None,
        last_updated_date_after: Optional[str] = None,
        valid_date_after: Optional[str] = None,
        phone: Optional[List[str]] = None,
        position_start_date_min: Optional[str] = None,
        position_start_date_max: Optional[str] = None,
        supplemental_email: Optional[List[str]] = None,
        web_references: Optional[List[str]] = None,
        buying_group: Optional[List[str]] = None,
        tech_skills: Optional[List[str]] = None,
        years_of_experience: Optional[str] = None,
        department: Optional[str] = None,
        exact_job_title: Optional[str] = None,
        company_ticker: Optional[List[str]] = None,
        company_description: Optional[str] = None,
        company_type: Optional[str] = None,
        address: Optional[str] = None,
        street: Optional[str] = None,
        zip_code: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        continent: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_website: Optional[str] = None,
        parent_id: Optional[str] = None,
        ultimate_parent_id: Optional[str] = None,
        zip_code_radius_miles: Optional[str] = None,
        hash_tag_string: Optional[str] = None,
        tech_attribute_tag_list: Optional[str] = None,
        sub_unit_types: Optional[str] = None,
        primary_industries_only: Optional[bool] = None,
        industry_codes: Optional[str] = None,
        industry_keywords: Optional[str] = None,
        sic_codes: Optional[str] = None,
        naics_codes: Optional[str] = None,
        revenue: Optional[str] = None,
        revenue_min: Optional[int] = None,
        revenue_max: Optional[int] = None,
        employee_range_min: Optional[str] = None,
        employee_range_max: Optional[str] = None,
        employee_count: Optional[str] = None,
        company_ranking: Optional[str] = None,
        metro_region: Optional[str] = None,
        location_search_type: Optional[str] = None,
        funding_amount_min: Optional[int] = None,
        funding_amount_max: Optional[int] = None,
        funding_start_date: Optional[str] = None,
        funding_end_date: Optional[str] = None,
        zoominfo_contacts_min: Optional[str] = None,
        zoominfo_contacts_max: Optional[str] = None,
        excluded_regions: Optional[str] = None,
        company_structure_included_sub_unit_types: Optional[str] = None,
        one_year_employee_growth_rate_min: Optional[str] = None,
        one_year_employee_growth_rate_max: Optional[str] = None,
        two_year_employee_growth_rate_min: Optional[str] = None,
        two_year_employee_growth_rate_max: Optional[str] = None,
        engagement_start_date: Optional[str] = None,
        engagement_end_date: Optional[str] = None,
        engagement_type: Optional[List[str]] = None,
        rpp: Optional[int] = None,
        page: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **extra_filters: Any,
    ) -> Dict[str, Any]:
        """Search for contacts using detailed filters.

        Parameters
        ----------
        person_id : Optional[str]
            Unique ZoomInfo identifier for the contact.
        email_address : Optional[str]
            Work email address for the contact.
        hashed_email : Optional[str]
            Hashed email value for the contact.
        full_name : Optional[str]
            Contact full name.
        first_name : Optional[str]
            Contact first name.
        middle_initial : Optional[str]
            Contact middle initial.
        last_name : Optional[str]
            Contact last name.
        job_title : Optional[str]
            Contact job title at current company.
        exclude_job_title : Optional[str]
            Comma-separated list of job titles to exclude.
        management_level : Optional[str]
            Contact management level.
        exclude_management_level : Optional[str]
            Comma-separated list of management levels to exclude.
        board_member : Optional[str]
            Include or exclude board members (include, exclude, only).
        exclude_partial_profiles : Optional[bool]
            When true, exclude contacts without an active company.
        executives_only : Optional[bool]
            When true, return only executives.
        required_fields : Optional[str]
            Required fields for each result (e.g., email, phone).
        contact_accuracy_score_min : Optional[str]
            Minimum accuracy score (70-99).
        contact_accuracy_score_max : Optional[str]
            Maximum accuracy score (70-99).
        job_function : Optional[str]
            Contact job function.
        last_updated_in_months : Optional[int]
            Number of months since profile update.
        has_been_notified : Optional[str]
            Filter by notification status (include, exclude, only).
        company_past_or_present : Optional[str]
            Filter by work history (present, past, pastAndPresent).
        school : Optional[str]
            Education school.
        degree : Optional[str]
            Education degree.
        location_company_id : Optional[List[str]]
            List of location company IDs.
        last_updated_date_after : Optional[str]
            Date after which profile was updated.
        valid_date_after : Optional[str]
            Date after which profile was validated.
        phone : Optional[List[str]]
            List of phone numbers.
        position_start_date_min : Optional[str]
            Minimum position start date ``YYYY-MM-DD``.
        position_start_date_max : Optional[str]
            Maximum position start date ``YYYY-MM-DD``.
        supplemental_email : Optional[List[str]]
            Supplemental email addresses.
        web_references : Optional[List[str]]
            Web references for the contact.
        buying_group : Optional[List[str]]
            Buying group IDs.
        tech_skills : Optional[List[str]]
            Technology skills list.
        years_of_experience : Optional[str]
            Years of overall experience.
        department : Optional[str]
            Contact department.
        exact_job_title : Optional[str]
            Exact match job title.
        company_ticker : Optional[List[str]]
            Company stock ticker symbols.
        company_description : Optional[str]
            Words describing the company.
        company_type : Optional[str]
            Company type (e.g., private, public).
        address : Optional[str]
            Company address.
        street : Optional[str]
            Company street.
        zip_code : Optional[str]
            Company zip code.
        state : Optional[str]
            Company state.
        country : Optional[str]
            Company country.
        continent : Optional[str]
            Company continent.
        company_id : Optional[str]
            ZoomInfo company ID (comma-separated for multiple).
        company_name : Optional[str]
            Company name.
        company_website : Optional[str]
            Company domain (comma-separated list allowed).
        parent_id : Optional[str]
            ZoomInfo ID for parent company.
        ultimate_parent_id : Optional[str]
            ZoomInfo ID for ultimate parent company.
        zip_code_radius_miles : Optional[str]
            Radius in miles around ``zip_code``.
        hash_tag_string : Optional[str]
            Company hash tags (comma-separated).
        tech_attribute_tag_list : Optional[str]
            Technology product tags.
        sub_unit_types : Optional[str]
            Company sub unit types.
        primary_industries_only : Optional[bool]
            If true, require results to match primary industries.
        industry_codes : Optional[str]
            Industry codes (comma-separated).
        industry_keywords : Optional[str]
            Industry keywords (supports ``AND``/``OR``).
        sic_codes : Optional[str]
            SIC codes (comma-separated).
        naics_codes : Optional[str]
            NAICS codes (comma-separated).
        revenue : Optional[str]
            Predefined revenue range IDs.
        revenue_min : Optional[int]
            Minimum annual revenue (thousands USD).
        revenue_max : Optional[int]
            Maximum annual revenue (thousands USD).
        employee_range_min : Optional[str]
            Minimum employee count.
        employee_range_max : Optional[str]
            Maximum employee count.
        employee_count : Optional[str]
            Predefined employee count range IDs.
        company_ranking : Optional[str]
            Company ranking IDs (comma-separated).
        metro_region : Optional[str]
            Metro regions (comma-separated).
        location_search_type : Optional[str]
            Location search type.
        funding_amount_min : Optional[int]
            Minimum funding amount (thousands).
        funding_amount_max : Optional[int]
            Maximum funding amount (thousands).
        funding_start_date : Optional[str]
            Funding start date ``YYYY-MM-DD``.
        funding_end_date : Optional[str]
            Funding end date ``YYYY-MM-DD``.
        zoominfo_contacts_min : Optional[str]
            Minimum number of ZoomInfo contacts.
        zoominfo_contacts_max : Optional[str]
            Maximum number of ZoomInfo contacts.
        excluded_regions : Optional[str]
            Regions to exclude.
        company_structure_included_sub_unit_types : Optional[str]
            Company hierarchical structure types to include.
        one_year_employee_growth_rate_min : Optional[str]
            Minimum one-year employee growth rate.
        one_year_employee_growth_rate_max : Optional[str]
            Maximum one-year employee growth rate.
        two_year_employee_growth_rate_min : Optional[str]
            Minimum two-year employee growth rate.
        two_year_employee_growth_rate_max : Optional[str]
            Maximum two-year employee growth rate.
        engagement_start_date : Optional[str]
            Engagement start date ``YYYY-MM-DD``.
        engagement_end_date : Optional[str]
            Engagement end date ``YYYY-MM-DD``.
        engagement_type : Optional[List[str]]
            Engagement types (e.g., email, phone).
        rpp : Optional[int]
            Results per page limit.
        page : Optional[int]
            Page number for pagination.
        sort_by : Optional[str]
            Field name to sort results by.
        sort_order : Optional[str]
            Sort order (``asc`` or ``desc``).
        **extra_filters : Any
            Additional filters passed directly to the API.

        Returns
        -------
        Dict[str, Any]
            Parsed JSON response from the API.
        """

        def to_camel(name: str) -> str:
            parts = name.split("_")
            return parts[0] + "".join(p.capitalize() for p in parts[1:])

        params = {
            to_camel(k): v
            for k, v in locals().items()
            if k not in {"self", "extra_filters"} and v is not None
        }
        params.update(extra_filters)
        return self._post("/search/contact", params)

    def search_companies(
        self,
        marketing_department_budget_min: Optional[int] = None,
        marketing_department_budget_max: Optional[int] = None,
        finance_department_budget_min: Optional[int] = None,
        finance_department_budget_max: Optional[int] = None,
        it_department_budget_min: Optional[int] = None,
        it_department_budget_max: Optional[int] = None,
        hr_department_budget_min: Optional[int] = None,
        hr_department_budget_max: Optional[int] = None,
        certified: Optional[int] = None,
        exclude_defunct_companies: Optional[bool] = None,
        company_ticker: Optional[List[str]] = None,
        company_description: Optional[str] = None,
        company_type: Optional[str] = None,
        address: Optional[str] = None,
        street: Optional[str] = None,
        zip_code: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        continent: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_website: Optional[str] = None,
        parent_id: Optional[str] = None,
        ultimate_parent_id: Optional[str] = None,
        zip_code_radius_miles: Optional[str] = None,
        hash_tag_string: Optional[str] = None,
        tech_attribute_tag_list: Optional[str] = None,
        sub_unit_types: Optional[str] = None,
        primary_industries_only: Optional[bool] = None,
        industry_codes: Optional[str] = None,
        industry_keywords: Optional[str] = None,
        sic_codes: Optional[str] = None,
        naics_codes: Optional[str] = None,
        revenue: Optional[str] = None,
        revenue_min: Optional[int] = None,
        revenue_max: Optional[int] = None,
        employee_range_min: Optional[str] = None,
        employee_range_max: Optional[str] = None,
        employee_count: Optional[str] = None,
        company_ranking: Optional[str] = None,
        metro_region: Optional[str] = None,
        location_search_type: Optional[str] = None,
        funding_amount_min: Optional[int] = None,
        funding_amount_max: Optional[int] = None,
        funding_start_date: Optional[str] = None,
        funding_end_date: Optional[str] = None,
        zoominfo_contacts_min: Optional[str] = None,
        zoominfo_contacts_max: Optional[str] = None,
        excluded_regions: Optional[str] = None,
        company_structure_included_sub_unit_types: Optional[str] = None,
        one_year_employee_growth_rate_min: Optional[str] = None,
        one_year_employee_growth_rate_max: Optional[str] = None,
        two_year_employee_growth_rate_min: Optional[str] = None,
        two_year_employee_growth_rate_max: Optional[str] = None,
        business_model: Optional[List[str]] = None,
        engagement_start_date: Optional[str] = None,
        engagement_end_date: Optional[str] = None,
        engagement_type: Optional[List[str]] = None,
        rpp: Optional[int] = None,
        page: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **extra_filters: Any,
    ) -> Dict[str, Any]:
        """Search for companies using detailed filters.

        Parameters
        ----------
        marketing_department_budget_min : Optional[int]
            Minimum marketing department budget (in thousands).
        marketing_department_budget_max : Optional[int]
            Maximum marketing department budget (in thousands).
        finance_department_budget_min : Optional[int]
            Minimum finance department budget (in thousands).
        finance_department_budget_max : Optional[int]
            Maximum finance department budget (in thousands).
        it_department_budget_min : Optional[int]
            Minimum IT department budget (in thousands).
        it_department_budget_max : Optional[int]
            Maximum IT department budget (in thousands).
        hr_department_budget_min : Optional[int]
            Minimum HR department budget (in thousands).
        hr_department_budget_max : Optional[int]
            Maximum HR department budget (in thousands).
        certified : Optional[int]
            1 for certified companies, 0 for not certified.
        exclude_defunct_companies : Optional[bool]
            When true, excludes defunct companies.
        company_ticker : Optional[List[str]]
            Company stock ticker symbols.
        company_description : Optional[str]
            Words describing the company.
        company_type : Optional[str]
            Company type (e.g., private, public).
        address : Optional[str]
            Company address.
        street : Optional[str]
            Street of company address.
        zip_code : Optional[str]
            Zip code of primary address.
        state : Optional[str]
            State of company.
        country : Optional[str]
            Country of company.
        continent : Optional[str]
            Continent of company.
        company_id : Optional[str]
            ZoomInfo company ID (comma-separated for multiple).
        company_name : Optional[str]
            Name of the company.
        company_website : Optional[str]
            Company domain (comma-separated list allowed).
        parent_id : Optional[str]
            ZoomInfo ID for parent company.
        ultimate_parent_id : Optional[str]
            ZoomInfo ID for ultimate parent company.
        zip_code_radius_miles : Optional[str]
            Radius in miles around ``zip_code``.
        hash_tag_string : Optional[str]
            Hash tags for a company (comma-separated).
        tech_attribute_tag_list : Optional[str]
            Technology product tags.
        sub_unit_types : Optional[str]
            Sub unit types (use with parent IDs).
        primary_industries_only : Optional[bool]
            If true, require results to match primary industries.
        industry_codes : Optional[str]
            Top-level industry codes (comma-separated).
        industry_keywords : Optional[str]
            Industry keywords (supports ``AND``/``OR``).
        sic_codes : Optional[str]
            SIC codes (comma-separated).
        naics_codes : Optional[str]
            NAICS codes (comma-separated).
        revenue : Optional[str]
            Predefined revenue range IDs.
        revenue_min : Optional[int]
            Minimum annual revenue (thousands USD).
        revenue_max : Optional[int]
            Maximum annual revenue (thousands USD).
        employee_range_min : Optional[str]
            Minimum employee count.
        employee_range_max : Optional[str]
            Maximum employee count.
        employee_count : Optional[str]
            Predefined employee count range IDs.
        company_ranking : Optional[str]
            Company ranking IDs (comma-separated).
        metro_region : Optional[str]
            Metro regions (comma-separated).
        location_search_type : Optional[str]
            Location search type (PersonOrHQ, etc.).
        funding_amount_min : Optional[int]
            Minimum funding amount (thousands).
        funding_amount_max : Optional[int]
            Maximum funding amount (thousands).
        funding_start_date : Optional[str]
            Funding start date ``YYYY-MM-DD``.
        funding_end_date : Optional[str]
            Funding end date ``YYYY-MM-DD``.
        zoominfo_contacts_min : Optional[str]
            Minimum number of ZoomInfo contacts.
        zoominfo_contacts_max : Optional[str]
            Maximum number of ZoomInfo contacts.
        excluded_regions : Optional[str]
            States or metro areas to exclude.
        company_structure_included_sub_unit_types : Optional[str]
            Company hierarchical structure types to include.
        one_year_employee_growth_rate_min : Optional[str]
            Minimum one-year employee growth rate.
        one_year_employee_growth_rate_max : Optional[str]
            Maximum one-year employee growth rate.
        two_year_employee_growth_rate_min : Optional[str]
            Minimum two-year employee growth rate.
        two_year_employee_growth_rate_max : Optional[str]
            Maximum two-year employee growth rate.
        business_model : Optional[List[str]]
            Business models (e.g., B2B, B2C, B2G).
        engagement_start_date : Optional[str]
            Engagement start date ``YYYY-MM-DD``.
        engagement_end_date : Optional[str]
            Engagement end date ``YYYY-MM-DD``.
        engagement_type : Optional[List[str]]
            Engagement types (e.g., email, phone).
        rpp : Optional[int]
            Results per page limit.
        page : Optional[int]
            Page number for pagination.
        sort_by : Optional[str]
            Field name to sort results by.
        sort_order : Optional[str]
            Sort order (``asc`` or ``desc``).
        **extra_filters : Any
            Additional filters passed directly to the API.

        Returns
        -------
        Dict[str, Any]
            Parsed JSON response from the API.
        """

        def to_camel(name: str) -> str:
            parts = name.split("_")
            return parts[0] + "".join(p.capitalize() for p in parts[1:])

        params = {
            to_camel(k): v
            for k, v in locals().items()
            if k not in {"self", "extra_filters"} and v is not None
        }
        params.update(extra_filters)
        return self._post("/search/company", params)


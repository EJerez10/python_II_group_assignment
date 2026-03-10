from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import io

import pandas as pd
import requests


class SimFinError(Exception):
    """Base error for SimFin wrapper."""


class SimFinHTTPError(SimFinError):
    """Raised when SimFin returns a non-200 response."""


class SimFinParseError(SimFinError):
    """Raised when response cannot be parsed into a DataFrame."""


def _validate_date(date_str: str, name: str) -> None:
    """Ensure dates are YYYY-MM-DD."""
    try:
        pd.to_datetime(date_str, format="%Y-%m-%d", errors="raise")
    except Exception as e:
        raise ValueError(f"{name} must be in 'YYYY-MM-DD' format. Got: {date_str}") from e


@dataclass
class PySimFin:
    api_key: str
    base_url: str = "https://simfin.com/api/v3"  # adjust if your instructions use a different base
    timeout: int = 30

    def __post_init__(self) -> None:
        if not self.api_key or not isinstance(self.api_key, str):
            raise ValueError("api_key must be a non-empty string.")
        self.session = requests.Session()
        self.session.headers.update({"api-key": self.api_key})

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Internal GET helper that returns a DataFrame."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            resp = self.session.get(url, params=params or {}, timeout=self.timeout)
        except requests.Timeout as e:
            raise SimFinHTTPError(f"Request timed out: {url}") from e
        except requests.RequestException as e:
            raise SimFinHTTPError(f"Request failed: {url}") from e

        if resp.status_code != 200:
            # Try to include useful error detail
            detail = resp.text[:500] if resp.text else ""
            raise SimFinHTTPError(f"HTTP {resp.status_code} for {url}. Details: {detail}")

        # Try parse as CSV first (common for financial/prices endpoints)
        content_type = (resp.headers.get("Content-Type") or "").lower()
        text = resp.text.strip()

        if not text:
            return pd.DataFrame()

        try:
            if "text/csv" in content_type or "," in text.splitlines()[0]:
                return pd.read_csv(io.StringIO(text))
            # Otherwise try JSON
            data = resp.json()
            # Many APIs return dict with 'data' key; handle both
            if isinstance(data, dict) and "data" in data:
                return pd.DataFrame(data["data"])
            return pd.DataFrame(data)
        except Exception as e:
            raise SimFinParseError("Could not parse SimFin response into a DataFrame.") from e

    # -----------------------------
    # Public methods (your spec)
    # -----------------------------
    def get_share_prices(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Return a DataFrame with all prices for ticker between start and end.
        Dates must be YYYY-MM-DD.
        """
        ticker = ticker.strip().upper()
        if not ticker:
            raise ValueError("ticker cannot be empty.")
        _validate_date(start, "start")
        _validate_date(end, "end")

        # NOTE: path/params may need adjustment to match your course’s SimFin endpoint format.
        # Keep it consistent and easy to change.
        params = {"ticker": ticker, "start": start, "end": end}
        return self._get("/shareprices", params=params)

    def get_financial_statement(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Return a DataFrame with financial statements for ticker between start and end.
        """
        ticker = ticker.strip().upper()
        if not ticker:
            raise ValueError("ticker cannot be empty.")
        _validate_date(start, "start")
        _validate_date(end, "end")

        params = {"ticker": ticker, "start": start, "end": end}
        return self._get("/financials", params=params)
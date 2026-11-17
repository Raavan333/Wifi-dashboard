# app/utils/filters.py


from typing import Any
 
 
class QueryBuilder:
    """
    Generic PostgreSQL WHERE clause builder.
 
    Maintains:
 
        WHERE conditions
        Query parameters
        ORDER BY
        LIMIT
        OFFSET
    """
 
    def __init__(self) -> None:
 
        self.conditions: list[str] = []
 
        self.params: list[Any] = []
 
    # ==========================================================
    # INTERNAL
    # ==========================================================
 
    def _add_param(
        self,
        value: Any,
    ) -> int:
 
        self.params.append(value)
 
        return len(self.params)
 
    # ==========================================================
    # EQUALS
    # ==========================================================
 
    def equals(
        self,
        column: str,
        value: Any,
    ):
 
        if value is None:
            return
 
        idx = self._add_param(value)
 
        self.conditions.append(
            f"{column} = ${idx}"
        )
 
    # ==========================================================
    # ILIKE
    # ==========================================================
 
    def contains(
        self,
        column: str,
        value: str | None,
    ):
 
        if not value:
            return
 
        idx = self._add_param(
            f"%{value}%"
        )
 
        self.conditions.append(
            f"{column} ILIKE ${idx}"
        )
 
    # ==========================================================
    # LIST
    # ==========================================================
 
    def in_list(
        self,
        column: str,
        values: list | None,
    ):
 
        if not values:
            return
 
        idx = self._add_param(values)
 
        self.conditions.append(
            f"{column} = ANY(${idx})"
        )
 
    # ==========================================================
    # BOOLEAN
    # ==========================================================
 
    def boolean(
        self,
        column: str,
        value: bool | None,
    ):
 
        if value is None:
            return
 
        idx = self._add_param(value)
 
        self.conditions.append(
            f"{column} = ${idx}"
        )
 
    # ==========================================================
    # DATE RANGE
    # ==========================================================
 
    def date_range(
        self,
        column: str,
        start,
        end,
    ):
 
        if start:
 
            idx = self._add_param(start)
 
            self.conditions.append(
                f"{column} >= ${idx}"
            )
 
        if end:
 
            idx = self._add_param(end)
 
            self.conditions.append(
                f"{column} <= ${idx}"
            )
 
    # ==========================================================
    # RAW CONDITION
    # ==========================================================
 
    def raw(
        self,
        clause: str,
    ):
 
        if clause:
            self.conditions.append(
                clause
            )
 
    # ==========================================================
    # VALID USERS
    # ==========================================================
 
    def valid_users_only(self):
 
        self.conditions.append(
            """
            wus.employee_id IS NOT NULL
            AND wus.total_success_count > 0
            AND wus.ux_available = TRUE
            """
        )
 
    # ==========================================================
    # BUILD
    # ==========================================================
 
    def build_where(self) -> str:
 
        if not self.conditions:
            return ""
 
        return (
            " WHERE "
            + " AND ".join(
                f"({c})"
                for c in self.conditions
            )
        )
 
    # ==========================================================
    # ORDER BY
    # ==========================================================
 
    @staticmethod
    def build_order_by(
        sort_by: str | None,
        sort_order: str = "desc",
        allowed_columns: set[str] | None = None,
    ) -> str:
 
        if not sort_by:
            return ""
 
        if allowed_columns:
 
            if sort_by not in allowed_columns:
                return ""
 
        sort_order = (
            "DESC"
            if sort_order.lower() == "desc"
            else "ASC"
        )
 
        return (
            f" ORDER BY "
            f"{sort_by} {sort_order}"
        )
 
    # ==========================================================
    # PAGINATION
    # ==========================================================
 
    def build_pagination(
        self,
        page: int,
        page_size: int,
    ) -> str:
 
        offset = (
            max(page, 1) - 1
        ) * page_size
 
        limit_idx = self._add_param(
            page_size
        )
 
        offset_idx = self._add_param(
            offset
        )
 
        return (
            f" LIMIT ${limit_idx}"
            f" OFFSET ${offset_idx}"
        )
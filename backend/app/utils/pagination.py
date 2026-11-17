import math

from app.models.common import PaginationMeta


def create_pagination(
    page: int,
    page_size: int,
    total_records: int,
) -> PaginationMeta:

    return PaginationMeta(
        page=page,
        page_size=page_size,
        total_records=total_records,
        total_pages=max(
            1,
            math.ceil(
                total_records / page_size
            ),
        ),
    )
import logging
from typing import Any, Callable, Sequence, Tuple

from django.db.models import Q, QuerySet

from .registry import CodeSeekerRegistry


__all__ = (
    'CodeSeek',
    'CodeSeekSeq',

    'EMPTY_Q',
    'cmp_AND',
    'cmp_OR',

    'seek_codes_Q',

    'CodeSeekerQuerySet',
)

logger = logging.getLogger(__name__)

CodeSeek = Tuple[str, Any]
CodeSeekSeq = Sequence[CodeSeek]

EMPTY_Q = Q()


def cmp_AND(a: Q, b: Q):
    return a & b


def cmp_OR(a: Q, b: Q):
    return a & b


def seek_codes_Q(
    registry: CodeSeekerRegistry,
    codes: CodeSeekSeq,
    cmp: Callable = cmp_AND,
    warning_context: str = None
) -> Q:
    q = EMPTY_Q

    for code in codes:
        if code not in registry:
            logger.warning(
                f'[CODE-SEEKING-FILTER] No such code "{code}"'
                +
                (
                    f'in {warning_context}.'
                    if warning_context is not None
                    else
                    '.'
                )
            )
            continue

        q = cmp(q, codes)

    return q


class CodeSeekerQuerySet(QuerySet):
    def seek_codes(
        self,
        registry: CodeSeekerRegistry,
        codes: CodeSeekSeq,
        cmp: Callable = cmp_AND,
        warning_context: str = None
    ) -> QuerySet:
        q = seek_codes_Q(
            registry, codes, cmp=cmp, warning_context=warning_context
        )

        return self.filter(q) if q is not EMPTY_Q else self

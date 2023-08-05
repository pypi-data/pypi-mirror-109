from typing import TypeVar
from wcd_geo_db.modules.code_seeker import CodeSeekerRegistry, query


QT = TypeVar('QT', bound=query.CodeSeekerQuerySet)


class CodeSeekingClientMixin:
    code_seeker_registry: CodeSeekerRegistry

    def __init__(
        self, *_, **kw
    ):
        code_seeker_registry = kw.get('code_seeker_registry')

        assert code_seeker_registry is not None, (
            'Code seeking registry must not be empty.'
        )

        super().__init__(**kw)

        self.code_seeker_registry = code_seeker_registry

    def _filter_codes(self, qs: QT, codes: query.CodeSeekSeq) -> QT:
        return qs.seek_codes(
            self.code_seeker_registry, codes,
            warning_context=f'{self.__class__} client\'s registry'
        )

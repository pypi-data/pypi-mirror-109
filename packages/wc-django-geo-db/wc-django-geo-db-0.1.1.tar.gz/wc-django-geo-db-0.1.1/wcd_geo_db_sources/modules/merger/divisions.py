from typing import Any, Dict, Sequence, Tuple
from pxd_postgres.ltree import LtreeValue
from wcd_geo_db.modules.bank.db import Division, DivisionTranslation
from wcd_geo_db.modules.code_seeker import CodeSeekerRegistry

from .code_seeker import get_code_seeker_registry
from .dtos import DivisionItem, DivisionTranslationItem


__all__ = (
    'CodeMapper',
    'find_by_codes',
    'make_merge_division_code',
    'merge_divisions',
    'merge_division_translations',
)


class CodeMapper:
    items: Sequence[Division]
    registry: CodeSeekerRegistry
    mapping: Dict[str, Sequence[Tuple[Any, Division]]]

    def __init__(self, registry: CodeSeekerRegistry, items):
        self.items = items
        self.registry = registry
        self.mapping = {}

        self.prepare_mapping()

    def prepare_mapping(self):
        mapping = self.mapping

        for item in self.items:
            for code, value in item.codes.items():
                mapping[code] = mapping.get(code) or []
                mapping[code].append((value, item))

    def get_by_codes(self, codes: Sequence):
        r = self.registry

        return (
            item
            for code, value in codes
            for stored_value, item in (self.mapping.get(code) or [])
            if (
                # code in self.registry and
                self.registry[code].eq(value, stored_value)
            )
        )

    def get_eq(self, item: DivisionItem) -> Division:
        return next(self.get_by_codes([item['code']]), None)


def collect_item_codes(item: DivisionItem):
    return [item['code']] + item['path']


def find_by_codes(registry: CodeSeekerRegistry, items: Sequence[DivisionItem]) -> CodeMapper:
    return CodeMapper(
        registry,
        Division.objects
        .seek_codes(registry=registry, codes=[
            (code, value)
            for item in items
            # TODO: SOMETHING WRONG HERE
            # [CODE-SEEKING-FILTER] issue must be fixed
            for code, value in collect_item_codes(item)
        ])
    )


def make_merge_division_code(seeker, code: Any):
    return seeker.name, code


def merge_divisions(items: Sequence[DivisionItem]):
    creations = []
    updates = []
    merge_failures = []
    codes_founded = find_by_codes(get_code_seeker_registry(), items)

    for item in items:
        eqs = codes_founded.get_eq(item)
        path = [codes_founded.get_eq({'code': code}) for code in item['path']]

        if None in path:
            merge_failures.append(('path_failure', item))
            continue

        path = [x.id for x in path]
        code, code_value = item['code']
        parent_id = path[-1] if len(path) > 0 else None

        if eqs is None:
            creations.append(Division(
                name = item['name'],
                codes = {code: code_value},
                types = item['types'],
                level = item['level'],
                # TODO: Fix this to work for any tree level depth
                # path = LtreeValue(path),
                parent_id=parent_id,
            ))
        else:
            eqs.path = LtreeValue(path + [eqs.id])
            eqs.level = item['level']
            eqs.codes[code] = code_value
            eqs.parent_id = parent_id

            if eqs.name != item['name']:
                synonyms = {s.strip() for s in item.synonyms.split(',')}
                synonyms.add(item['name'])
                eqs.synonyms = ','.join(synonyms)

            eqs.types = list(set((eqs.types or []) + item['types']))

            updates.append(eqs)

    print(merge_failures)

    Division.objects.bulk_create(creations)
    Division.objects.bulk_update(
        updates, fields=(
            'name', 'types', 'level', 'codes', 'synonyms', 'parent_id'
        )
    )
    Division.objects.all().update_roughly_invalid_tree()


def merge_division_translations(
    language: str,
    items: Sequence[DivisionTranslationItem]
):
    pass

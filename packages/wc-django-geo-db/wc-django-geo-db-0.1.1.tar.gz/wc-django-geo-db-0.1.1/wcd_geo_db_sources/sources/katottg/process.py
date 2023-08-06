import json
from functools import partial
from django.db import transaction
from wcd_geo_db.const import DivisionLevel
from wcd_geo_db_sources.modules.process import stage
from wcd_geo_db.modules.bank.db import Division, DivisionTranslation
from wcd_geo_db.modules.code_seeker import ISO3166_SEEKER, registry as seeker_registry
from wcd_geo_db_sources.modules.merger.divisions import merge_divisions, make_merge_division_code

from .._base import BaseImportRunner
from .._base.dtos import DivisionSource
from .parsers import registry
from .const import SOURCE, ImportStage
from .code_seeker import KATOTTG_SEEKER


UPLOAD_URL = (
    'https://www.minregion.gov.ua/wp-content/uploads/2021/04/kodyfikator-2.xlsx'
)
PARSER_VERSION = 'v1'

UKRAINE = DivisionSource(
    name='Україна',
    code=(ISO3166_SEEKER.name, 'UA'),
    path=[],
    level=DivisionLevel.COUNTRY,
    types=['country'],
)


make_code = partial(make_merge_division_code, KATOTTG_SEEKER)


class KATOTTGImportRunner(BaseImportRunner):
    CHUNK_SIZE: int = 5000
    source: str = SOURCE
    Stage: ImportStage = ImportStage
    default_config: dict = {
        'url': UPLOAD_URL,
        'version': PARSER_VERSION,
    }
    parser_registry: dict = registry

    @stage(Stage.MERGE)
    def run_merge(self):
        state = self.state.state

        if KATOTTG_SEEKER.name not in seeker_registry:
            seeker_registry.register(KATOTTG_SEEKER)

        with transaction.atomic():
            if 'country' not in state:
                merge_divisions([UKRAINE])
                self.update_state(partial_state={'country': True})
                return

        offset = state.get('merge_offset', 0)
        chunk = []
        count = self.CHUNK_SIZE
        nest = None

        with open(state['parsed_file'], 'r') as file:
            items = json.loads(file.read())
            l = len(items)

            while count >= 0 and offset < l:
                item = items[offset]

                if nest == None:
                    nest = len(item['path'])

                if len(item['path']) != nest:
                    break

                item['code'] = make_code(item['code'])
                item['path'] = ([UKRAINE['code']] + list(map(make_code, item['path'])))[:-1]
                chunk.append(item)

                offset += 1
                count -= 1

            with transaction.atomic():
                merge_divisions(chunk)
                self.update_state(partial_state={'merge_offset': offset})

            if l > offset:
                return

        self.update_state(stage=self.Stage.MERGE_TRANSLATIONS)

    @stage(Stage.MERGE_TRANSLATIONS)
    def run_merge_translations(self):
        self.update_state(stage=self.Stage.CLEANUP)

from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.cycle import get_feed
from hestia_earth.models.utils.emission import _new_emission
from . import MODEL

TERM_ID = 'ch4ToAirEntericFermentation'


def _emission(value: float, sd: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['sd'] = [sd]
    emission['methodTier'] = EmissionMethodTier.TIER_2.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _get_animalProduct_lookup_value(cycle: dict, lookup_col: str):
    primary_product = find_primary_product(cycle)
    term_id = primary_product.get('term', {}).get('@id') if primary_product else {}
    lookup = download_lookup('animalProduct-ipcc2019Tier2Ch4.csv', True)
    return safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(lookup_col)))


def _run(feed: float, enteric_factor: float, enteric_sd: float):
    value = feed * enteric_factor
    return [_emission(value, enteric_sd)]


def _should_run(cycle: dict):
    enteric_factor = _get_animalProduct_lookup_value(cycle, 'Ym') / 100
    enteric_sd = _get_animalProduct_lookup_value(cycle, 'SD')
    feed = get_feed(cycle)
    logger.debug('feed=%s, enteric_factor=%s', feed, enteric_factor)

    should_run = all([feed != 0, enteric_factor != 0])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, feed, enteric_factor, enteric_sd


def run(cycle: dict):
    should_run, feed, enteric_factor, enteric_sd = _should_run(cycle)
    return _run(feed, enteric_factor, enteric_sd) if should_run else []

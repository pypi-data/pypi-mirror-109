from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.model import filter_list_term_type, find_term_match
from hestia_earth.utils.tools import list_average, list_sum

from ..log import logger
from . import _filter_list_term_unit, Units
from .crop import get_crop_property_value_converted
from .dataCompleteness import _is_term_type_complete
from .input import get_total_nitrogen
from .measurement import most_relevant_measurement_value
from .site import valid_site_type as site_valid_site_type


def get_land_occupation(cycle: dict):
    measurements = cycle.get('site', {}).get('measurements', [])
    fallowCorrection = find_term_match(measurements, 'fallowCorrection').get('value', [])
    return cycle.get('cycleDuration', 365) / 365 * list_average(fallowCorrection) if len(fallowCorrection) > 0 else None


def get_excreta_N_total(cycle: dict) -> float:
    """
    Get the total nitrogen content of excreta used in the Cycle.

    The result is the sum of every excreta specified in `kg N` as an `Input` or a `Product`.

    Note: in the event where `dataCompleteness.products` is set to `True` and there are no excreta inputs or products,
    `0` will be returned.

    Parameters
    ----------
    cycle : dict
        The `Cycle` as defined in the Hestia Schema.

    Returns
    -------
    float
        The total value as a number.
    """
    inputs = filter_list_term_type(cycle.get('inputs', []), TermTermType.EXCRETA)
    products = filter_list_term_type(cycle.get('products', []), TermTermType.EXCRETA)
    values = get_total_nitrogen(inputs) + get_total_nitrogen(products)
    return 0 if len(values) == 0 and _is_term_type_complete(cycle, {'termType': 'products'}) else list_sum(values)


def calculate_land_occupation(cycle: dict, site: dict, primary_product: dict):
    cycleDuration = cycle.get('cycleDuration', 365)
    fallowCorrection = list_average(
        most_relevant_measurement_value(site.get('measurements', []), 'fallowCorrection', cycle.get('endDate')),
        1
    )
    # 1) Account for crop duration (for example multiple crops on a given field in a given year)
    value = 10000 * cycleDuration / 365
    # 2) Account for fallow period in crop production
    value = value * fallowCorrection
    # 3) Reduce the impact by economic value share
    value = value * (primary_product.get('economicValueShare', 0) / 100)
    # 4) Divide by product value to estimate land occupation (use) per kg.
    value = value / list_sum(primary_product.get('value', [0]))
    logger.debug('land occupation=%s', value)
    return value


def valid_site_type(cycle: dict, include_permanent_pasture=False):
    """
    Check if the `site.siteType` of the cycle is `cropland`.

    Parameters
    ----------
    cycle : dict
        The `Site`.
    include_permanent_pasture : bool
        If set to `True`, `permanent pasture` is also allowed. Defaults to `False`.

    Returns
    -------
    bool
        `True` if `siteType` matches the allowed values, `False` otherwise.
    """
    site_types = [SiteSiteType.CROPLAND.value] + (
        [SiteSiteType.PERMANENT_PASTURE.value] if include_permanent_pasture else []
    )
    return site_valid_site_type(cycle.get('site', {}), site_types)


def get_feed(cycle: dict):
    inputs = _filter_list_term_unit(cycle.get('inputs', []), Units.KG)
    inputs = (
        filter_list_term_type(inputs, TermTermType.CROP) +
        filter_list_term_type(inputs, TermTermType.ANIMALPRODUCT) +
        filter_list_term_type(inputs, TermTermType.OTHER)
    )
    return list_sum([get_crop_property_value_converted(input, 'grossEnergyContent') for input in inputs])

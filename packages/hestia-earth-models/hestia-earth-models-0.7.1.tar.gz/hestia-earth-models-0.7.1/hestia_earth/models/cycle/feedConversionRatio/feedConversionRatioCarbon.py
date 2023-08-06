from hestia_earth.models.utils.cycle import get_feed

from hestia_earth.models.log import logger
TERM_ID = 'feedConversionRatioCarbon'


def run(cycle: dict):
    feed = get_feed(cycle)
    logger.debug('term=%s, feed=%s', TERM_ID, feed)
    return feed * 0.021

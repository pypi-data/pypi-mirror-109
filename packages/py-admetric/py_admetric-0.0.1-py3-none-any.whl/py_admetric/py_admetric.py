from py_admetric.utils import validate_negative, validate_integer, safe_div


def cpi(cost: int, impressions: int) -> float:
    """Calculate CPI(Cost Per Impression)

    Args:
        cost (integer): expense to earn impressions
        impressions (integer): count of times ads display to users
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cpi(1,1)
    """
    validate_integer(cost, impressions)
    validate_negative(cost, impressions)
    return safe_div(cost, impressions)


def cpm(cost: int, impressions: int) -> float:
    """Calculate CPM(Cost Per Thousand Impressions (Cost Per Mille))

    Args:
        cost (integer): expense to earn impressions
        impressions (integer): count of times ads display to users
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cpm(1,1)
    """
    validate_integer(cost, impressions)
    validate_negative(cost, impressions)
    return safe_div(cost, impressions)*1000


def cpc(cost: int, clicks: int) -> float:
    """Calculate CPC(Cost Per Click)

    Args:
        cost (integer): expense to earn impressions
        clicks (integer): count of times users have clicked on ads
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cpc(1,1)
    """
    validate_integer(cost, clicks)
    validate_negative(cost, clicks)
    return safe_div(cost, clicks)


def cpa(cost: int, conversions: int) -> float:
    """Calculate CPA(Cost Per Action (Cost Per Acquisition))

    Args:
        cost (integer): expense to earn impressions
        conversions (integer): count of times users have acted on ads
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cpa(1,1)
    """
    validate_integer(cost, conversions)
    validate_negative(cost, conversions)
    return safe_div(cost, conversions)


def cpv(cost: int, video_views: int) -> float:
    """Calculate CPV(Cost Per View)

    Args:
        cost (integer): expense to earn impressions
        video_views (integer): count of times ads viewed
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cpv(1,1)
    """
    validate_integer(cost, video_views)
    validate_negative(cost, video_views)
    return safe_div(cost, video_views)


def ctr(clicks: int, impressions: int) -> float:
    """Calculate CTR(Click Through Rate)

    Args:
        clicks (integer): count of times users have clicked on ads
        impressions (integer): count of times ads display to users
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.ctr(1,1)
    """
    validate_integer(clicks, impressions)
    validate_negative(clicks, impressions)
    return safe_div(clicks, impressions)


def vtr(video_views: int, impressions: int) -> float:
    """Calculate VTR(View Through Rate)

    Args:
        video_views (integer): count of times ads viewed
        impressions (integer): count of times ads display to users
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.vtr(1,1)
    """
    validate_integer(video_views, impressions)
    validate_negative(video_views, impressions)
    return safe_div(video_views, impressions)


def cvr(conversions: int, clicks: int) -> float:
    """Calculate CVR(Conversion Rate)

    Args:
        conversions (integer): count of times users have acted on ads
        clicks (integer): count of times users have clicked on ads
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import py_admetric
      >>> val = py_admetric.cvr(1,1)
    """
    validate_integer(conversions, clicks)
    validate_negative(conversions, clicks)
    return safe_div(conversions, clicks)


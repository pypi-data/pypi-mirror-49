from django.conf import settings

def websitecoverpage(request):
    # bail if not a non-Ajax GET request
    if request.method != 'GET' or request.is_ajax():
        return {}

    # get config
    config = getattr(settings, 'WEBSITE_COVERPAGE', {})

    # bail if cookie already set
    cookie_name = config.get('cookie_name', 'coverpage')
    if cookie_name in request.COOKIES:
        print('coverpage cookie exists')
        return {}

    # get ignore_urls
    ignore_urls = config.get('ignore_urls', '[]') + [
        '/favicon.ico',
        '/robots.txt'
    ]
    for ig in ignore_urls:
        if request.path.startswith(ig):
            return {}

    # ignore common bots
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    bots = [
        '360spider',
        'adsbot-google',
        'ahrefs',
        'apachebench', # not a bot, but it can go here
        'archive.org',
        'baiduspider',
        'bingbot',
        'bingpreview',
        'dotbot',
        'duckduckgo',
        'duckduckbot',
        'exabot',
        'facebook',
        'feedfetcher-google',
        'googlebot',
        'googleimageproxy',
        'ia_archiver',
        'mediapartners-google',
        'mj12bot',
        'msnbot',
        'panscient.com',
        'pinterest',
        'slackbot',
        'slurp',
        'sogou',
        'surveybot',
        'twitterbot',
        'voilabot',
        'yahoo-mmcrawler',
        'yahoomailproxy',
        'yandexbot'
    ]
    for bot in bots:
        if bot in ua:
            return {}

    # attempt to find from memcache
    #
    #

    # attempt to find from database
    #
    #

    """
    # check start time
    dt_from = config.get('start', None)
    if dt_from is not None:
        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
        dt_from = datetime.datetime(*dt_from, tzinfo=tz)
        if now() < dt_from:
            return False

    # check end time
    dt_to = config.get('end', None)
    if dt_to is not None:
        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
        dt_to = datetime.datetime(*dt_to, tzinfo=tz)
        if now() > dt_to:
            return False
    """

    # temporary values
    html = """
<table onclick="websiteCoverPage.close()">
    <tr>
        <td>
            <img src="/static/coverpage/2/king_birthday.jpg" />
        </td>
    </tr>
</table>
    """

    style = """
#websitecoverpage {
    background: rgba(0, 0, 0, 0.5);
    height: 100vh;
    left: 0;
    position: fixed;
    right: 0;
    top: 0;
    z-index: 9999998;
}

#websitecoverpage table, tr {
    height: 100vh;
    width: 100%;
}

#websitecoverpage td {
    padding: 25px;
    text-align: center;
    vertical-align: middle;
}

#websitecoverpage img {
    box-shadow: 0px 0px 25px 5px rgba(0, 0, 0, 0.5);
    cursor: pointer;
    max-width: 800px;
    width: 100%;
}
    """

    # coverpage found: return it
    return {
        'websitecoverpage': {
            'cookie_name': cookie_name,
            'html': html,
            'style': style
        }
    }
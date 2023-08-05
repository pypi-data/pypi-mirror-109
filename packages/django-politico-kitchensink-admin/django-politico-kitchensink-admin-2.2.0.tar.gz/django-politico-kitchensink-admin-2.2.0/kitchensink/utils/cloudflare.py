import requests
from kitchensink.conf import settings


def post_request(opts):
    url = "https://api.cloudflare.com/client/v4/zones/{}/purge_cache".format(
        settings.CLOUDFLARE_ZONE
    )

    headers = {
        "Authorization": "Bearer {}".format(settings.CLOUDFLARE_TOKEN),
        "Content-Type": "application/json"
    }

    return requests.post(
        url,
        headers=headers,
        json=opts
    )


def purge_cache_by_url(urls, cloudflare_opts={}):
    urls_list = urls if isinstance(urls, list) else [urls]

    default_opts = {
        "files": urls_list
    }

    opts = {}
    opts.update(default_opts)
    opts.update(cloudflare_opts)

    return post_request(opts)


def purge_cache_by_prefix(prefixes, cloudflare_opts={}):
    prefixes_list = prefixes if isinstance(prefixes, list) else [prefixes]

    default_opts = {
        "prefixes": prefixes_list
    }

    opts = {}
    opts.update(default_opts)
    opts.update(cloudflare_opts)

    return post_request(opts)

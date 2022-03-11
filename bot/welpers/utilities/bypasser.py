import requests
import re
import cloudscraper
import urllib.parse
import time
from bs4 import BeautifulSoup
from base64 import standard_b64encode
from bot import Config

# wetransfer
WETRANSFER_API_URL = 'https://wetransfer.com/api/v4/transfers'
WETRANSFER_DOWNLOAD_URL = WETRANSFER_API_URL + '/{transfer_id}/download'

def art_j(id):
    scraper = cloudscraper.create_scraper(interpreter='nodejs', allow_brotli=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"https://www.artstation.com/projects/{id}.json"
    response = scraper.get(apix, headers=headers)
    query = response.json()
    return query

def art_k(id):
    uhh = art_j(id)
    text = f'Title : {uhh["title"]}\n\n<a href="{uhh["assets"][0]["image_url"]}">ART 🎨</a>'
    return text

def mdis_k(urlx):
    scraper = cloudscraper.create_scraper(interpreter='nodejs', allow_brotli=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"http://x.egraph.workers.dev/?param={urlx}"
    response = scraper.get(apix, headers=headers)
    query = response.json()
    return query

def mdisk(url):
    check = re.findall(r'\bhttps?://.*mdisk\S+', url)
    if not check:
        textx = f'Invalid mdisk url'
        return textx
    else:
        try:
            fxl = url.split("/")
            urlx = fxl[-1]
            uhh = mdis_k(urlx)
            text = f'Title : {uhh["filename"]}\n\n{uhh["download"]}'
            return text
        except ValueError:
            textx = f'The content is deleted.'
            return textx

def gplinks(url):
    check = re.findall(r'\bhttps?://.*gplink\S+', url)
    if not check:
        textx = f'Invalid GPLinks url'
        return textx
    else:
        scraper = cloudscraper.create_scraper(interpreter='nodejs', allow_brotli=False)
        res = scraper.get(url)
        h = { "referer": res.url }
        res = scraper.get(url, headers=h)
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }
        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }
        time.sleep(10) # !important
        p = urllib.parse.urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        res = scraper.post(final_url, data=data, headers=h).json()
        return res['url']

def droplink(url):
    check = re.findall(r'\bhttps?://.*droplink\S+', url)
    if not check:
        textx = f'Invalid DropLinks url'
        return textx
    else:
        client = requests.Session()
        res = client.get(url)
        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
        h = {'referer': ref}
        res = client.get(url, headers=h)
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }
        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }
        p = urllib.parse.urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()
        return res['url']

def _prepare_session() -> requests.Session:
    """Prepare a wetransfer.com session.
    Return a requests session that will always pass the required headers
    and with cookies properly populated that can be used for wetransfer
    requests.
    """
    s = requests.Session()
    r = s.get('https://wetransfer.com/')
    m = re.search('name="csrf-token" content="([^"]+)"', r.text)
    s.headers.update({
        'x-csrf-token': m.group(1),
        'x-requested-with': 'XMLHttpRequest',
    })

    return s

def wetransfer(url):
    """Given a wetransfer.com download URL download return the downloadable URL.
    The URL should be of the form `https://we.tl/' or
    `https://wetransfer.com/downloads/'. If it is a short URL (i.e. `we.tl')
    the redirect is followed in order to retrieve the corresponding
    `wetransfer.com/downloads/' URL.
    The following type of URLs are supported:
     - `https://we.tl/<short_url_id>`:
        received via link upload, via email to the sender and printed by
        `upload` action
     - `https://wetransfer.com/<transfer_id>/<security_hash>`:
        directly not shared in any ways but the short URLs actually redirect to
        them
     - `https://wetransfer.com/<transfer_id>/<recipient_id>/<security_hash>`:
        received via email by recipients when the files are shared via email
        upload
    Return the download URL (AKA `direct_link') as a str or None if the URL
    could not be parsed.
    """
    # Follow the redirect if we have a short URL
    if url.startswith('https://we.tl/'):
        r = requests.head(url, allow_redirects=True)
        url = r.url

    recipient_id = None
    params = urllib.parse.urlparse(url).path.split('/')[2:]

    if len(params) == 2:
        transfer_id, security_hash = params
    elif len(params) == 3:
        transfer_id, recipient_id, security_hash = params
    else:
        return None

    j = {
        "intent": "entire_transfer",
        "security_hash": security_hash,
    }
    if recipient_id:
        j["recipient_id"] = recipient_id
    s = _prepare_session()
    r = s.post(WETRANSFER_DOWNLOAD_URL.format(transfer_id=transfer_id),
               json=j)

    j = r.json()
    if "direct_link" in j:
        return j["direct_link"]
    else:
        xo = f'The content is expired/deleted.'
        return xo

def encod(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    encoded = bytes_b64.decode('ascii')
    return encoded

def bifm(url):
    client = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"{Config.BIFM_URL}={url}"
    response = client.get(apix, headers=headers)
    query = response.json()
    if "destination" in query:
        return query["destination"]
    else:
        return query["err"]

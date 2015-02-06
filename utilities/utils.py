__author__ = 'swolfod'

from urllib.parse import urlparse
import math
import re
import requests
import sys
import os
from lxml import html
from difflib import SequenceMatcher

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def getBoolValue(v):
    if isinstance(v, str):
        return str2bool(v)

    return v


def calcDist(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
    # haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def listAllFiles(directory):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, name)):
            files.append(name)
    return files

def LoadHttpString(link, postData={}, encoding=None, session=None, headers=None, timeout=30):
    for i in range(3):
        try:
            if link.find("#") >= 0:
                link = link[:link.find("#")]

            if not link.lower().startswith("http"):
                link = 'http://' + link

            requestHeaders = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            if headers:
                requestHeaders.update(headers)

            if not session:
                session = requests.Session()

            if postData:
                res = session.post(link, data=postData, headers=requestHeaders, timeout=timeout)
            else:
                res = session.get(link, headers=requestHeaders, timeout=timeout)
            docContent = res.text
            if not encoding:
                contentType = res.headers['content-type'] if 'content-type' in res.headers else None

                if not (contentType and contentType.find('charset=') >= 0):
                    contentTypeMatch = re.search(r"<meta\s+[^>]*http-equiv=['\"]Content-Type['\"]\s+[^>]*content=['\"]([^'\"]+)['\"] />",
                                                 docContent, re.IGNORECASE)
                    if contentTypeMatch:
                        contentType = contentTypeMatch.group(1)

                if contentType and contentType.find('charset=') >= 0:
                    encoding=contentType.split('charset=')[-1]
                    if encoding.lower() == 'gb2312':
                        encoding = 'gb18030'
            if encoding:
                try:
                    docContent = docContent.decode(encoding)
                except:
                    pass

            return res.url, docContent, session
        except Exception as e:
            if i == 2:
                raise


def ConstructHtmlDoc(htmlStr):
    stderr = sys.stderr
    try:
        sys.stderr = os.devnull
        return html.fromstring(htmlStr)
    finally:
        sys.stderr = stderr


def HtmlEncode(strToEncode):
    return html.escape(strToEncode)


def HtmlDecode(htmlStr):
    return htmlStr.replace('&#39;', "'").replace('&quot;', '"').replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')


def FixLink(linkUrl, srcPageUrl):
    linkUrl = HtmlDecode(linkUrl.strip())

    if linkUrl.lower().startswith("http") or not srcPageUrl.lower().startswith("http"):
        return linkUrl

    if linkUrl.startswith("/"):
        end = srcPageUrl.find("/", srcPageUrl.index("://") + 3)
    elif linkUrl.startswith("?"):
        end = srcPageUrl.find("?")
    else:
        end = srcPageUrl.rfind("/") + 1

    if end < 0:
        end = len(srcPageUrl)
    return srcPageUrl[0:end] + linkUrl


def GetLxmlNodeText(lxmlNode):
    nodeText = ""
    for text in lxmlNode.itertext():
        nodeText += " " + text.strip()

    return nodeText.lstrip()


def LoadXmlNodesText(parentNode, selectPath):
    return [selectedNode.strip() if isinstance(selectedNode, str) else GetLxmlNodeText(selectedNode) for selectedNode in parentNode.xpath(selectPath)]


def LoadCombinedXmlNodesText(parentNode, selectPath):
    return " ".join(LoadXmlNodesText(parentNode, selectPath))


def LoadSingleXmlNodeText(parentNode, selectPath):
    selectedNode = parentNode.xpath(selectPath)
    if selectedNode:
        node = selectedNode[0]
        return node.strip() if isinstance(node, str) else GetLxmlNodeText(node)
    else:
        return None


def ClearComments(doc):
    comments = doc.xpath("//comment()")
    for comment in comments:
        comment.getparent().remove(comment)

def GetInnerText(lxmlNode):
    if lxmlNode is None:
        return ""

    childText = [html.tostring(child, encoding="unicode") for child in lxmlNode.iterchildren()]
    return (lxmlNode.text or '') + ''.join(childText)


def GetSubdirectories(directory):
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]


def GetFiles(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def decimalizeLatLng(lat_lon_str):
    parts = lat_lon_str.split()
    latStr = parts[0].strip()
    lngStr = parts[1].strip()

    return decimalizeGeoCoord(latStr, True), decimalizeGeoCoord(lngStr, False)


def decimalize(degrees, minutes, seconds, direction):
    decimal = int(degrees) + int(minutes if minutes else 0) / 60 + float(seconds if seconds else 0) / 3600
    if direction in 'SW':
        decimal = -decimal
    return decimal


def decimalizeGeoCoord(coordStr, isLat=True):
    regex = r"""(\d+)°(?:-?(\d+)′(?:-?([\d+.]+)″)?)?([NS])""" if isLat else r"""(\d+)°(?:-?(\d+)′(?:-?([\d+.]+)″)?)?([EW])"""
    match = re.match(regex, coordStr.strip())
    if not match:
        raise ValueError("Invalid input string: {0:r}".format(coordStr))

    return decimalize(*match.groups())


def similarity(a, b, caseSensitive=True):
    if not caseSensitive:
        a = a.lower()
        b = b.lower()

    return SequenceMatcher(None, a, b).ratio()


def toEast(lngSrc, lngDst):
    distance = lngDst - lngSrc
    if distance < 0:
        distance += 360

    return distance < 180
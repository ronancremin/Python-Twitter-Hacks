import urllib2
import json
import base64
import sys
import argparse


def main(args):
    site = args.url[0]
    if not site.startswith('http://'):
        site = 'http://' + site

    if args.desktop:
        api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&url="
    else:
        api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=mobile&url="

    api += urllib2.quote(site)

    try:
        site_data = json.load(urllib2.urlopen(api))
    except urllib2.URLError:
        print "Unable to retreive data"
        sys.exit()

    try:
        screenshot_encoded =  site_data['screenshot']['data']
    except ValueError:
        print "Invalid JSON encountered."
        sys.exit()	

    #	Google has a weird way of encoding the Base64 data
    screenshot_encoded = screenshot_encoded.replace("_", "/")
    screenshot_encoded = screenshot_encoded.replace("-", "+")

    #	Decode the Base64 data
    screenshot_decoded = base64.b64decode(screenshot_encoded)

    #	Save the file
    with open('screenshot.jpg', 'w') as file_:
        file_.write(screenshot_decoded)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save a screenshot of a site using Google PageSpeed service.')
    parser.add_argument('--url', '-u', nargs=1, required=True, help='The URL to create the screenshot from')
    parser.add_argument('--desktop', default=False, action='store_true', required=False, help='Get screenshot of desktop experience')
    main(parser.parse_args())

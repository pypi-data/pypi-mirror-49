import requests

from radio.core.log import logger


def rec(fname, url):
    resp = requests.get(url, stream=True)
    with open(fname, "wb+") as audio_file:
        try:
            for block in resp.iter_content(512):
                audio_file.write(block)
        except Exception as exc:
            logger.info(exc)


def main():
    fname = "local.mp3"
    url = "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p"
    rec(fname, url)


if __name__ == "__main__":
    main()

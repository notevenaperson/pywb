r"""

# warc.gz
>>> print_cdx_index('example.warc.gz')
 CDX N b a m s k r M S V g
com,example)/?example=1 20140103030321 http://example.com?example=1 text/html 200 B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 1043 333 example.warc.gz
com,example)/?example=1 20140103030341 http://example.com?example=1 warc/revisit - B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 553 1864 example.warc.gz
org,iana)/domains/example 20140128051539 http://www.iana.org/domains/example text/html 302 JZ622UA23G5ZU6Y3XAKH4LINONUEICEG - - 577 2907 example.warc.gz

# warc
>>> print_cdx_index('example.warc')
 CDX N b a m s k r M S V g
com,example)/?example=1 20140103030321 http://example.com?example=1 text/html 200 B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 1987 460 example.warc
com,example)/?example=1 20140103030341 http://example.com?example=1 warc/revisit - B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 896 3161 example.warc
org,iana)/domains/example 20140128051539 http://www.iana.org/domains/example text/html 302 JZ622UA23G5ZU6Y3XAKH4LINONUEICEG - - 854 4771 example.warc

# arc.gz
>>> print_cdx_index('example.arc.gz')
 CDX N b a m s k r M S V g
com,example)/ 20140216050221 http://example.com/ text/html 200 B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 856 171 example.arc.gz

# arc
>>> print_cdx_index('example.arc')
 CDX N b a m s k r M S V g
com,example)/ 20140216050221 http://example.com/ text/html 200 B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 1656 151 example.arc

# wget warc (w/ metadata)
>>> print_cdx_index('example-wget-1-14.warc.gz')
 CDX N b a m s k r M S V g
com,example)/ 20140216012908 http://example.com/ text/html 200 B2LTWWPUOYAH7UIPQ7ZUPQ4VMBSVC36A - - 1151 792 example-wget-1-14.warc.gz
metadata)/gnu.org/software/wget/warc/manifest.txt 20140216012908 metadata://gnu.org/software/wget/warc/MANIFEST.txt text/plain 200 SWUF4CK2XMZSOKSA7SDT7M7NUGWH2TRE - - 315 1943 example-wget-1-14.warc.gz
metadata)/gnu.org/software/wget/warc/wget_arguments.txt 20140216012908 metadata://gnu.org/software/wget/warc/wget_arguments.txt text/plain 200 UCXDCGORD6K4RJT5NUQGKE2PKEG4ZZD6 - - 340 2258 example-wget-1-14.warc.gz
metadata)/gnu.org/software/wget/warc/wget.log 20140216012908 metadata://gnu.org/software/wget/warc/wget.log text/plain 200 2ULE2LD5UOWDXGACCT624TU5BVKACRQ4 - - 599 2598 example-wget-1-14.warc.gz

# bad arcs -- test error edge cases
>>> print_cdx_index('bad.arc')
 CDX N b a m s k r M S V g
com,example)/ 20140401000000 http://example.com/ text/html 204 3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ - - 67 134 bad.arc
com,example)/ 20140401000000 http://example.com/ text/html 204 3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ - - 68 202 bad.arc
"""

from pywb import get_test_dir
from pywb.warc.archiveindexer import ArchiveIndexer

from io import BytesIO
import sys

TEST_CDX_DIR = get_test_dir() + 'cdx/'
TEST_WARC_DIR = get_test_dir() + 'warcs/'

def read_fully(cdx):
    with open(TEST_CDX_DIR + cdx) as fh:
        curr = BytesIO()
        while True:
            b = fh.read()
            if not b:
                break
            curr.write(b)
    return curr.getvalue()

def cdx_index(warc, sort=False):
    buff = BytesIO()
    with open(TEST_WARC_DIR + warc) as fh:
        indexer = ArchiveIndexer(fh, warc,
                                 out=buff,
                                 sort=sort)

        indexer.make_index()

    return buff.getvalue()

def print_cdx_index(warc, sort=False):
    sys.stdout.write(cdx_index(warc, sort))

def assert_cdx_match(cdx, warc, sort=False):
    assert read_fully(cdx) == cdx_index(warc, sort)

def test_sorted_warc_gz():
    assert_cdx_match('example.cdx', 'example.warc.gz', sort=True)
    assert_cdx_match('dupes.cdx', 'dupes.warc.gz', sort=True)
    assert_cdx_match('iana.cdx', 'iana.warc.gz', sort=True)
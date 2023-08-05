# py-emailprotections
[![Build Status](https://travis-ci.com/poipoii/pyemailprotectionslib.svg?branch=master)](https://travis-ci.com/poipoii/pyemailprotectionslib)
[![Coverage Status](https://coveralls.io/repos/github/poipoii/pyemailprotectionslib/badge.svg?branch=master)](https://coveralls.io/github/poipoii/pyemailprotectionslib?branch=master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-emailprotections.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-emailprotections.svg)
[![PyPI version](https://badge.fury.io/py/py-emailprotections.svg)](https://badge.fury.io/py/py-emailprotections)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py-emailprotections.svg)

This is a simple library designed to assist people with finding email protections.

## Installing

``` python
pip install py-emailprotections
```

## Usage

The simplest use of this library is to find and process SPF and DMARC records for domains. This is easiest with the `SpfRecord.from_domain(domain)` and `DmarcRecord.from_domain(domain)` factory methods.

Example:

    import emailprotectionslib.spf as spf
    import emailprotectionslib.dmarc as dmarc
    
    spf_record = spf.SpfRecord.from_domain("google.com")
    dmarc_record = dmarc.DmarcRecord.from_domain("google.com")
    
    print spf_record.record
    print dmarc_record.policy
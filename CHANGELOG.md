# Changelog

<!--next-version-placeholder-->

## v0.5.0 (2023-01-25)
### Feature
* Drop 3.8 support in favour of >3.10 ([`0a52772`](https://github.com/iwpnd/flashgeotext/commit/0a527729c7c3c54582236703f9be1de6cbdb4645))

### Documentation
* Update actions badge ([`a83af01`](https://github.com/iwpnd/flashgeotext/commit/a83af01dd04de2b278f1d13680a33980e0e5a01d))
* Update poetry action ([`b0de497`](https://github.com/iwpnd/flashgeotext/commit/b0de497af354d02ed8cd230eec994fab36936689))
* Fix docs workflow ([`fc64e76`](https://github.com/iwpnd/flashgeotext/commit/fc64e764f865f1600661ce647e7b577fa2d2ea60))

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2022-01-31
### Fix
- Parse extract when span_info is false ([`d497b57`](https://github.com/iwpnd/flashgeotext/commit/d497b5797d81e669712c9a73500fbb16acfc5bd2))

## [0.3.0] - 2021-02-29
### Added
- removed flit. now using poetry
- added optional case_sensitive option to look for lower case city names
## [0.2.0] - 2020-03-02
### Added
- `script` argument to LookupData to specify from what script the characters in the lookup will be, see [usage](https://flashgeotext.iwpnd.pw/usage), this will make sure that flashgeotext works with different character sets accordingly


## [0.1.0] - 2020-02-25
### Added
- initial release of [flashgeotext](https://flashgeotext.iwpnd.pw)

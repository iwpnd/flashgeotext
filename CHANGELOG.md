# Changelog
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

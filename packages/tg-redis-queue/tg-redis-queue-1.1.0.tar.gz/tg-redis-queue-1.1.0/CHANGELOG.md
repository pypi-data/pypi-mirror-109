# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2020-06-10

### Added

- Asynchronous redis queue implementation
- Ability to override the serialization logic in a subclass (`dump_data` and `load_data`) to 
  allow using some alternative to json
- This changelog

### Changed

- Package no longer depends on redis directly (since asynchronous version uses aioredis), to 
  install with proper dependencies use `synchronous` or `asyncio` extra requirements (see [README](README.md))
- Due to different implementations requiring different packages, is no longer possible to import directly from 
  tg_redis_queue: `from tg_redis_queue.sync_redis_queue import RedisObjectQueue` instead of 
  `from tg_redis_queue import RedisObjectQueue`

## [1.0.0] - 2020-05-28

### Added

- Synchronous redis queue implementation, extracted from existing non-library code
- Tests, and pipeline configuration for running the tests in CI
- Code quality checks and formatters (isort, black, prospector)

[1.1.0]: https://gitlab.com/thorgate-public/tg-redis-queue/-/tags/v1.1.0
[1.0.0]: https://gitlab.com/thorgate-public/tg-redis-queue/-/tags/v1.0.0

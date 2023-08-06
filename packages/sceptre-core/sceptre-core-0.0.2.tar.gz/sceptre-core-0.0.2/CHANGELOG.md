# CHANGELOG

Categories: Added, Removed, Changed, Fixed, Nonfunctional, Deprecated

## Unreleased

### Fixed

- `sceptre_user_data` resolver infinite recursion

## 0.0.1 (2019.07.16)

### Added

- SceptreContext to Hooks and Resolvers

### Removed

- Sceptre CLI from core repository
- Built in Hooks and Resolvers

### Changed

- Treat all Hooks and Resolvers equally when loading
- Load plugins at config reader

### Fixed

- Remove redundant code after raising AttributeError
- Debugging output for StackGraph

### Nonfunctional

- Move CircleCi Dockerfile to own repo
- Update sonar properties
- Separate CLI from core repository
- Change example url to sceptre homepage
- Update CONTRIBUTING docs for test coverage level
- Update CircleCI test results output dir
- Set test coverage fail level to 92%
- Add exclusions to sonarqube
- Add sonar badges
- Add sonar-project properties file.

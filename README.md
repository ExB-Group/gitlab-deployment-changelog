# Gitlab Deployment Changelog

- set gitlab access token `PAT` (https://gitlab.com/-/profile/personal_access_tokens)  and `WEBHOOK_URL` for slack

## How to use locally

- checkout
- `pdm install`
- Make sure you have `PROJECT_ID` properly set
- `pdm run changelog [environment]` environment defaults to `production/the_exb` 

## Pipelien usage

- set PAT
- call it with the environement name as argument
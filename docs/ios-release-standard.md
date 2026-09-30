# WorksBien iOS Release Standard

This template keeps app-specific release configuration in one file: `APP_IDENTITY.json`.

Do not hand-edit these generated files unless you are also changing the generator:

- `.github/testflight-app-map.json`
- `docs/app-store-listing-manifest.json`

## State model

| Field | Meaning |
| --- | --- |
| `release_state: draft` | The app is wired but cannot upload to TestFlight. |
| `release_state: ready` | The TestFlight reusable workflow may build and upload. |
| `listing.mode: draft` | Listing upload can dry-run/validate but must not submit for review. |
| `listing.mode: submission` | Final App Review submission is allowed only with explicit workflow confirmation. |

## Required app changes

Before switching to `ready`, replace all placeholder values in `APP_IDENTITY.json`:

- `repository`
- `app.bundle_id`
- `app.asc_app_id`
- `release.beta_group_id`
- `xcode.container`
- `xcode.scheme`
- listing URLs and locale text

Then run:

```bash
python3 scripts/materialize_release_contract.py
python3 scripts/materialize_release_contract.py --check
```

The central reusable workflows will fail closed if the repository, bundle ID, App Store Connect app ID, credentials, or listing manifest disagree.

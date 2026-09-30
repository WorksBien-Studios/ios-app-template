# WorksBien iOS App Template

This repository is the starter contract for WorksBien iOS apps.

It wires a new app into the organisation-level release automation in `WorksBien-Studios/.github`:

- TestFlight upload through the central reusable workflow.
- App Store listing upload through the central reusable workflow.
- A single canonical `APP_IDENTITY.json` file for bundle IDs, App Store Connect IDs, scheme, workspace, and listing metadata.
- A generated `.github/testflight-app-map.json` used by CI.
- A generated `docs/app-store-listing-manifest.json` used by the listing lane.
- A fail-closed sync check so stale release metadata cannot silently ship.

## New app setup

1. Create a new repository from this template.
2. Add your Xcode project or workspace.
3. Edit `APP_IDENTITY.json`.
4. Run:

   ```bash
   python3 scripts/materialize_release_contract.py
   ```

5. Commit the generated `.github/testflight-app-map.json` and `docs/app-store-listing-manifest.json`.
6. Push to `main` and use the GitHub Actions workflows.

## Release contract

The central WorksBien workflows expect these organisation secrets and variables to exist:

- `ASC_ISSUER_ID`
- `ASC_KEY_ID`
- `ASC_PRIVATE_KEY`
- `ASC_EXPECTED_ISSUER_ID`
- `ASC_EXPECTED_KEY_ID`

The template deliberately starts in draft mode with placeholder IDs. Real upload lanes should not be treated as production-ready until `APP_IDENTITY.json` is completed for the app.

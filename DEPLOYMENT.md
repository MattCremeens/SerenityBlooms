# Serenity Blooms — Cloud Run deployment

This package is the deployable FastAPI site. It deliberately excludes the local
virtual environment, git history, and `.env` credentials. Run these commands
on your own Ubuntu machine in this directory.

## First-time setup

Confirm that `serenity-blooms` is the actual **project ID** (not just its name).
Verify that billing is linked to the project.

```bash
gcloud config set project serenity-blooms
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com iam.googleapis.com
```

Create a dedicated service identity and grant access only to its SMTP secret:

```bash
gcloud iam service-accounts create serenity-blooms-web \
  --display-name="Serenity Blooms website"

gcloud secrets create serenity-blooms-smtp-password \
  --replication-policy=automatic
```

Enter the Gmail **app password**, not your regular Google account password.
The terminal hides input. Do not paste it into this document, source files,
or a `gcloud --set-env-vars` command.

```bash
read -rsp 'Gmail app password: ' SB_SMTP_PASSWORD
printf '\n'
printf '%s' "$SB_SMTP_PASSWORD" | gcloud secrets versions add \
  serenity-blooms-smtp-password --data-file=-
unset SB_SMTP_PASSWORD
```

```bash
gcloud secrets add-iam-policy-binding serenity-blooms-smtp-password \
  --member="serviceAccount:serenity-blooms-web@serenity-blooms.iam.gserviceaccount.com" \
  --role=roles/secretmanager.secretAccessor
```

## Deploy and verify

```bash
gcloud run deploy serenity-blooms-web \
  --source . \
  --region us-central1 \
  --service-account serenity-blooms-web@serenity-blooms.iam.gserviceaccount.com \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --memory 512Mi \
  --set-env-vars SMTP_HOST=smtp.gmail.com,SMTP_PORT=587,SMTP_USER=mattandheathercremeens@gmail.com,ORDER_EMAIL_TO=mattandheathercremeens@gmail.com \
  --set-secrets SMTP_PASSWORD=serenity-blooms-smtp-password:1
```

`--source .` uses the supplied Dockerfile. The server listens on Cloud Run's
`PORT` variable. First deployment may prompt you to create an Artifact Registry
repository or grant build permissions.

1. Visit the `https://...run.app` URL returned by deployment.
2. Check the homepage, galleries, and shop pages.
3. Submit a **test inquiry** and confirm it reaches the Gmail inbox.
4. Test an order with Heather (do not make an actual Venmo payment during testing).
   The Venmo link now appears only after the server successfully emails the order.
5. Set a billing budget alert in Google Cloud. Budget alerts are not spending caps.

If an email fails, inspect Cloud Run logs. The application deliberately displays
a generic error instead of disclosing SMTP internals.

## Domain and launch

After the temporary Cloud Run URL works, connect both
`serenitybloomsflowerco.com` and `www.serenitybloomsflowerco.com` via Firebase
Hosting or another supported HTTPS front end. Follow the exact DNS records
shown by the hosting wizard in the Cloud DNS managed zone; don't guess A or CNAME
values. Keep one URL canonical and redirect the other.

## Operational notes

- The website uses the `America/Chicago` timezone for form dates.
- Form emails contain visitors' personal details. Limit who can view service
  logs and the mailbox.
- The hidden form honeypot remains, but it is **not a complete spam defense**.
  Before advertising widely, add a managed bot challenge or a durable,
  edge-enforced rate limit. Instance-local counters are not reliable on
  autoscaled Cloud Run.
- Domain and Secret Manager charges may apply even when Cloud Run scales to zero.
- Keep `SMTP_PASSWORD` in Secret Manager, never in the image, environment
  variables entered as plaintext, or committed files.

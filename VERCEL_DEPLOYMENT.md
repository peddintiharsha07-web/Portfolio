# Deploy this Django portfolio to Vercel + Neon + Cloudinary

This project is configured to use:
- Vercel for the Django app and collected static assets.
- Neon PostgreSQL when `DATABASE_URL` is set (SQLite remains the local default).
- Cloudinary for uploaded media (profile images, project images, certificates, gallery images, and CV files) when `CLOUDINARY_URL` is set.

## Before pushing to GitHub

1. Create and activate a virtual environment.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Generate the app's initial migration (the supplied ZIP did not contain one):
   `python manage.py makemigrations portfolio`
4. Apply local migrations: `python manage.py migrate`.
5. Check the project: `python manage.py check`.
6. Commit the generated `portfolio/migrations/0001_initial.py` file to GitHub. Do not ignore or omit migrations.

If your local SQLite database already has old tables from a previous no-migrations setup, back it up before applying the new initial migration. A fresh database is the simplest clean setup.

## Create the external services

### Neon

Create a PostgreSQL project/database in Neon. Copy the connection string from the Neon Connect dialog. For the deployed app, use the pooled connection string where available. Keep the connection string private.

### Cloudinary

Create a Cloudinary account and copy the `CLOUDINARY_URL` value from its API environment details. It contains credentials; never commit it to GitHub or paste it into public code.

## GitHub

Push the project root (the folder containing `manage.py`, `config/`, and `portfolio/`) to a GitHub repository. Ensure `.env`, `db.sqlite3`, `media/`, and virtual-environment folders are not committed.

## Vercel project settings

Import the GitHub repository into Vercel. Set the Root Directory to the directory containing `manage.py` (if you pushed the outer extracted folder, this will be `portfolio_project`; if you pushed the contents of that folder, it will be `.`).

Vercel's current Django integration detects Django projects from `manage.py`, configures routing, and serves collected static files through its CDN. Do not add an old `/api` shim or a custom `vercel.json` unless Vercel's current build output explicitly asks for one. See the official [zero-configuration Django support announcement](https://vercel.com/changelog/zero-configuration-django-support).

## Vercel environment variables

Add these for Production (and Preview only if you want preview deployments connected to separate test services):

- `DJANGO_DEBUG` = `0`
- `DJANGO_SECRET_KEY` = a newly generated, private Django secret key
- `DJANGO_ALLOWED_HOSTS` = `.vercel.app,your-custom-domain.example` (replace with your actual domain; do not include `https://`)
- `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://your-project.vercel.app,https://your-custom-domain.example` (only include domains you actually use)
- `DATABASE_URL` = Neon PostgreSQL connection string
- `CLOUDINARY_URL` = Cloudinary URL from its dashboard

Do not put quotes around the values in Vercel's environment variable editor. Never share secret values in screenshots or chat.

## Apply migrations to Neon

Generate and commit migration files first. Then, from your own computer, temporarily set `DATABASE_URL` to the Neon connection string in a terminal and run:

PowerShell:

```powershell
$env:DATABASE_URL = "YOUR_NEON_CONNECTION_STRING"
python manage.py migrate
```

Use the direct Neon connection string for this one-time migration if the pooled connection has migration/session limitations. Then remove the variable from that terminal:

```powershell
Remove-Item Env:DATABASE_URL
```

The app uses the `DATABASE_URL` configured in Vercel at runtime. Do not run `makemigrations` against production; generate migrations locally, review them, and commit them.

## Deploy and verify

Deploy from Vercel. Check the deployment logs if the build fails. Verify:

- `/` loads the portfolio.
- `/admin/` loads and accepts the superuser credentials.
- Create a test project and upload a test image in Admin; confirm the image URL is served from Cloudinary.
- Check project detail pages and static CSS/JS.
- Check the site at 320px, 375px, 430px, tablet width, and desktop width; open and close the mobile menu and test the project thumbnail navigation.

Create a production admin user against Neon from your computer by setting `DATABASE_URL` to the Neon connection string and running:

```powershell
python manage.py createsuperuser
```

## Important notes

- Vercel's filesystem is not persistent for user uploads. Cloudinary is configured as the default file storage only when `CLOUDINARY_URL` is present.
- Do not rely on SQLite on Vercel for persistent data. Set `DATABASE_URL` before production deployment.
- Preview deployments should ideally use a separate Neon branch/database so test migrations and test content do not affect production.
- The project was prepared from the uploaded source, but a live Vercel deployment and external Neon/Cloudinary credentials cannot be tested from this workspace.

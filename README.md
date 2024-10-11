## Chikorita Eatclean ERP Backend

Chikorita ERP app is a Frappe app that provides a web interface for restaurant's owners and staffs to manage operation.

Backend infomation:

- Built with Frappe Framework
- Code: Python
- DB: MariaDB

### Dev Setup:

#### Setting up Docker Container

Clone `frappe-docker`:

`git clone https://github.com/frappe/frappe_docker.git`

```
cd frappe_docker
cp -R devcontainer-example .devcontainer
cp -R development/vscode-example development/.vscode
```

Open VSCode `code .` and choose to reopen in container. The Docker container will be built.

#### Setting up Frappe Bench

`bench init --skip-redis-config-generation --frappe-branch version-15 frappe-bench`

`cd frappe-bench`

```
bench set-config -g db_host mariadb
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379
```

#### Creating a new site

`bench new-site development.localhost`

Change to development mode (only for development):

```
bench --site development.localhost set-config developer_mode 1
bench --site development.localhost clear-cache
bench use development.localhost
```

_Turn off CSRF checking_: In `site.config`:

`bench --site development.localhost set-config ignore_csrf 1`

Or add `"ignore_csrf": 1` to `sites/common_site_config.json`

Allow CORS: add `"allow_cors": "*"` in `sites/common_site_config.json`

Start the development server:

`bench start`

Go to `http://development.localhost:8000`.

#### Installing Chikorita app

```
bench get-app https://github.com/alannguyen127/emfresh-erp
bench --site development.localhost install-app emfresh_erp
```

```
bench update --requirements --patch --build
```

**Site commands**

- List of commands: `bench --site development.localhost --help`
- Python console: `bench --site development.localhost console`
- MariaDB console: `bench --site development.localhost mariadb`

#### Commit changes

Go to `frappe-bench/apps/emfresh_erp` and commit changes.

#### Setup Bruno

The app use Bruno to manage API requests. To install bruno app:

`brew install bruno`

Or go to [Bruno](https://www.usebruno.com/downloads)

Open the collection stored in `api_docs` folder.

Rename `api_docs/environments/development.bru_example` to `api_docs/environments/development.bru`.

Go to Frappe Admin Page -> Users -> Choose a user -> Settings -> API Key -> Generate API Key.

Copy API Key and API Secret to `development.bru`.

### License

apache-2.0

## Accessing the Project on PythonAnywhere

You can manage and update the website directly via PythonAnywhere:
[PythonAnywhere – teamsuman](https://www.pythonanywhere.com/user/teamsuman/)

### Core Project Files

The main Django project files are located here:
[teamsuman core files](https://www.pythonanywhere.com/user/teamsuman/files/home/teamsuman)

The folder structure follows the standard Django layout:

```text
.
├── home
│   └── templates
│       └── home
├── media
│   └── images
├── pharmocast
│   └── assets
│       ├── delg_models
│       ├── pka_models
│       └── solu_models
├── scripts
├── static
│   ├── css
│   ├── img
│   ├── js
│   └── pharmocast
│       ├── css
│       ├── js
│       └── images
├── staticfiles
│   ├── css
│   ├── img
│   ├── js
│   └── pharmocast
│       ├── css
│       ├── js
│       └── images
└── teamsuman
    └── static
        ├── css
        ├── img
        ├── js
        └── pharmocast
            ├── css
            ├── js
            └── images
```

---

### HTML Templates

All HTML template files are located here:
[Templates folder](https://www.pythonanywhere.com/user/teamsuman/files/home/teamsuman/website/home/templates/home)

Changes made to these files will **immediately reflect on the live site**.

The templates are organized by page:

```text
home
├── templates
│   └── home
│       ├── 404.html
│       ├── base.html
│       ├── contact.html
│       ├── email.html
│       ├── footer.html
│       ├── gallery.html
│       ├── header.html
│       ├── home.html
│       ├── news.html
│       ├── pharmocast.html
│       ├── position.html
│       ├── publication.html
│       ├── research_detail.html
│       ├── research.html
│       ├── softwares.html
│       ├── team.html
│       └── test.html
├── tests.py
├── urls.py
└── views.py
```

**Notes:**

* `base.html` is the main template used by all pages.
* `header.html` and `footer.html` are included in `base.html`; modifying them will globally affect all pages.
* Page-specific templates (e.g., `home.html`, `contact.html`) extend `base.html`.

---

## Accessing Files Locally

You can test and modify the project locally before updating the remote site. To retrieve the files from PythonAnywhere, use `rsync`:

```bash
rsync -avzhe ssh teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website .
```

This will copy the project files to your local machine after authentication.

---

### Installing Dependencies

Install the required Python packages using `pip`:

```bash
pip install django
pip install django-admin-sortable2
pip install django-summernote
pip install joblib
pip install jsonfield
```
---

### Running the Development Server

1. Ensure `DEBUG = True` in `settings.py`.
2. Start the Django server:

```bash
python manage.py runserver
```

This will run the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).
Changes made locally will be immediately reflected in your browser.

---

### Updating the Remote Server

After making changes locally, export them to PythonAnywhere using `rsync`:

```bash
rsync -avzhe ssh ./* teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website/ --exclude "*settings.py"
```

> ⚠️ Note: `settings.py` is excluded to avoid overwriting your remote configuration.

---

## Admin-Specific Changes

Dynamic content on the site can be modified via the Django admin interface. Changes made through the admin are **permanent**.

* **Locally:** Access the admin at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* **On the live site:** Access at [http://teamsuman.org/admin](http://teamsuman.org/admin)

Log in with your admin credentials and make the necessary updates. All changes will be reflected immediately on the site.

---

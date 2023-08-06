# django-cra-helper

## Introduction

**django-cra-helper** is the missing link between **Django** and **create-react-app**. By adding this to your Django project, you can almost effortlessly inject your React components into your Django templates and initialize component props via Django context variables.

The ultimate goal of this package is to integrate these two projects with minimal changes to workflows that are typically used with either during development. From `npm start` to `python manage.py collectstatic`, your commands should work as expected so you can forget about implementation and get back to development!

> Note: For the purposes of this README, the abbreviation **CRA** will be used to refer to **create-react-app**.

## Installation

This package is available for installation via `pip`:

```sh
pip install django-cra-helper
```

## Setup & Configuration

Once **django-cra-helper** is installed, `cra_helper` will need to be added to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cra_helper',
    'django.contrib.staticfiles',
]
```

> Note: `cra_helper` **must** be placed above `django.contrib.staticfiles` in the list!

Add `cra_helper.context_processors.static` to `TEMPLATES['OPTIONS']['context_processors']`:

```python
TEMPLATES = [
    {
        # ...snip...
        'OPTIONS': {
            'context_processors': [
                # ...snip...
                'cra_helper.context_processors.static',
            ],
        },
    },
]
```

Additionally, the following `STATICFILES_FINDERS` list will also need to be added to `settings.py`:

```python
STATICFILES_FINDERS = [
    # Django defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # A finder to pull in asset-manifest.json
    'cra_helper.finders.CRAManifestFinder',
]
```

The last necessary setting is the name of the folder containing the CRA project files, relative to the base directory of the Django **project** (the folder containing `manage.py`):

```python
CRA_APP_NAME = 'cra-app'
```

If for some reason the CRA liveserver does *not* serve on localhost or port 3000, the following settings can be added to `settings.py` to specify its actual host and port:

```python
CRA_HOST = '0.0.0.0'
CRA_PORT = 9999
```

> Note: if you don't set a value for `CRA_HOST` then **django-cra-helper will default to host `'localhost'`**

> Note: if you don't set a value for `CRA_PORT` then **django-cra-helper** will default to port `3000`.

Finally, run CRA's `npm run build` command once to generate a `build/` directory. **django-cra-helper** requires the `build/asset-manifest.json` file contained within to help load non-JS and non-CSS assets that might be used in any React components. This command should be re-run any time a new non-JS or non-CSS asset is added to the project.

Once everything is in place, **django-cra-helper** will make the following possible:

### Access React components in real-time from the CRA liveserver

If the CRA project's liveserver is started via `npm start` prior to starting Django's development server via `python manage.py runserver`, code changes in the React codebase will be updated immediately within Django views as well.

When the CRA liveserver is running, **django-cra-helper** adds a `bundle_js` template variable that can be inserted into the Django view's template to load the liveserver's intermediate `bundle.js` file containing all of the current JS and CSS. This file is recompiled on-the-fly by the liveserver whenever edits are made to the React code. This file can be added to a Django template as follows:

```html
{% if bundle_js %}<script type="text/javascript" src="{{ bundle_js }}"></script>{% endif %}
```
> Note: Don't use the `static` template tag here! This file needs to be loaded from the CRA liveserver instead.

### Access React components in production

**django-cra-helper** also takes care of ensuring that Django's `collectstatic` command pulls in production-ready bundles built by CRA's `npm run build` command.

First, prepare React files for production with the typical CRA `npm` build command:

```sh
npm run build
```

This will output bundled, minified JavaScript and CSS, and assets to the `/build/` folder within the CRA project folder.

Once this command is complete, run the following Django command to gather static files, including the compiled React assets:

```sh
python manage.py collectstatic --no-input
```

React assets will be included with the other static assets in the `settings.STATIC_ROOT` directory, to be served as is usual in a Django production environment. An `asset-manifest.json` file will also get pulled in. The contents of this CRA-generated file are required by **django-cra-helper** to help reference React files that have had a unique hash added to their filenames during the build process.

Similar to the `bundle_js` template variable mentioned earlier, **django-cra-helper** includes numerous other template variables when the CRA liveserver is _not_ running. The two most important ones are `main_js` and `main_css`. These can be injected into the page via a typical call to `{% static %}` in the template:

```html
{% if main_css %}<link href="{% static main_css %}" rel="stylesheet">{% endif %}
```
```html
{% if main_js %}<script type="text/javascript" src="{% static main_js %}"></script>{% endif %}

```

Other assets bundled by CRA, including image assets, can be accessed in templates by substituting `_` for `/` and `.` (period). **django-cra-helper** adds every entry in `asset-manifest.json` to the base context, using these substitution rules to accomodate Django's `static` tag.

For example,  a **logo.svg** file in the CRA project can be included in a Django template as follows:

```html
<!-- This file is located at `/build/static/media/logo.svg` -->
<img src="{% static static_media_logo_svg %}" height="40" width="40">
```
> Note: This is optional! Static assets can still be included in the Django app's `/static/` directory and loaded as usual. The special substitution mentioned above is only needed when reusing React assets outside of specific components.

## Accessing React Components via Django template contexts

The CRA project will need to undergo a small bit of re-archiceture to prepare it to accept input values from Django when Django serves a view. The following is an example of how a couple of small tweaks to a CRA project's `src/index.js` file will establish a simple API for Django to communicate with the bundled React codebase:

```js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

/**
 * Maintain a simple map of React components to make it easier
 * for Django to reference individual components
 */
const pages = {
  App,
}

/**
 * If Django hasn't injected these properties into the HTML
 * template that's loading this script then we're viewing it
 * via the create-react-app liveserver
 */
window.component = window.component || 'App';
window.props = window.props || { env: 'create-react-app' };
window.reactRoot = window.reactRoot || document.getElementById('root');

/**
 * React the component as usual
 */
ReactDOM.render(
  React.createElement(pages[window.component], window.props),
  window.reactRoot,
);
```

Basically, `index.js` is updated to read values set to `window.component`, `window.props`, and `window.reactRoot` and use these to render a component. Each of these three "inputs" will allow Django to easily specify which component to initialize on a per-view basis:

* `window.component`: A **string** that points to a Component entry in `pages`
* `window.props`: An **Object** containing props to get passed into the Component
* `window.reactRoot`: an **instance** of `document.getElementById`

> Note: Settings these values is optional. The defaults specified in the template above enable components to render as expected when viewed from the CRA liveserver.

Now that the "API" is in place, Django Views can include values for these inputs via the context they pass to their template:

```python
def index(request):
    context = {
        'component': 'App',
        'props': {
            'env': 'Django',
        },
    }
    return render(request, 'index.html', context)
```

Below is the Django app's `index.html` template that will render the context:

```html
{% load static %}
{% load cra_helper_tags %}
<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    {% if main_css %}<link href="{% static main_css %}" rel="stylesheet">{% endif %}
    <title>Django + React Project</title>
  </head>

  <body>
    <div id="react">Loading...</div>

    <script>
      window.component = '{{ component }}';
      window.props = {{ props | json }};
      window.reactRoot = document.getElementById('react');
    </script>
    {% if bundle_js %}<script type="text/javascript" src="{{ bundle_js }}"></script>{% endif %}
    {% if main_js %}<script type="text/javascript" src="{% static main_js %}"></script>{% endif %}
  </body>

</html>
```
The context's `component` and `props` are bound to `window.component` and `window.props` respectively.

Note the use of the `json` filter when setting `windows.props`! `{% load cra_helper_tags %}` provides this filter as a way to easily sanitize and convert a Python `dict` to a Javascript `Object`. The View context prepared above thus renders to the following typical Javascript Object:

```js
// This is what is returned in the rendered HTML
window.props = {"env": "Django"};
```
Finally, `window.reactRoot` specifies the container element that the React component should be rendered into. Setting a value for this is only required if the container's `id` is *not* **"root"** (the same ID assigned to the container `<div>` in the CRA project's `index.html`.)

## The Payoff Revealed

When all is said and done, React components should now render and be viewable in both the CRA liveserver and when served via Django. Here's an example of a slightly-modified CRA `App` component displayed in Django (left) and CRA (right):

![Comparison Shot](./side_by_side.png)

## TODO

* Figure out how to get Django to auto-reload when the CRA liveserver reloads after code is updated.

Taiga Contrib Sendinblue Subscription
=====================================

![Kaleidos Project](http://kaleidos.net/static/img/badge.png "Kaleidos Project")
[![Managed with Taiga.io](https://tree.taiga.io/support/images/taiga-badge-gh.png)](https://taiga.io "Managed with Taiga.io")

Plugin to subscribe and unsubscribe users to the newsletter and user list in Sendinblue


Installation
------------

### Configure Sendinblue

In Sendinblue you have to add two custom attributes to your contacts.

1 - Open Sendinblue.
2 - Go to `Settings` > `Attributes & CRM`
3 - Add the attributes:
    - Remove 'SURNAME' and 'NAME'
    - Add 'FULL_NAME' and 'USERNAME' (text type both of them).


### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-sendinblue-subscription` with:

```bash
  pip install -e "git+https://github.com/taigaio/taiga-contrib-sendinblue-subscription.git@stable#egg=taiga-contrib-sendinblue-subscription&subdirectory=back"
```

Then modify in `taiga-back` your `settings/local.py` and include this line:

```python
  SENDINBLUE_NEWSLETTER_LIST_ID = "my-newsletter-list-id"
  SENDINBLUE_TAIGA_USERS_LIST_ID = "my-taiga-user-list-id"
  SENDINBLUE_API_KEY = "XXXXXXXXXXXXXXXXX"

  INSTALLED_APPS += ["taiga_contrib_sendinblue_subscription"]
```


#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-sendinblue-subscription` compiled code (you need subversion in your system):

```bash
  cd dist/
  mkdir -p plugins
  cd plugins
  svn export "https://github.com/taigaio/taiga-contrib-sendinblue-subscription/branches/stable/front/dist" "sendinblue-subscription"
```

Include in your `dist/conf.json` in the `contribPlugins` list the value `"/plugins/sendinblue-subscription/sendinblue-subscription.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/sendinblue-subscription/sendinblue-subscription.json"
    ]
...
```


### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-sendinblue-subscription/back
  workon taiga
  pip install -e .
```

Then modify in `taiga-back` your `settings/local.py` and include this line:

```python
  MAILCHIMP_NEWSLETTER_ID = "my-newsletter"
  MAILCHIMP_API_KEY = "XXXXXXXXXXXXXXXXX"

  INSTALLED_APPS += ["taiga_contrib_sendinblue_subscription"]
```


#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-sendinblue-subscription/front/dist sendinblue-subscription
```

Include in your `dist/conf.json` in the `contribPlugins` list the value `"/plugins/sendinblue-subscription/sendinblue-subscription.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/sendinblue-subscription/sendinblue-subscription.json"
    ]
...
```

In the plugin source dir `taiga-contrib-sendinblue-subscription` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.

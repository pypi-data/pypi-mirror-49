graphene-sentry
-------

This package is based on 
[graphene-django-sentry](https://pypi.org/project/graphene-django-sentry/)
([Github page](https://github.com/phalt/graphene-django-sentry))
package.

Main focus of package was to fix issue with sentry reporting with 
[graphene_django](https://github.com/graphql-python/graphene-django) package.

I think this package can be extended to handle nore cases.

Survey is needed if you faced similar problem with sentry report with other 
frameworks or graphene implementations let me know via issues.

*Capture Sentry exceptions in Graphene views*

When using [Graphene Django](https://github.com/graphql-python/graphene-django),
you sometimes want to raise exceptions and capture them in the API.

However, Graphene Django eats the raised exceptions and you won't see it
in Sentry! 😭

This package thinly wraps the normal GraphQLView with a handler that
deals with Sentry errors properly.

So the results:

1.  Sentry will show the true exceptions.
2.  Graphene will continue to work like normal.

Works with:

-   Python 3.6+
-   Django 2.1+
-   graphene-django 2.2+

![image](https://img.shields.io/pypi/v/graphene-sentry.svg%0A%20%20%20%20%20:target:%20https://pypi.org/project/graphene-sentry/)

![image](https://img.shields.io/pypi/pyversions/graphene_sentry.svg%0A%20%20%20%20%20:target:%20https://pypi.org/project/graphene_sentry/)

![image](https://img.shields.io/pypi/l/graphene-sentry.svg%0A%20%20%20%20%20:target:%20https://pypi.org/project/graphene-sentry/)

![image](https://img.shields.io/pypi/status/graphene_sentry.svg%0A%20%20%20%20%20:target:%20https://pypi.org/project/graphene_sentry/)

![image](https://circleci.com/gh/phalt/graphene-sentry/tree/master.svg?style=svg%0A%20%20%20%20%20:target:%20https://circleci.com/gh/phalt/graphene-sentry/tree/master)

Installing the project is easy:

``` {.sourceCode .bash}
pip install graphene-sentry
```

Example without file upload:

``` {.sourceCode .python}
# urls.py

from .schema import schema
from graphene_sentry.views import SentryGraphQLView

urlpatterns = [
    url(
        r'^graphql',
        csrf_exempt(SentryGraphQLView.as_view(schema=schema)),
        name='graphql',
    ),
]
```

Example with graphene file upload:

``` {.sourceCode .python}
# urls.py

from .schema import schema
from graphene_sentry.views import SentryFileUploadGraphQLView

urlpatterns = [
    url(
        r'^graphql',
        csrf_exempt(SentryFileUploadGraphQLView.as_view(schema=schema)),
        name='graphql',
    ),
]
```

What can I do?
--------

-   Capture Sentry exceptions properly when they are raise-d in Graphene
    views.

Status
========

graphene-sentry is currently stable and suitable for use.

Credits
=========
This package is based on 
[graphene-django-sentry](https://github.com/phalt/graphene-django-sentry)
author [@phalt](https://github.com/phalt)

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter).

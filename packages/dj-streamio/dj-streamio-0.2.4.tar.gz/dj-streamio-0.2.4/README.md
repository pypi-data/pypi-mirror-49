# DJ StreamIO

Framework for making it easy to post stream updates to (stream.io)[https://getstream.io]

## Installation

[![PyPI version](https://badge.fury.io/py/dj-streamio.svg)](https://badge.fury.io/py/dj-streamio)

```
pip install dj-streamio
```

## Configuration

### 1. Add `streamio` to `INSTALLED_APPS`

### 2. Configure your models for tracking:

e.g.:

```python
from streamio.mixins import StreamModelMixin

class Todo(models.Model, StreamModelMixin):

    collection = 'todos'
    feed_name = 'todo'
    feed_actor_field = 'owner_id'
    feed_once_off_actions = ["create"]
    feed_related_mapping = [
        # feed_slug, model_field
        ('user', 'owner_id'),
        ('todo', 'id'),
    ]
    # a list of object_id prefixes to look for in the `object_ids` field
    # e.g.: todo.object_ids = ["foo:1", "bar:2"]
    feed_object_ids_mapping = ["foo", "bar"]
    enrichment_serializer = 'example_app.models.TodoSerializer'

```

**Notes:**

1. We add `StreamModelMixin` to our model
2. Add the various meta fields
3. Profit

#### Track actions:

```python
todo = Todo.objects.first()
todo.track_action('create')
todo.track_action('start')
todo.track_action('complete')
```

#### Add notifications:

```python
todo = Todo.objects.first()

# note: you'll need to setup a webhook to actually handle forwarding!
# https://getstream.io/docs/#realtime-webhooks

# a combination of ways to propagate this notification (all are optional)
forward = {
    "sms": ['+27...', '+27...'],
    "inapp": ['user:1', 'user:2'], # inapp notification channels
    "email: ['jane@soap.com', 'joe@soap.com']
}

todo.add_notification(
    verb="..",
    notify=[user1.id, user2.id],
    message='hello!',
    forward = forward
)
```

### Get Feed

```python
todo = Todo.objects.first()
# get feed with all the defaults
todo.get_feed()

# you can set any extra args with kwargs:
# available parameters: https://getstream.io/docs/python/#retrieve
todo.get_feed({"limit": 5, "offset": 5, "enrich": False})
```

## Low level usage

```python
from streamio.streamio import get_client
stream = get_client() # returns a standard logged-in stream.io client
...
```
**Note:**

* See also: `StreamObject` and `StreamUser`

### TODOS:

* Provide alternative backends (later)




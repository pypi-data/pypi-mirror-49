# Mercurio

Send email with python, my way.

Mercurio is a simple class to send email with python, managing
smtp, attachments and mimetypes, multiple recipients,
attachments with a specific content id (to html email templating)...

## Installation

Installation is as easy as run:
```pip install mercurio```

## Usage

To initialize a mercurio instance simply call it with
typical smtp parameters. No connection will be opened
at this stage, then you can initialize and reuse it
during the whole code.

```python
from mercurio import mercurio

hg = mercurio(
    host="smtp.test.com",
    port=25,
    smtp_user="myuser",
    smtp_pwd="mypwd"
)
```

To debug purposes, you can create the message and save it in a file
without send it thgrougth smtp. You can open such file
with a normal email client.

```python
message = hg.make_message(
    fromaddress="from@me.com",
    recipient="to@me.com",
    reply_to_address="reply@to.me",
    text="a long text, very long.",
    sbj="The subject, or the object?",
    attachments=[],
    cid_attachments={}
)

with open('test_email.eml', 'w') as o:
    o.write(message.as_string())
```


Send a real message is easy: use
an hg instance, and call
send method with its parameters. Note that you can
send multiple type of attachments (images, xlsx, json,
txt). Mercurio can choice the correct mime type.
You can also use attachment with a specific content
id, that can be used in html email to include
images in the body of the message.

```python
hg.send(
    fromaddress="from@me.com",
    recipients=["to@me.com"],
    reply_to_address="reply@to.me",
    text="a long text, very long.",
    sbj="The subject, or the object?",
    attachments=[],
    cid_attachments={"content_id_01": "mylogo.png"}
)
```

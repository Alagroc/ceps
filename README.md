# ceps
CEPS - Credit Card, email and password service detector.

This is a quick PoC for a hackathon using Python + Flask.

# What does it do?

In a pastebin service we identified a bunch of notes with credit card numbers, emails and even passwords.

This service accepts a chunk of text as a POST or GET on the endpoint /checkrgx/. It checks if there is a possible Personal Identifiable Information (PII) inside, and return a positive answer if so. It was thought to use it to check data before creating a paste note.

# How does it run?

Using uwsgi + nginx is the ideal.

Others, try running *ceps.py* directly with python and flask to test it out.

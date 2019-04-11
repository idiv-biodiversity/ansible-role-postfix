Ansible Role: Postfix
=====================

An Ansible role that installs [Postfix][] and configures it.

Table of Contents
-----------------

<!-- toc -->

- [Requirements](#requirements)
- [Role Variables](#role-variables)
  * [Basic Variables](#basic-variables)
  * [Masquerading](#masquerading)
  * [Aliases Database](#aliases-database)
  * [Generic Database](#generic-database)
  * [Relay Database](#relay-database)
  * [SMTP](#smtp)
  * [Transport Database](#transport-database)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
  * [Top-Level Playbook](#top-level-playbook)
  * [Role Dependency](#role-dependency)
- [License](#license)
- [Author Information](#author-information)

<!-- tocstop -->

Requirements
------------

- Ansible 2+

Role Variables
--------------

### Basic Variables

Variables with defaults:

```yml
postfix_inet_interfaces:
  - localhost
```

These are empty by default, but can be set to simple string values:

```yml
postfix_hostname: 'foo'
postfix_domain: 'bar'
postfix_origin: 'baz'
postfix_relayhost: 'bippy'
```

### Masquerading

Variables regarding masquerading are lists, e.g.:

```yml
postfix_masquerade_classes:
  - 'envelope_sender'
  - 'header_sender'
  - 'header_recipient'

postfix_masquerade_domains:
  - 'foo.example.org'
  - 'bar.example.org'

postfix_masquerade_exceptions:
  - 'root'
```

### Aliases Database

The variable `postfix_aliases` configures `/etc/aliases`, e.g.:

```yml
postfix_aliases:
  - user: 'root'
    alias: 'admin@example.org'
```

### Generic Database

Configure `/etc/postfix/generic`, e.g.:

```yml
postfix_smtp_generic_maps: 'hash:/etc/postfix/generic'

postfix_generic_entries:
  - src: 'root'
    dst: 'admin@example.org'
  - src: 'icinga2@host.foo.example.org'
    dst: 'admin@example.org'
```

### SMTP

That's where I'm mostly fuzzy, but that's how it works for us:

```yml
postfix_smtp:
  tls_CApath: '/etc/pki/tls/certs'
  tls_security_level: 'may'
  tls_cert_file: '/etc/pki/cert.pem'
  tls_key_file: '/etc/pki/key.pem'
  tls_note_starttls_offer: 'yes'

postfix_smtpd:
  tls_CApath: '/etc/pki/tls/certs'
  tls_security_level: 'may'
  tls_cert_file: '/etc/pki/cert.pem'
  tls_key_file: '/etc/pki/key.pem'
  tls_auth_only: 'no'
  tls_loglevel: '1'
  tls_received_header: 'yes'
  tls_session_cache_timeout: '3600s'

postfix_tls_random_source: 'dev:/dev/urandom'
```

At the moment, PEM files need to be copied manually.

### Transport Database

Configure `/etc/postfix/transport`, e.g.:

```yml
postfix_transport_maps: 'hash:/etc/postfix/transport'

postfix_transport_entries:
  - src: 'foo.org'
    dst: 'smtp:[mail.example.org]'
  - src: 'bar.org'
    dst: 'smtp:[mail.example.org]'
```

Dependencies
------------

None.

Example Playbook
----------------

Add to `requirements.yml`:

```yml
---

- src: idiv-biodiversity.postfix

...
```

Download:

```console
$ ansible-galaxy install -r requirements.yml
```

### Top-Level Playbook

Write a top-level playbook:

```yml
---

- name: head server
  hosts: head

  roles:
    - role: idiv-biodiversity.postfix
      tags:
        - mail
        - mta
        - postfix

...
```

### Role Dependency

Define the role dependency in `meta/main.yml`:

```yml
---

dependencies:

  - role: idiv-biodiversity.postfix
    tags:
      - mail
      - mta
      - postfix

...
```

License
-------

MIT

Author Information
------------------

This role was created in 2017 by [Christian Krause][author] aka [wookietreiber at GitHub][wookietreiber], HPC cluster systems administrator at the [German Centre for Integrative Biodiversity Research (iDiv)][idiv], based on a draft by Ben Langenberg aka [bencarsten at GitHub][bencarsten].


[author]: https://www.idiv.de/groups_and_people/employees/details/eshow/krause-christian.html
[idiv]: https://www.idiv.de/
[bencarsten]: https://github.com/bencarsten
[wookietreiber]: https://github.com/wookietreiber
[postfix]: http://www.postfix.org/

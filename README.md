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
```

### Aliases

The variable `postfix_aliases` configures `/etc/aliases`, e.g.:

```yml
postfix_aliases:
  - user: 'root'
    alias: 'admin@example.org'
```

### SMTP Generic Table

Defines address mappings when mail is delivered via SMTP. This is useful to
transform **local** mail addresses into **valid** mail addresses. The following
example rewrites the sender **icinga@internal** to **support@example.org** and
everything else **@internal** to **no-reply@example.org**:

```yml
postfix_smtp_generic:
  type: hash
  dest: /etc/postfix/smtp_generic
  content: |
    icinga@internal support@example.org
    @internal       no-reply@example.org
```

**Note:** Affects both message header addresses, i.e. the **From:** field, and
envelope addresses which are used by SMTP.

**Note:** Consult `man 5 generic` for more information.

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

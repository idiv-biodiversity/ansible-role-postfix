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
  * [Aliases](#aliases)
  * [Relay and Transport](#relay-and-transport)
  * [Canonical Address Mapping](#canonical-address-mapping)
  * [SMTP Generic Table](#smtp-generic-table)
  * [Header Checks](#header-checks)
  * [SMTP](#smtp)
  * [Automatic Header Rewriting](#automatic-header-rewriting)
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

This role does in no way capture the entirety of possible postfix options. If
you need something specific, feel free to contribute!

The `content` field is optional for of all dictionary variables potentially
referring to *configuration tables*, e.g. `postfix_transport`.

### Basic Variables

Variables with defaults:

```yml
postfix_inet_interfaces:
  - localhost

postfix_inet_protocols: all

postfix_destinations:
  - $myhostname
  - localhost.$mydomain
  - localhost
```

These variables are empty by default, but postfix has its own defaults for
them. Check `postconf -d | grep ^my` for their defaults.

```yml
postfix_hostname: host.example.org
postfix_domain: example.org
postfix_origin: example.org
```

**Note:** Consult `man 5 postconf` for more information.

### Masquerading

Masquerading can strip off subdomain structure, e.g. to rewrite
**user@sub.domain.example.org** to **user@example.org**:

```yml
postfix_masquerade_domains:
  - example.org
```

Addresses that will be changed by masquerading:

```yml
postfix_masquerade_classes:
  - envelope_sender
  - envelope_recipient
  - header_sender
  - header_recipient
```

Users who are exceptions to masquerading:

```yml
postfix_masquerade_exceptions:
  - root
```

**Note:** Masquerading address mapping mechanism is able to rewrite both header
and envelope addresses. For headers to be rewritten, see the section about
[Automatic Header Rewriting](#automatic-header-rewriting).

### Aliases

The variable `postfix_aliases` configures `/etc/aliases`, e.g.:

```yml
postfix_aliases:
  - user: icinga
    alias: root
  - user: root
    alias: admin@example.org
```

### Relay and Transport

Delivery targets, i.e. relays:

```yml
postfix_relayhost: relay1.domain.org
postfix_smtp_fallback_relay: relay2.domain.org
```

Additionally, there is more fine-grained control with the transport table:

```yml
postfix_transport:
  - type: hash
    dest: /etc/postfix/transport
    content: |
      foo.org         smtp:[imap1.example.org]
      .foo.org        smtp:[imap1.example.org]
      bar.org         smtp:[imap2.example.org]
      .bar.org        smtp:[imap2.example.org]
```

**Note:** Consult `man 5 transport` for more information.

### Canonical Address Mapping

Rewrite recipient and sender:

```yml
postfix_canonical:
  - type: hash
    dest: /etc/postfix/canonical
    content: |
      platform@internal.domain platform@example.org
  - type: ldap
    dest: /etc/postfix/ldap-canonical.cf
    content: |
      server_host = ldap.example.org
      search_base = dc=example, dc=org
      query_filter = uid=%s
      result_attribute = mail
```

Rewrite recipient:

```yml
postfix_recipient_canonical:
  - type: hash
    dest: /etc/postfix/recipient_canonical
    content: |
      root@internal.domain   admin@example.org
      icinga@internal.domain admin@example.org
```

Rewrite sender:

```yml
postfix_sender_canonical:
  - type: hash
    dest: /etc/postfix/sender_canonical
    content: |
      root@internal.domain   support@example.org
      icinga@internal.domain support@example.org
```

**Note:** The **canonical** address mapping mechanism is able to rewrite both
header and envelope addresses. For headers to be rewritten, see the section
about [Automatic Header Rewriting](#automatic-header-rewriting).

**Note:** Consult `man 5 canonical` for more information.

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

### Header Checks

This lets you rewrite or reject message headers:

```yml
postfix_header_checks:
  - type: regexp
    dest: /etc/postfix/header_checks
    content: |
      /^From: root@[^ ]+\.example.org .*/ REPLACE From: no-reply@example.org
```

**Note:** Consult `man 5 header_checks` for more information.

### SMTP

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

**Note:** At the moment, PEM files need to be copied manually.

### Automatic Header Rewriting

Starting with Postfix 2.2 automatic message header rewriting has been disabled
by default. Instead, only envelope addresses get rewritten. This applies to the
address rewriting facilities. Check `man 5 postconf` to see if it applies to
your configuration entries.

To get the behavior before Postfix 2.2, add this variable:

```yml
postfix_local_header_rewrite_clients:
  - type: static
    dest: all
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

==============================
Fortinet.Fortios Release Notes
==============================

.. contents:: Topics


v2.0.2
======

Release Summary
---------------

patch release of 2.0.2

Major Changes
-------------

- Improve ``fortios_configuration_fact`` to use multiple selectors concurrently.
- Support ``check_mode`` in all cofigurationAPI-based modules.
- Support filtering for fact gathering modules ``fortios_configuration_fact`` and ``fortios_monitor_fact``.
- Support moving policy in ``firewall_central_snat_map``.
- Unify schemas for monitor API.

Bugfixes
--------

- Fix the authorization fails at log in with username and password in FOS7.0.
- Github Issue 103
- Github Issue 105

v2.0.1
======

Minor Changes
-------------

- fixed pylint testing errors.

v2.0.0
======

Release Summary
---------------

The major breaking release of FOS 2.x collections.

Major Changes
-------------

- New module fortios_configuration_fact
- New module fortios_json_generic
- New module fortios_monitor
- New module fortios_monitor_fact

Breaking Changes / Porting Guide
--------------------------------

- Generic FortiOS Module - FOS module to issue generic request with Ansible.
- Support for FOS Monitor API - several modules are new for monitor API.
- Unified Collection - The fortios collection itself will be adapting any FOS platforms.

Removed Features (previously deprecated)
----------------------------------------

- Removed module fortios_facts
- Removed module fortios_registration_forticare
- Removed module fortios_registration_vdom
- Removed module fortios_system_config_backup_restore
- Removed module fortios_system_vmlicense

Bugfixes
--------

- Deprecated second-layer state module parameter
- enable_log - Explicit logging option.

Known Issues
------------

- Modules for monitor API are not versioned yet.

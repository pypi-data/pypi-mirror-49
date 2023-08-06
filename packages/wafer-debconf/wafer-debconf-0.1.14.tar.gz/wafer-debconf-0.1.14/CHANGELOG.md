# Changelog

## 0.1.13

* Support Postgres in the queue migration from 0.1.12

## 0.1.12

* Add a management command to create volunteer tasks from YAML
* Improve the track list in the schedule.
* Change registration permissions (only admins can take cash).
* Get badges working again.
* Assign keysigning IDs, and add a management command to sort them.

## 0.1.11

* Generalize the badger speaker script to all talk statuses.
* Add a keysigning export.

## 0.1.10

* Validate speaker attendance dates, when schedule editing.
* Use DebConf's custom schedule templates.
* Add Python 3.5 support to the load\_schedule\_grid command.

## 0.1.9

* Add a command to load schedule grid from YAML

## 0.1.8

* Add a badger for accepted talks
* Add travel\_from to the bursary export.

## 0.1.7

* List exports in front desk
* Add bursaries export

## 0.1.6

* Further improvements to the bursary notification email.

## 0.1.5

* Add management command to remind users to register.
* Include some details, useful for visas in the registration
  confirmation email.
* Handle unassigned rooms, correctly.
* Clear travel expense amount, when cancelling a travel bursary request.
* Add a CSV export for Child Care.
* Display meal lists, in order.
* Remove DC18 details from the bursary notification email.

## 0.1.4

* Correct the permission checked by bursary admin pages.

## 0.1.3

* Add a Volunteer Admin group.
* Add Kosovo to the list of countries.

## 0.1.2

* SECURITY: Don't show other registered attendees as room-mates, when
  nobody has rooms assigned.

## 0.1.1

* Package now has metadata and license.
* New management commands: `create_debconf_groups`,
  `load_tracks_and_talk_types`.

## 0.1.0

* Initial release, mostly ready for DebConf19.

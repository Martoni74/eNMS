==============
Administration
==============

Changelog
---------

eNMS keeps of changelog available in "Home / Changelog".

.. image:: /_static/administration/changelog.png
   :alt: Filtering System.
   :align: center

This changelog contains:

- All creation and deletion of model instances.
- All modification of these instances (which properties were modified: old value and new value).
- All runs: what services / workflows were run, when, who started them.
- Various administration logs such as database migration, parameters update, etc.

Credentials
-----------

Credentials are stored in a Hashicorp Vault, or in the database if no Vault has been configured.
If you are using eNMS in production, it is recommended to set up a Hashicorp Vault to handle the storage of all credentials.

- User credentials can be used to authenticate to eNMS, as well as to authenticate to a network device.
- Device credentials are a property of the device itself within the inventory. The credentials of a device are a ``username``, a ``password``, and an ``enable password`` required on some devices to enter the "enable" mode.
    
.. image:: /_static/advanced/administration/credentials.png
   :alt: Set password
   :align: center

Database
********

Migration, Backup, and Restore
------------------------------

The eNMS migration system handles exporting the complete database content into YAML files.
By providing a directory name and selecting which eNMS object types to export/backup,
eNMS serializes the stored objects in the directory ``eNMS/files/migrations/project_name``.
These yaml files can then be copied into the same directory on a new VM instance of eNMS,
and then the Import function can be used to import/restore the configuration and living data of
those object types.
These migration files are used for migrating from one version of eNMS to the next version. 
They are also used for Backup and Restore of eNMS.
The migration system is accessed from the :guilabel:`Admin / Administration` or from the REST API.

.. image:: /_static/administration/administration/migrations.png
   :alt: Migrations
   :align: center

When creating a new instance of eNMS:
  - Install eNMS.
  - Run the :guilabel:`Admin / Administration / Migration` either from the UI or from the REST API. Select 'Empty_database_before_import' = True, specify
    the location of the file to import, and select all object types to be imported: "user", "device", "link", "pool", "service", "workflow_edge", "task"

When backing up eNMS, it is only necessary to perform :guilabel:`Admin / Administration / Migration` either from the UI or from the REST API.
  - Select a directory name for storing the migration files into, and select all object types to Export
  - the Topology Export of device and link data from :guilabel:`Admin / Administration / Topology Import` and :guilabel:`Admin / Administration / Topology Export` is not needed for Backup.
    It is intended for sharing of device and link data.

.. note:: the exported backup files do not contain the secure credentials for each of the inventory devices in plain text, as credentials are considered to be stored in a Vault in production mode.

.. note:: If you are migrating data on an existing instance of eNMS, you can choose tick the option ``Empty Database before Import`` to empty the database before starting the migration.

.. note:: See additional discussion of migration in the Installation Section

Miscellaneous
-------------

- ``Fetch Git Configurations and Update Devices``: this feature will retrieve configurations from the git 'configurations' repository and load those into the database for each matching inventory device. This is performed automatically when eNMS starts up: the git configurations repository is quietly cloned and loaded into the database. This feature allows for manual pulling of updated configurations data.
- ``Pause and Resume Scheduler``: this feature will pause and resume all scheduler tasks currently waiting to run.
- ``Reset Service Statuses``: when a service or workflow fails, it is sometimes stuck in a "Running" mode and cannot be executed. This button will reset the status of all services and workflows.

Individual export
-----------------

Services and workflows can be exported and imported individually, as a .tgz archive.
This is useful when you have multiple VMs deployed with eNMS, and you need to send a service / workflow from one VM to another.

To import a service, you need to move the archive to the ``files/services`` folder,
then go to the "Administration" page and click on the ``Import services`` button.


CLI interface
-------------

eNMS has a CLI interface with the following operations:

Fetch an object from the database
*********************************

General syntax: ``flask fetch object_type object_name``
Example:

::

 flask fetch device Washington

Modify the properties of an object
**********************************

General syntax: ``flask update object type 'object_properties'`` where `object_properties` is a JSON dictionary that contains the name of the object, and the properties to update.
Example:

::

 flask update device '{"name": "Aserver", "description": "test"}'

Delete an object from the database
**********************************

General syntax: ``flask delete object_type object_name``
Example:

::

 `flask delete device Washington`

Run a service
*************

General syntax: ``flask start service_name --devices list_of_devices --payload 'payload'`` where:

- list_of_devices is a list of device name separated by commas.
- payload is a JSON dictionary.

Both devices and payload are optional parameters.

Examples:

::

 `flask run_service get_facts`
 `flask run_service get_facts --devices Washington,Denver`
 `flask run_service get_facts --payload '{"a": "b"}'`
 `flask run_service get_facts --devices Washington,Denver --payload '{"a": "b"}'`
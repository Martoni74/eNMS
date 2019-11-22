===============
Workflow System
===============

A workflow is comprised of one or more services that when followed from start to end will execute an activity, such as a software upgrade. These services are constructed into a directed graph instructing the machine which service is next. The services in the workflow can be either a service or another workflow. A service can range from a simple query to a more complex set of commands.

Each service in eNMS returns a boolean value:

- ``True`` if it ran successfully.
- ``False`` otherwise.

There are two types of results from a workflow service: ``Success`` edge and ``Failure`` edge. If a service is executed as designed, it returns a success edge, and the workflow continues down the path to the next service as indicated in the graph. However, if a service returns atypical or correctable output it give us the failure edge, which takes a different path if provided in the graph, or stops the workflow when no path is provided in the graph. Each workflow must have a Start service and an End service for eNMS to know which service should be executed first and when to stop running the workflow.

Workflows are created and managed from the :guilabel:`Automation / Workflow Management` and :guilabel:`Automation / Workflow Builder` page.

Workflow Management
-------------------

In the :guilabel:`Automation / Workflow Management` page, click on the button ``Create`` and fill the workflow creation form.
The new workflow will be automatically added to the table of workflows.
From the same page, workflows can be edited, deleted, and duplicated. They can also be ran, and their result logs examined.

.. image:: /_static/workflows/workflow_management.png
   :alt: Workflow management
   :align: center

Workflows can also be created from the Workflow Builder page.

Workflow Builder
----------------

The :guilabel:`Automation/Workflow Builder` is the place where services (or other workflows) are organized into workflows.
It contains:

- A drop-down list containing all existing workflows. This list allows switching between workflows.
- The workflow itself is displayed as a graph. The  services are connected by arrows of type success edge or failure edge.
- A ``general right-click menu`` can be accessed by clicking on the background or white-space.
- A ``service-specific right-click menu`` can be accessed by right clicking on a specific service.

The ``general right-click menu`` contains the following entries:

- Change Mode (create edges or move a service in the Workflow Builder)
- Create Workflow
- Add to Workflow (lets you choose which services to add amongst all existing services)
- Run Workflow (starts the workflow)
- Edit Workflow (same Workflow editor from the Workflow Management page)
- Workflow Results
- Workflow Logs
- Refresh View

.. image:: /_static/workflows/workflow_background_menu.png
   :alt: Workflow management
   :align: center

From the ``service-specific right-click menu``, you can:

- Edit a service (service or workflow)
- Run a service (service or workflow)
- Display the Results
- Delete a service (remove from the workflow)

.. image:: /_static/workflows/workflow_service_menu.png
   :alt: Workflow management
   :align: center

Waiting time
------------

Services and Workflows have a ``Waiting time`` property: this tells eNMS how much time it should wait after the Service/Subworkflow has run before it begins the next service.
This is useful if the service you're running needs time to be processed or operated upon before another service can be started.

A service can also be configured to "retry"  if the results returned are not as designed. An example execution of a service in a workflow, in terms of waiting times and retries, is as follows:

::

  First try
  time between retries pause
  Retry 1
  time between retries pause
  Retry 2  (Successful, or only 2 Retries specified)
  Waiting time pause

Workflow devices
----------------

When you create a workflow, just like with services instances, the form will also contain multiple selection fields for you to select "target devices", as well as an option ``Use Workflow Targets``:

- If selected, the devices for the workflow will be used for execution.
- If not selected, the devices selected at the individual service level will be used for execution.


If ``Use Workflow Targets`` is unticked, services will run on their own targets. A service is considered successful if it ran successfully on all of its targets (if it fails on at least one target, it is considered to have failed).
The "Use service targets" mode can be used for workflows where services have different targets (for example, a first service would run on devices A, B, C and the next one on devices D, E).

If ``Use Workflow Targets`` is ticked, the workflow will run on its own targets (all devices configured at service level are ignored). Devices are independent from each other: one device may run on all services in the workflow if it is successful while another one could stop at the first step: they run the workflow independently and will likely follow different path in the workflow depending on whether they fail or pass services thoughout the workflow.

Connection Cache
----------------

When using several netmiko and napalm connections in a workflow, the connection object is cached and reused automatically.
If for some reason you want a service to create a fresh connection, you can tick the ``Start New Connection`` box
in the "Workflow" section of the creation panel.
Upon running this service, eNMS will automatically discard the current cached connection, start a new one and
make it the new cached connection.

Success of a Workflow
---------------------

The behavior of the workflow is such that the workflow is considered to have an overall Success status if the END service is reached. So, the END service should only be reached by an edge when the overall status of the workflow is considered successful. If a particular service service fails, then the workflow should just stop there (with the workflow thus having an overall Failure status), or it should call a cleanup/remediation service (after which the workflow will just stop there).

Position saving
---------------

Note that the positions of the services of a workflow in the Workflow Builder page is saved to the database only when the user navigates away from the workflow.
- Upon leaving the Workflow Builder page.
- When switching to another workflow.

All other changes to the Workflow Builder are saved immediately.

Automatic refresh
-----------------

A workflow displayed in the Workflow Builder page is automatically updated:
- Every 0.7 second if the workflow is currently running
- Every 15 seconds otherwise

This allows multiple users to work concurrently on a single Workflow in the Workflow Builder.

Workflow Restartability
-----------------------

A workflow can be restarted with any services set as "Entry points"
and with the payload from a previous runs.
This is useful if you are testing a workflow with a lot of services, and you don't want it to
restart from scratch all the time.

You must click on "Run with Updates" and go to the "Workflow" section to access these parameters.

.. image:: /_static/workflows/workflow_restartability.png
   :alt: Workflow Restartability
   :align: center

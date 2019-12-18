/*
global
alertify: false
call: false
config: true
createPanel: false
fCall: false
folders: false
JSONEditor: false
page: false
showPanel: false
tables: false
*/

let editor;

// eslint-disable-next-line
function showConfiguration() {
  createPanel("configuration", "Configuration", null, function() {
    editor = new JSONEditor(document.getElementById("content"), {}, config);
  });
}

// eslint-disable-next-line
function saveConfiguration() {
  $.ajax({
    type: "POST",
    url: "/save_configuration",
    contentType: "application/json",
    data: JSON.stringify(editor.get()),
    success: function() {
      config = editor.get();
      $("#configuration").remove();
      alertify.notify("Configuration saved.", "success", 5);
    },
  });
}

// eslint-disable-next-line
function showImportTopologyPanel(type) {
  createPanel("excel_import", "Import Topology as an Excel file", 0, () => {
    document.getElementById("file").onchange = function() {
      importTopology();
    };
  });
}

// eslint-disable-next-line
function queryOpenNMS() {
  call("/query_opennms", function() {
    alertify.notify("Topology imported from OpenNMS.", "success", 5);
  });
}

// eslint-disable-next-line
function queryNetbox() {
  call("/query_netbox", function() {
    alertify.notify("Topology imported from Netbox.", "success", 5);
  });
}

// eslint-disable-next-line
function queryLibreNMS() {
  call("/query_librenms", function() {
    alertify.notify("Topology imported from LibreNMS.", "success", 5);
  });
}

// eslint-disable-next-line
function exportTopology() {
  alertify.notify("Topology export starting...", "success", 5);
  fCall("/export_topology", "#excel_export-form", function() {
    alertify.notify("Topology successfully exported.", "success", 5);
  });
}

// eslint-disable-next-line
function importTopology() {
  alertify.notify("Topology import: starting...", "success", 5);
  const formData = new FormData($("#import-form")[0]);
  $.ajax({
    type: "POST",
    url: "/import_topology",
    dataType: "json",
    data: formData,
    contentType: false,
    processData: false,
    async: true,
    success: function(result) {
      alertify.notify(result, "success", 5);
    },
  });
  $("#file")[0].value = "";
}

function getClusterStatus() {
  call("/get_cluster_status", function(cluster) {
    tables["server"].ajax.reload(null, false);
    setTimeout(getClusterStatus, 15000);
  });
}

// eslint-disable-next-line
function migrationsExport() {
  alertify.notify("Export initiated.", "success", 5);
  fCall("/migration_export", "#migration-form", function() {
    alertify.notify("Export successful.", "success", 5);
  });
}

// eslint-disable-next-line
function showMigrationPanel() {
  showPanel("database_migration", null, () => {
    let list = document.getElementById("versions");
    folders.forEach((item) => {
      let option = document.createElement("option");
      option.textContent = option.value = item;
      list.appendChild(option);
    });
  });
}

// eslint-disable-next-line
function migrationsImport() {
  alertify.notify("Import initiated.", "success", 5);
  fCall("/migration_import", "#migration-form", function(result) {
    alertify.notify(result, "success", 5);
  });
}

function refreshExportedServices() {
  call("/get_exported_services", function(services) {
    let list = document.getElementById("service");
    services.forEach((item) => {
      let option = document.createElement("option");
      option.textContent = option.value = item;
      list.appendChild(option);
    });
    $("#service").selectpicker("refresh");
  });
}

// eslint-disable-next-line
function showImportServicePanel() {
  showPanel("import_service", null, () => {
    refreshExportedServices();
  });
}

// eslint-disable-next-line
function importService() {
  call(`/import_service/${$("#service").val()}`, function(result) {
    alertify.notify("Import successful.", "success", 5);
    $("#import_service").remove();
  });
}

// eslint-disable-next-line
function databaseDeletion() {
  alertify.notify("Starting to delete...", "success", 5);
  fCall("/database_deletion", "#database_deletion-form", function(result) {
    alertify.notify("Deletion done.", "success", 5);
    $("#deletion-form").remove();
  });
}

// eslint-disable-next-line
function getGitContent() {
  call("/get_git_content", function(result) {
    alertify.notify("Action successful.", "success", 5);
  });
}

// eslint-disable-next-line
function scheduler(action) {
  call(`/scheduler_action/${action}`, function() {
    alertify.notify(`Scheduler ${action}d.`, "success", 5);
  });
}

// eslint-disable-next-line
function scanCluster() {
  alertify.notify("Scan started.", "success", 5);
  call("/scan_cluster", function(cluster) {
    alertify.notify("Scan completed.", "success", 5);
  });
}

(function() {
  if (page == "server_management") {
    getClusterStatus();
  }
})();

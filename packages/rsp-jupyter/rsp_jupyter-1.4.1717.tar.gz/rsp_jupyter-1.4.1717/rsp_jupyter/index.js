define([
   "base/js/events",
   "base/js/namespace",
   "base/js/promises",
   "base/js/utils",
   "base/js/dialog",
   "base/js/i18n"],

function(events, Jupyter, promises, utils, dialog, i18n) {

   function load_ipython_extension() {
      promises.app_initialized.then(function(app) {
         if (app === "NotebookApp") {
            writeNotebookPath();
            registerHomeButton();
            modifyLogoutButton();
            startAuthCheck();
         }
      });
   }

   function getServerRpcUrl() {
      var jupyterBaseUrl = Jupyter.notebook.base_url;

      // rewrite the base URL to point to the root url (prefix of workspace url)
      var regex = /(s\/[\w]{5}[\w]{8}[\w]{8}\/)/g;
      return jupyterBaseUrl.replace(regex, "")
   }

   function getBaseUrl() {
      var jupyterBaseUrl = Jupyter.notebook.base_url;

      // rewrite the base URL to point to the workspaces session url
      var regex = /(s\/[\w]{5})([\w]{8}[\w]{8})/g;
      return jupyterBaseUrl.replace(regex, "$13c286bd33c286bd3")
   }

   function getHomeUrl() {
      var jupyterBaseUrl = Jupyter.notebook.base_url;

      // rewrite the base URL to point to the /home url
      var regex = /s\/[\w]{5}[\w]{8}[\w]{8}/g;
      return jupyterBaseUrl.replace(regex, "home")
   }

   function writeNotebookPath() {
      var notebookPath = Jupyter.notebook.notebook_path;
      var baseUrl = getBaseUrl();
      var homepageUrl = getHomeUrl();
      var workspacesUrl = baseUrl + "workspaces/";
      var rpcUrl = workspacesUrl + "write_notebook_path?path=" + encodeURIComponent(notebookPath);

      var onSuccess = function(result) {
         $.ajax({
            url: rpcUrl,
            success: function(result) {
               console.log("Successfully wrote notebook path " + notebookPath);
            },
            error: function(xhr, status, error) {
               console.log("Failed to write notebook path to " + rpcUrl + " - " + error);
            }
         });
      }

      // before invoking the RPC, load the homepage to ensure that the workspaces executable is running
      // it is possible for it to exit, and loading the workspaces page forces it to be relaunched
      $.ajax({
         url: homepageUrl,
         success: onSuccess,
         error: function(xhr, status, error) {
            console.log("Could not connect to RSP homepage URL: " + homepageUrl);
         }
      });
   }

   function registerHomeButton() {
      var imageSrc = requirejs.toUrl("nbextensions/rsp_jupyter/rstudio.png");
      var element = "<span id=\"rstudio_logo_widget\"><a href=\"" + getHomeUrl() + "\"><img class=\"current_kernel_logo\" alt=\"RStudio Home Page\" src=\"" + imageSrc +
                    "\" title=\"RStudio Home Page\" style=\"display: inline; padding-right: 10px;\" height=\"32\"></a></span>";

      $("#ipython_notebook").before(element);
   }

   function modifyLogoutButton() {
      btn = $("button#logout")
      btn.html("Quit");
      btn.unbind();
      btn.click(function () {
         utils.ajax(utils.url_path_join(
            utils.get_body_data("baseUrl"),
            "api",
            "shutdown"
         ), {
            type: "POST",
            success: display_shutdown_dialog,
            error: function (error) {
               console.log(error);
            }
         });
      });
    }

    function display_shutdown_dialog() {
      var body = $("<div/>").append(
            $("<p/>").text(i18n.msg._("You have shut down Jupyter. You can now close this tab."))
      ).append(
            $("<p/>").text(i18n.msg._("To use Jupyter again, you will need to relaunch it."))
      );

      dialog.modal({
         title: i18n.msg._("Server stopped"),
         body: body
      })
   }

   // tracks the last time the user performed an action via mouse/keyboard
   var lastActivity;

   // invokes RPC to check if we are still signed in, and also refresh credentials if user is active
   // if we are unauthorized, we will get a redirect to the sign in page
   // indicating our auth is expired, and we should reload the page to be redirected
   // to the correct sign in page
   function checkAuth() {
      var baseUrl = getServerRpcUrl();
      var authUrl = baseUrl + "check_auth";
      if (Date.now() - lastActivity <= 30000) {
         authUrl += "?refresh=1";
      }

      var xhr = new XMLHttpRequest();
      xhr.open('GET', authUrl, true);
      xhr.onload = function() {
         if (xhr.status === 401) {
            location.reload(true);
         }
      };
      xhr.send();
   }

   function startAuthCheck() {
      // periodically check for auth validity and redirect to the RSP homepage if our auth expires
      // we will proactively refresh out auth based on when the user performed some action via mouse/keyboard
      document.onkeypress = function(e) {
         lastActivity = Date.now();
      };

      document.onmousedown = function(e) {
         lastActivity = Date.now();
      };

      window.setInterval(checkAuth, 30000);

      // set the initial last activity time to now
      // to ensure that auth cookies are generated on the first RPC call
      // this ensures that the cookie will always be available unless it expires
      // due to the user not using the session
      lastActivity = Date.now();
   }

   return {
      load_ipython_extension: load_ipython_extension
   };

});

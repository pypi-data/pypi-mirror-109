(self["webpackChunkjupyterlab_novnc"] = self["webpackChunkjupyterlab_novnc"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'novnc', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fooIcon": () => (/* binding */ fooIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg");




const SETTINGS_ID = 'jupyterlab-novnc:jupyterlab-novnc-settings';




const fooIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: 'jupyterlab-novnc:icon',
    svgstr: _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__.default
});
class noVNCWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame {
    constructor(options) {
        super();
        const queryElems = [];
        for (const k in options) {
            queryElems.push(encodeURIComponent(k) + '=' + encodeURIComponent(options[k]));
        }
        this.query = queryElems.join('&');
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getBaseUrl();
        this.url = baseUrl + `novnc/app/vnc.html?${this.query}`;
        console.log('Full URL: ', this.url);
        this.id = 'noVNC';
        this.title.label = 'noVNC';
        this.title.closable = true;
        this.node.style.overflowY = 'auto';
        this.node.style.background = '#FFF';
        this.sandbox = [
            'allow-forms',
            'allow-modals',
            'allow-orientation-lock',
            'allow-pointer-lock',
            'allow-popups',
            'allow-presentation',
            'allow-same-origin',
            'allow-scripts',
            'allow-top-navigation',
            'allow-top-navigation-by-user-activation'
        ];
    }
    dispose() {
        super.dispose();
    }
    onCloseRequest() {
        this.dispose();
    }
}
/**
 * Initialization data for the jupyterlab-novnc extension.
 */
const extension = {
    id: 'jupyterlab-novnc:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    activate: (app, palette, settings, launcher) => {
        let _settings;
        const command = 'novnc:open';
        let registeredCommands = [];
        const _loadSettings = () => {
            const enpoints = _settings.get('configured_endpoints').composite;
            let i = 0;
            for (const c of registeredCommands) {
                c.dispose();
            }
            registeredCommands = [];
            for (const epconf of enpoints) {
                console.log('Adding comand .. ');
                // const full_cmd = command + `:${i}`
                const full_cmd = command + `:${i}`;
                const widget = new noVNCWidget(epconf);
                const rcmd = app.commands.addCommand(full_cmd, {
                    label: `Connect to VNC ${i}: ${'name' in epconf ? epconf['name'] : epconf['host']}`,
                    execute: () => {
                        if (!widget.isAttached) {
                            // Attach the widget to the main work area if it's not there
                            app.shell.add(widget, 'main');
                        }
                        // Activate the widget
                        app.shell.activateById(widget.id);
                    },
                    icon: fooIcon
                });
                registeredCommands.push(rcmd);
                // Add a launcher item if the launcher is available.
                if (launcher) {
                    const lcmd = launcher.add({
                        command: full_cmd,
                        rank: 1,
                        category: 'VNC'
                    });
                    registeredCommands.push(lcmd);
                }
                const pcmd = palette.addItem({ command: full_cmd, category: 'NoVNC' });
                registeredCommands.push(pcmd);
                i += 1;
            }
        };
        settings.load(SETTINGS_ID).then(setting => {
            console.log(setting);
            _settings = setting;
            const extensions = setting.get('configured_endpoints').composite;
            console.log(extensions);
            _loadSettings();
            setting.changed.connect(_loadSettings);
        });
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab-novnc server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./style/icon.svg":
/*!************************!*\
  !*** ./style/icon.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>\r\n<!-- Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\r\n<svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\r\n\t viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M394.668,0H32.001c-17.673,0-32,14.327-32,32v256c0,17.673,14.327,32,32,32h138.667v-21.333H32.001\r\n\t\t\tc-5.891,0-10.667-4.776-10.667-10.667V32c0-5.891,4.776-10.667,10.667-10.667h362.667c5.891,0,10.667,4.776,10.667,10.667v192\r\n\t\t\th21.333V32C426.668,14.327,412.341,0,394.668,0z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<rect x=\"128.001\" y=\"309.333\" width=\"21.333\" height=\"64\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M74.668,256c-5.891,0-10.667-4.776-10.667-10.667V224H42.668v21.333c0,17.673,14.327,32,32,32h21.333V256H74.668z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<rect x=\"42.668\" y=\"181.333\" width=\"21.333\" height=\"21.333\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M389.836,225.941c-21.736-21.74-51.219-33.953-81.961-33.952c-64.006,0.003-115.891,51.892-115.889,115.898\r\n\t\t\tc0.003,64.006,51.892,115.891,115.898,115.889c30.732-0.001,60.204-12.208,81.937-33.937\r\n\t\t\tC435.084,344.584,435.091,271.205,389.836,225.941z M307.82,402.453c-52.224-0.018-94.546-42.368-94.528-94.592\r\n\t\t\tc0.018-52.224,42.368-94.546,94.592-94.528c25.101-0.068,49.184,9.92,66.869,27.733c17.718,17.738,27.667,41.787,27.659,66.859\r\n\t\t\tC402.394,360.149,360.044,402.471,307.82,402.453z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M508.876,464l-66.955-66.933c-2-2-4.713-3.125-7.541-3.125c-2.829,0.001-5.541,1.125-7.541,3.125l-29.76,29.76\r\n\t\t\tc-4.164,4.165-4.164,10.917,0,15.083l66.955,66.965c2,2.001,4.713,3.125,7.541,3.125v0c2.833-0.009,5.547-1.145,7.541-3.157\r\n\t\t\tl29.76-29.76C513.04,474.917,513.04,468.165,508.876,464z M471.574,486.251l-51.872-51.883l14.677-14.677l51.872,51.883\r\n\t\t\tL471.574,486.251z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t\r\n\t\t\t<rect x=\"390.231\" y=\"374.581\" transform=\"matrix(0.7071 -0.7071 0.7071 0.7071 -166.0486 400.894)\" width=\"21.333\" height=\"52.608\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M309.334,234.667V256c29.441,0.035,53.298,23.893,53.333,53.333h21.333C383.954,268.116,350.552,234.714,309.334,234.667z\r\n\t\t\t\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<rect x=\"106.668\" y=\"362.667\" width=\"85.333\" height=\"21.333\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M160.001,42.667c-17.673,0-32,14.327-32,32c0,17.673,14.327,32,32,32s32-14.327,32-32\r\n\t\t\tC192.001,56.994,177.674,42.667,160.001,42.667z M160.001,85.333c-5.891,0-10.667-4.776-10.667-10.667\r\n\t\t\tc0-5.891,4.776-10.667,10.667-10.667s10.667,4.776,10.667,10.667C170.668,80.558,165.892,85.333,160.001,85.333z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M234.668,117.333c-17.673,0-32,14.327-32,32c0,17.673,14.327,32,32,32c17.673,0,32-14.327,32-32\r\n\t\t\tC266.668,131.66,252.341,117.333,234.668,117.333z M234.668,160c-5.891,0-10.667-4.776-10.667-10.667\r\n\t\t\tc0-5.891,4.776-10.667,10.667-10.667c5.891,0,10.667,4.776,10.667,10.667C245.334,155.224,240.559,160,234.668,160z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t\r\n\t\t\t<rect x=\"84.956\" y=\"101.336\" transform=\"matrix(0.7071 -0.7071 0.7071 0.7071 -43.269 119.5445)\" width=\"75.424\" height=\"21.333\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t\r\n\t\t\t<rect x=\"186.623\" y=\"74.317\" transform=\"matrix(0.7071 -0.7071 0.7071 0.7071 -21.4319 172.3178)\" width=\"21.333\" height=\"75.424\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t<path d=\"M309.334,42.667c-17.673,0-32,14.327-32,32c0,17.673,14.327,32,32,32c17.673,0,32-14.327,32-32\r\n\t\t\tC341.335,56.994,327.008,42.667,309.334,42.667z M309.334,85.333c-5.891,0-10.667-4.776-10.667-10.667\r\n\t\t\tc0-5.891,4.776-10.667,10.667-10.667c5.891,0,10.667,4.776,10.667,10.667C320.001,80.558,315.225,85.333,309.334,85.333z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n\t<g>\r\n\t\t\r\n\t\t\t<rect x=\"234.285\" y=\"101.373\" transform=\"matrix(0.7071 -0.7071 0.7071 0.7071 0.4421 225.1463)\" width=\"75.424\" height=\"21.333\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n</svg>\r\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.28962115e413402a7328.js.map
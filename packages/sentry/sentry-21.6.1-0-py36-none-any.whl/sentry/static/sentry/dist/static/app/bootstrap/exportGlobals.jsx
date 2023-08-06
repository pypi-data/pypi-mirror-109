import { __assign, __awaiter, __generator, __read } from "tslib";
import * as React from 'react';
import ReactDOM from 'react-dom';
import * as Router from 'react-router';
import * as Sentry from '@sentry/react';
import createReactClass from 'create-react-class';
import jQuery from 'jquery';
import throttle from 'lodash/throttle';
import moment from 'moment';
import PropTypes from 'prop-types';
import Reflux from 'reflux';
import { Client } from 'app/api';
import plugins from 'app/plugins';
var globals = {
    // The following globals are used in sentry-plugins webpack externals
    // configuration.
    PropTypes: PropTypes,
    React: React,
    Reflux: Reflux,
    Router: Router,
    Sentry: Sentry,
    moment: moment,
    ReactDOM: {
        findDOMNode: ReactDOM.findDOMNode,
        render: ReactDOM.render,
    },
    // jQuery is still exported to the window as some bootsrap functionality
    // and legacy plugins like youtrack make use of it.
    $: jQuery,
    jQuery: jQuery,
    // django templates make use of these globals
    createReactClass: createReactClass,
    SentryApp: {},
};
// The SentryApp global contains exported app modules for use in javascript
// modules that are not compiled with the sentry bundle.
var SentryApp = {
    // The following components are used in sentry-plugins.
    Form: require('app/components/forms/form').default,
    FormState: require('app/components/forms/index').FormState,
    LoadingIndicator: require('app/components/loadingIndicator').default,
    plugins: {
        add: plugins.add,
        addContext: plugins.addContext,
        BasePlugin: plugins.BasePlugin,
        DefaultIssuePlugin: plugins.DefaultIssuePlugin,
    },
    // The following components are used in legacy django HTML views
    ConfigStore: require('app/stores/configStore').default,
    HookStore: require('app/stores/hookStore').default,
    Modal: require('app/actionCreators/modal'),
    getModalPortal: require('app/utils/getModalPortal').default,
};
/**
 * Wrap export so that we can track usage of these globals to determine how we want to handle deprecatation.
 * These are sent to Sentry install, which then checks to see if SENTRY_BEACON is enabled
 * in order to make a request to the SaaS beacon.
 */
var _beaconComponents = [];
var makeBeaconRequest = throttle(function () { return __awaiter(void 0, void 0, void 0, function () {
    var api, components, e_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                api = new Client();
                components = _beaconComponents;
                _beaconComponents = [];
                _a.label = 1;
            case 1:
                _a.trys.push([1, 3, , 4]);
                return [4 /*yield*/, api.requestPromise('/api/0/internal/beacon/', {
                        method: 'POST',
                        data: {
                            // Limit to first 20 components... if there are more than 20, then something
                            // is probably wrong.
                            batch_data: components.slice(0, 20).map(function (component) { return (__assign({ description: 'SentryApp' }, component)); }),
                        },
                    })];
            case 2:
                _a.sent();
                return [3 /*break*/, 4];
            case 3:
                e_1 = _a.sent();
                return [3 /*break*/, 4];
            case 4: return [2 /*return*/];
        }
    });
}); }, 5000, { trailing: true, leading: false });
/**
 * First checks if stacktrace should be ignored, and then returns
 * a scrubbed and limited stacktrace.
 *
 * Returns `null` if it should be ignored
 */
export function getCleanStack(stack) {
    // Scrub out any hostnames
    var scrubbedStack = stack.replace(/https?:\/\/.*?\//, '/');
    // This is an exclude list of strings. If any of these appear in the stack,
    // then it should be ignored.
    var excludeList = [
        '__puppeteer_evaluation_script__',
        '-extension',
        'papaparse',
        'AdGuard',
    ];
    if (excludeList.some(function (str) { return scrubbedStack.includes(str); })) {
        return null;
    }
    // Split stack by lines and filter out empty strings
    var stackArr = (scrubbedStack === null || scrubbedStack === void 0 ? void 0 : scrubbedStack.split('\n').filter(function (s) { return !!s; })) || [];
    // There's an issue with Firefox where this getter for jQuery gets called many times (> 100)
    // The stacktrace doesn't show it being called outside of this block either.
    // (this works fine in Chrome...)
    if (stackArr.length <= 1) {
        return null;
    }
    // First limit to last 5 frames and limit to first 1024 characters
    return stackArr.slice(0, 5).join('\n').slice(0, 1024);
}
[
    [SentryApp, globals.SentryApp],
    [globals, window],
].forEach(function (_a) {
    var _b = __read(_a, 2), obj = _b[0], parent = _b[1];
    var properties = Object.fromEntries(Object.entries(obj).map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return [
            key,
            {
                configurable: false,
                enumerable: false,
                get: function () {
                    var _a;
                    try {
                        var stack = getCleanStack((_a = new Error().stack) !== null && _a !== void 0 ? _a : '');
                        if (key !== 'SentryApp' && stack !== null) {
                            _beaconComponents.push({
                                component: key,
                                stack: stack,
                            });
                            makeBeaconRequest();
                        }
                    }
                    catch (_b) {
                        // Ignore errors
                    }
                    return value;
                },
            },
        ];
    }));
    Object.defineProperties(parent, properties);
});
export default globals;
//# sourceMappingURL=exportGlobals.jsx.map
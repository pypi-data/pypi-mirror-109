import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import LoadingIndicator from 'app/components/loadingIndicator';
import { PanelItem } from 'app/components/panels';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var ProjectPerformance = /** @class */ (function (_super) {
    __extends(ProjectPerformance, _super);
    function ProjectPerformance() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/", {
                method: 'DELETE',
                complete: function () { return _this.fetchData(); },
            });
        };
        return _this;
    }
    ProjectPerformance.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Performance'), projectId, false);
    };
    ProjectPerformance.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            ['threshold', "/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/"],
        ];
        return endpoints;
    };
    ProjectPerformance.prototype.getEmptyMessage = function () {
        return t('There is no threshold set for this project.');
    };
    ProjectPerformance.prototype.renderLoading = function () {
        return (<LoadingIndicatorContainer>
        <LoadingIndicator />
      </LoadingIndicatorContainer>);
    };
    Object.defineProperty(ProjectPerformance.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'threshold',
                    type: 'string',
                    label: t('Response Time Threshold'),
                    placeholder: t('300'),
                    help: t('Set a response time threshold to help define what satisfactory and tolerable times are. These will be reflected in the calculation of your Apdex, a standard measurement in performance monitoring and the User Misery score. You can customize this per project.'),
                },
                {
                    name: 'metric',
                    type: 'select',
                    label: t('Metric'),
                    choices: function () { return ['duration', 'lcp', 'fcp']; },
                    help: t('Set the measurement to apply the Response Time Threshold to. This metric will be used to calculate the Apdex and User Misery Scores.'),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectPerformance.prototype, "initialData", {
        get: function () {
            var threshold = this.state.threshold;
            return {
                threshold: threshold.threshold,
                metric: threshold.metric,
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectPerformance.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, project = _a.project;
        var endpoint = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
        return (<React.Fragment>
        <SettingsPageHeader title={t('Performance')}/>
        <Form saveOnBlur allowUndo initialData={this.initialData} apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={function (resp) {
                _this.setState({ threshold: resp });
            }}>
          <JsonForm title={t('General')} fields={this.formFields} renderFooter={function () { return (<Actions>
                <Button onClick={function () { return _this.handleDelete(); }}>
                  {t('Clear Custom Threshold')}
                </Button>
              </Actions>); }}/>
        </Form>
      </React.Fragment>);
    };
    return ProjectPerformance;
}(AsyncView));
var Actions = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var LoadingIndicatorContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 18px 18px 0;\n"], ["\n  margin: 18px 18px 0;\n"])));
export default ProjectPerformance;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectPerformance.jsx.map
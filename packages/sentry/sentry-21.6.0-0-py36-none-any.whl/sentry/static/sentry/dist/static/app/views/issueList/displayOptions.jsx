import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getDisplayLabel, IssueDisplayOptions } from 'app/views/issueList/utils';
var IssueListDisplayOptions = function (_a) {
    var onDisplayChange = _a.onDisplayChange, display = _a.display, hasSessions = _a.hasSessions, hasMultipleProjectsSelected = _a.hasMultipleProjectsSelected;
    var getMenuItem = function (key) {
        var tooltipText;
        var disabled = false;
        if (key === IssueDisplayOptions.SESSIONS) {
            if (hasMultipleProjectsSelected) {
                tooltipText = t('Select a project to view events as a % of sessions. This helps you get a better picture of how these errors affect your users.');
                disabled = true;
            }
            else if (!hasSessions) {
                tooltipText = t('The selected project does not have session data');
                disabled = true;
            }
        }
        return (<DropdownItem onSelect={onDisplayChange} eventKey={key} isActive={key === display} disabled={disabled}>
        <StyledTooltip containerDisplayMode="block" position="top" delay={500} title={tooltipText} disabled={!tooltipText}>
          {getDisplayLabel(key)}
        </StyledTooltip>
      </DropdownItem>);
    };
    return (<StyledDropdownControl buttonProps={{ prefix: t('Display') }} label={getDisplayLabel(display)}>
      <React.Fragment>
        {getMenuItem(IssueDisplayOptions.EVENTS)}
        {getMenuItem(IssueDisplayOptions.SESSIONS)}
      </React.Fragment>
    </StyledDropdownControl>);
};
var StyledDropdownControl = styled(DropdownControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledTooltip = styled(Tooltip)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default IssueListDisplayOptions;
var templateObject_1, templateObject_2;
//# sourceMappingURL=displayOptions.jsx.map
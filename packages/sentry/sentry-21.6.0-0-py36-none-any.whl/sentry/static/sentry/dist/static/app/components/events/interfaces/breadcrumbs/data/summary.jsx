import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import ContextData from 'app/components/contextData';
function Summary(_a) {
    var kvData = _a.kvData, children = _a.children, onToggle = _a.onToggle;
    function renderKvData() {
        if (!kvData || !Object.keys(kvData).length) {
            return null;
        }
        return <ContextData data={kvData} onToggle={onToggle} withAnnotatedText/>;
    }
    return (<StyledPre>
      <StyledCode>{children}</StyledCode>
      {renderKvData()}
    </StyledPre>);
}
export default Summary;
var StyledPre = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  background: none;\n  box-sizing: border-box;\n  white-space: pre-wrap;\n  word-break: break-all;\n  margin: 0;\n  font-size: ", ";\n"], ["\n  padding: 0;\n  background: none;\n  box-sizing: border-box;\n  white-space: pre-wrap;\n  word-break: break-all;\n  margin: 0;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledCode = styled('code')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  line-height: 26px;\n"], ["\n  white-space: pre-wrap;\n  line-height: 26px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=summary.jsx.map
import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import Card from 'app/components/card';
import { tn } from 'app/locale';
import space from 'app/styles/space';
function NewIssue(_a) {
    var sampleEvent = _a.sampleEvent, eventCount = _a.eventCount, isReloading = _a.isReloading;
    var title = sampleEvent.title, culprit = sampleEvent.culprit;
    return (<StyledCard interactive={false} isReloading={isReloading}>
      <div>
        <Title>{title}</Title>
        <CulPrint>{culprit}</CulPrint>
      </div>
      <ErrorsCount>
        {eventCount}
        <ErrorLabel>{tn('Error', 'Errors', eventCount)}</ErrorLabel>
      </ErrorsCount>
    </StyledCard>);
}
export default NewIssue;
var StyledCard = styled(Card)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -1px;\n  overflow: hidden;\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  padding: ", " ", ";\n  grid-gap: ", ";\n  word-break: break-word;\n  ", "\n"], ["\n  margin-bottom: -1px;\n  overflow: hidden;\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  padding: ", " ", ";\n  grid-gap: ", ";\n  word-break: break-word;\n  ",
    "\n"])), space(1.5), space(2), space(2), function (p) {
    return p.isReloading &&
        "\n      opacity: 0.5;\n      pointer-events: none;\n    ";
});
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 700;\n"], ["\n  font-size: ", ";\n  font-weight: 700;\n"])), function (p) { return p.theme.fontSizeLarge; });
var CulPrint = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ErrorsCount = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  justify-items: center;\n"], ["\n  display: grid;\n  align-items: center;\n  justify-items: center;\n"])));
var ErrorLabel = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-weight: 500;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  text-transform: uppercase;\n  font-weight: 500;\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=newIssue.jsx.map
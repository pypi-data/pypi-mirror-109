import { __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { parseSearch, Token } from './parser';
var ResultRenderer = /** @class */ (function () {
    function ResultRenderer() {
        var _this = this;
        this.renderFilter = function (filter) { return (<FilterToken>
      {filter.negated && <Negation>!</Negation>}
      {_this.renderKey(filter.key, filter.negated)}
      {filter.operator && <Operator>{filter.operator}</Operator>}
      <Value>{_this.renderToken(filter.value)}</Value>
    </FilterToken>); };
        this.renderKey = function (key, negated) {
            var value = key.text;
            if (key.type === Token.KeyExplicitTag) {
                value = (<ExplicitKey prefix={key.prefix}>
          {key.key.quoted ? "\"" + key.key.value + "\"" : key.key.value}
        </ExplicitKey>);
            }
            return <Key negated={!!negated}>{value}:</Key>;
        };
        this.renderList = function (token) { return (<InList>
      {token.items.map(function (_a) {
                var value = _a.value, separator = _a.separator;
                return [
                    <ListComma key="comma">{separator}</ListComma>,
                    _this.renderToken(value),
                ];
            })}
    </InList>); };
        this.renderNumber = function (token) { return (<Fragment>
      {token.value}
      <Unit>{token.unit}</Unit>
    </Fragment>); };
        this.renderToken = function (token) {
            switch (token.type) {
                case Token.Spaces:
                    return token.value;
                case Token.Filter:
                    return _this.renderFilter(token);
                case Token.LogicGroup:
                    return <LogicGroup>{_this.renderResult(token.inner)}</LogicGroup>;
                case Token.LogicBoolean:
                    return <LogicBoolean>{token.value}</LogicBoolean>;
                case Token.ValueBoolean:
                    return <Boolean>{token.text}</Boolean>;
                case Token.ValueIso8601Date:
                    return <DateTime>{token.text}</DateTime>;
                case Token.ValueTextList:
                case Token.ValueNumberList:
                    return _this.renderList(token);
                case Token.ValueNumber:
                    return _this.renderNumber(token);
                default:
                    return token.text;
            }
        };
        this.renderResult = function (result) {
            return result
                .map(_this.renderToken)
                .map(function (renderedToken, i) { return <Fragment key={i}>{renderedToken}</Fragment>; });
        };
    }
    return ResultRenderer;
}());
var renderer = new ResultRenderer();
export default function renderQuery(query) {
    var result = query;
    try {
        var parseResult = parseSearch(query);
        result = renderer.renderResult(parseResult);
    }
    catch (err) {
        // eslint-disable-next-line no-console
        console.log(err);
    }
    return <SearchQuery>{result}</SearchQuery>;
}
var SearchQuery = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  font-family: ", ";\n"], ["\n  font-size: ", ";\n  font-family: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; });
var FilterToken = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var filterCss = function (theme) { return css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  border: 0.5px solid ", ";\n  padding: ", " 0;\n"], ["\n  background: ", ";\n  border: 0.5px solid ", ";\n  padding: ", " 0;\n"])), theme.searchTokenBackground, theme.searchTokenBorder, space(0.25)); };
var Negation = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"], ["\n  ", ";\n  border-right: none;\n  padding-left: 1px;\n  margin-left: -2px;\n  font-weight: bold;\n  border-radius: 2px 0 0 2px;\n  color: ", ";\n"])), function (p) { return filterCss(p.theme); }, function (p) { return p.theme.red300; });
var Key = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ", ";\n"], ["\n  ", ";\n  border-right: none;\n  font-weight: bold;\n  ",
    ";\n"])), function (p) { return filterCss(p.theme); }, function (p) {
    return !p.negated
        ? css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "], ["\n          border-radius: 2px 0 0 2px;\n          padding-left: 1px;\n          margin-left: -2px;\n        "]))) : css(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n          border-left: none;\n          margin-left: 0;\n        "], ["\n          border-left: none;\n          margin-left: 0;\n        "])));
});
var ExplicitKey = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"], ["\n  &:before,\n  &:after {\n    color: ", ";\n  }\n  &:before {\n    content: '", "[';\n  }\n  &:after {\n    content: ']';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.prefix; });
var Operator = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"], ["\n  ", ";\n  border-left: none;\n  border-right: none;\n  margin: -1px 0;\n  color: ", ";\n"])), function (p) { return filterCss(p.theme); }, function (p) { return p.theme.orange400; });
var Value = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: ", ";\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"], ["\n  ", ";\n  border-left: none;\n  border-radius: 0 2px 2px 0;\n  color: ", ";\n  margin: -1px -2px -1px 0;\n  padding-right: 1px;\n"])), function (p) { return filterCss(p.theme); }, function (p) { return p.theme.blue300; });
var Unit = styled('span')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var LogicBoolean = styled('span')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n"], ["\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
var Boolean = styled('span')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.pink300; });
var DateTime = styled('span')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.green300; });
var ListComma = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var InList = styled('span')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"], ["\n  &:before {\n    content: '[';\n    font-weight: bold;\n    color: ", ";\n  }\n  &:after {\n    content: ']';\n    font-weight: bold;\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, Value, function (p) { return p.theme.purple300; });
var LogicGroup = styled('span')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  &:before,\n  &:after {\n    position: relative;\n    font-weight: bold;\n    color: ", ";\n    padding: 3px 0;\n    background: ", ";\n    border-radius: 1px;\n  }\n  &:before {\n    left: -3px;\n    content: '(';\n  }\n  &:after {\n    right: -3px;\n    content: ')';\n  }\n"], ["\n  &:before,\n  &:after {\n    position: relative;\n    font-weight: bold;\n    color: ", ";\n    padding: 3px 0;\n    background: ", ";\n    border-radius: 1px;\n  }\n  &:before {\n    left: -3px;\n    content: '(';\n  }\n  &:after {\n    right: -3px;\n    content: ')';\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.red200; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=renderer.jsx.map
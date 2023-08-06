import { __assign, __awaiter, __generator, __makeTemplateObject, __read } from "tslib";
import { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { DEFAULT_DEBOUNCE_DURATION } from 'app/constants';
import { IconFlag } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import withApi from 'app/utils/withApi';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import RangeSlider from 'app/views/settings/components/forms/controls/rangeSlider';
import NewIssue from './newIssue';
function Grouping(_a) {
    var _b, _c, _d;
    var api = _a.api, groupId = _a.groupId, location = _a.location;
    var _e = __read(useState(false), 2), isLoading = _e[0], setIsLoading = _e[1];
    var _f = __read(useState(false), 2), isGroupingLevelDetailsLoading = _f[0], setIsGroupingLevelDetailsLoading = _f[1];
    var _g = __read(useState(undefined), 2), error = _g[0], setError = _g[1];
    var _h = __read(useState([]), 2), groupingLevels = _h[0], setGroupingLevels = _h[1];
    var _j = __read(useState(undefined), 2), activeGroupingLevel = _j[0], setActiveGroupingLevel = _j[1];
    var _k = __read(useState([]), 2), activeGroupingLevelDetails = _k[0], setActiveGroupingLevelDetails = _k[1];
    var _l = __read(useState(''), 2), pagination = _l[0], setPagination = _l[1];
    useEffect(function () {
        fetchGroupingLevels();
    }, []);
    useEffect(function () {
        setCurrentGrouping();
    }, [groupingLevels]);
    useEffect(function () {
        fetchGroupingLevelDetails();
    }, [activeGroupingLevel, location.query]);
    var handleSetActiveGroupingLevel = debounce(function (groupingLevelId) {
        setActiveGroupingLevel(Number(groupingLevelId));
    }, DEFAULT_DEBOUNCE_DURATION);
    function fetchGroupingLevels() {
        return __awaiter(this, void 0, void 0, function () {
            var response, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        setError(undefined);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/")];
                    case 2:
                        response = _a.sent();
                        setIsLoading(false);
                        setGroupingLevels(response.levels);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        setIsLoading(false);
                        setError(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function fetchGroupingLevelDetails() {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var _b, response, xhr, pageLinks, err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (!groupingLevels.length) {
                            return [2 /*return*/];
                        }
                        setIsGroupingLevelDetailsLoading(true);
                        setError(undefined);
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/" + activeGroupingLevel + "/new-issues/", {
                                method: 'GET',
                                includeAllArgs: true,
                                query: __assign(__assign({}, location.query), { per_page: 10 }),
                            })];
                    case 2:
                        _b = __read.apply(void 0, [_c.sent(), 3]), response = _b[0], xhr = _b[2];
                        pageLinks = xhr && ((_a = xhr.getResponseHeader) === null || _a === void 0 ? void 0 : _a.call(xhr, 'Link'));
                        setPagination(pageLinks !== null && pageLinks !== void 0 ? pageLinks : '');
                        setActiveGroupingLevelDetails(Array.isArray(response) ? response : [response]);
                        setIsGroupingLevelDetailsLoading(false);
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        setIsGroupingLevelDetailsLoading(false);
                        setError(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function setCurrentGrouping() {
        var currentGrouping = groupingLevels.find(function (groupingLevel) { return groupingLevel.isCurrent; });
        if (!currentGrouping) {
            return;
        }
        setActiveGroupingLevel(Number(currentGrouping.id));
    }
    if (isLoading) {
        return <LoadingIndicator />;
    }
    if (error) {
        if (error.status === 403 && ((_b = error.responseJSON) === null || _b === void 0 ? void 0 : _b.detail)) {
            var _m = error.responseJSON.detail, message = _m.message, code = _m.code;
            return (<Wrapper>
          <EmptyMessage size="large" icon={<IconFlag size="xl"/>} action={code === 'merged_issues' ? (<Button to={"/organizations/sentry/issues/" + groupId + "/merged/?" + location.search}>
                  {t('Unmerge issue')}
                </Button>) : undefined}>
            {message}
          </EmptyMessage>
        </Wrapper>);
        }
        return (<LoadingError message={t('Unable to load grouping levels, please try again later')} onRetry={fetchGroupingLevels}/>);
    }
    if (!groupingLevels.length) {
        return (<EmptyStateWarning withIcon={false}>
        {t('No grouping levels have been found.')}
      </EmptyStateWarning>);
    }
    var links = parseLinkHeader(pagination);
    var hasMore = ((_c = links.previous) === null || _c === void 0 ? void 0 : _c.results) || ((_d = links.next) === null || _d === void 0 ? void 0 : _d.results);
    return (<Wrapper>
      <Description>
        {t('Sometimes you might want to split up issues by additional frames or other criteria. Select a granularity level below and see how many new issues will be created in the process.')}
      </Description>
      <div>
        <StyledList symbol="colored-numeric">
          <StyledListItem>
            {t('Select level')}
            <StyledRangeSlider name="grouping-level" allowedValues={groupingLevels.map(function (groupingLevel) {
            return Number(groupingLevel.id);
        })} formatLabel={function (value) {
            return value === 0 ? t('Automatically grouped') : t('Level %s', value);
        }} value={activeGroupingLevel !== null && activeGroupingLevel !== void 0 ? activeGroupingLevel : 0} onChange={handleSetActiveGroupingLevel}/>
          </StyledListItem>
          <StyledListItem>
            <div>
              {t('What happens to this issue')}
              <WhatHappensDescription>
                {tct("This issue will be deleted and [quantity] new issues will be created.", {
            quantity: hasMore
                ? activeGroupingLevelDetails.length + "+"
                : activeGroupingLevelDetails.length,
        })}
              </WhatHappensDescription>
            </div>
            <NewIssues>
              {activeGroupingLevelDetails.map(function (_a) {
            var hash = _a.hash, latestEvent = _a.latestEvent, eventCount = _a.eventCount;
            return (<NewIssue key={hash} sampleEvent={latestEvent} eventCount={eventCount} isReloading={isGroupingLevelDetailsLoading}/>);
        })}
            </NewIssues>
          </StyledListItem>
        </StyledList>
        <Pagination pageLinks={pagination}/>
      </div>
    </Wrapper>);
}
export default withApi(Grouping);
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  background: ", ";\n  grid-gap: ", ";\n  margin: -", " -", ";\n  padding: ", " ", ";\n"], ["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  background: ", ";\n  grid-gap: ", ";\n  margin: -", " -", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.background; }, space(2), space(3), space(4), space(3), space(4));
var Description = styled('p')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(0.5));
var StyledListItem = styled(ListItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var StyledRangeSlider = styled(RangeSlider)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  max-width: 300px;\n"], ["\n  max-width: 300px;\n"])));
var StyledList = styled(List)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(2), function (p) { return p.theme.fontSizeExtraLarge; });
var NewIssues = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var WhatHappensDescription = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=grouping.jsx.map
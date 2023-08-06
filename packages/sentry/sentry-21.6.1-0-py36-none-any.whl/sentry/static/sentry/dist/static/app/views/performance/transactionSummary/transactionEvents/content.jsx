import { __assign, __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { Fragment } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import TransactionsTable from 'app/components/discover/transactionsTable';
import SearchBar from 'app/components/events/searchBar';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import * as Layout from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Pagination from 'app/components/pagination';
import { t } from 'app/locale';
import space from 'app/styles/space';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { updateQuery } from 'app/views/eventsV2/table/cellAction';
import { getCurrentLandingDisplay, LandingDisplayField } from '../../landing/utils';
import TransactionHeader, { Tab } from '../header';
import { generateTraceLink, generateTransactionLink } from '../utils';
var DEFAULT_TRANSACTION_LIMIT = 50;
var EventsPageContent = /** @class */ (function (_super) {
    __extends(EventsPageContent, _super);
    function EventsPageContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleCursor = function (cursor, pathname, query) {
            var _a;
            var cursorName = _this.props.cursorName;
            browserHistory.push({
                pathname: pathname,
                query: __assign(__assign({}, query), (_a = {}, _a[cursorName] = cursor, _a)),
            });
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeTag('transaction');
                updateQuery(searchConditions, action, column, value);
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: stringifyQueryObject(searchConditions) }),
                });
            };
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        return _this;
    }
    EventsPageContent.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, eventView = _b.eventView, location = _b.location, organization = _b.organization, projects = _b.projects, transactionName = _b.transactionName, limit = _b.limit, cursorName = _b.cursorName;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var transactionsListEventView = eventView.clone();
        var transactionsListTitles = [
            t('event id'),
            t('user'),
            t('operation duration'),
            t('total duration'),
            t('trace id'),
            t('timestamp'),
        ];
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<Fragment>
        <TransactionHeader eventView={transactionsListEventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.Events} hasWebVitals={getCurrentLandingDisplay(location, projects, eventView).field ===
                LandingDisplayField.FRONTEND_PAGELOAD} handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          <StyledSdkUpdatesAlert />
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            <Search {...this.props}/>
            <StyledTable>
              <DiscoverQuery location={location} eventView={transactionsListEventView} orgSlug={organization.slug} limit={limit} cursor={cursor} referrer="api.discover.transactions-list">
                {function (_a) {
                var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData;
                return (<React.Fragment>
                      <TransactionsTable eventView={eventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} columnOrder={eventView.getColumns()} titles={transactionsListTitles} handleCellAction={_this.handleCellAction} generateLink={{
                        id: generateTransactionLink(transactionName),
                        trace: generateTraceLink(eventView.normalizeDateSelection(location)),
                    }} baselineTransactionName={null} baselineData={null}/>
                      <Pagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
                    </React.Fragment>);
            }}
              </DiscoverQuery>
            </StyledTable>
          </Layout.Main>
        </Layout.Body>
      </Fragment>);
    };
    EventsPageContent.defaultProps = {
        cursorName: 'transactionCursor',
        limit: DEFAULT_TRANSACTION_LIMIT,
    };
    return EventsPageContent;
}(React.Component));
var Search = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization;
    var handleSearch = function (query) {
        var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
        // do not propagate pagination when making a new search
        var searchQueryParams = omit(queryParams, 'cursor');
        browserHistory.push({
            pathname: location.pathname,
            query: searchQueryParams,
        });
    };
    var query = decodeScalar(location.query.query, '');
    return (<StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>);
};
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledTable = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n  padding-top: ", ";\n"], ["\n  flex-grow: 1;\n  padding-top: ", ";\n"])), space(2));
var StyledSdkUpdatesAlert = styled(GlobalSdkUpdateAlert)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
export default EventsPageContent;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map
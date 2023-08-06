import { BreadcrumbType } from 'app/types/breadcrumbs';
import Default from './default';
import Exception from './exception';
import Http from './http';
var Data = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm, onToggle = _a.onToggle;
    if (breadcrumb.type === BreadcrumbType.HTTP) {
        return <Http breadcrumb={breadcrumb} searchTerm={searchTerm} onToggle={onToggle}/>;
    }
    if (breadcrumb.type === BreadcrumbType.WARNING ||
        breadcrumb.type === BreadcrumbType.ERROR) {
        return (<Exception breadcrumb={breadcrumb} searchTerm={searchTerm} onToggle={onToggle}/>);
    }
    return (<Default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm} onToggle={onToggle}/>);
};
export default Data;
//# sourceMappingURL=index.jsx.map
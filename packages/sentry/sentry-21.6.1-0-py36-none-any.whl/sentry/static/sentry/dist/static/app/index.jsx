import { __awaiter, __generator } from "tslib";
import { bootstrap } from 'app/bootstrap';
import { initializeMain } from 'app/bootstrap/initializeMain';
function app() {
    return __awaiter(this, void 0, void 0, function () {
        var data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, bootstrap()];
                case 1:
                    data = _a.sent();
                    initializeMain(data);
                    return [2 /*return*/];
            }
        });
    });
}
app();
//# sourceMappingURL=index.jsx.map
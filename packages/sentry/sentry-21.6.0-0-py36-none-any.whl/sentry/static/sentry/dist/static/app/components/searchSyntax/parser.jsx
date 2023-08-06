var _a;
import { __assign, __read, __spreadArray } from "tslib";
import moment from 'moment';
import grammar from './grammar.pegjs';
var listJoiner = function (_a) {
    var _b = __read(_a, 4), s1 = _b[0], comma = _b[1], s2 = _b[2], value = _b[3];
    return ({
        separator: [s1.value, comma, s2.value].join(''),
        value: value,
    });
};
/**
 * A token represents a node in the syntax tree. These are all extrapolated
 * from the grammar and may not be named exactly the same.
 */
export var Token;
(function (Token) {
    Token["Spaces"] = "spaces";
    Token["Filter"] = "filter";
    Token["FreeText"] = "freeText";
    Token["LogicGroup"] = "logicGroup";
    Token["LogicBoolean"] = "logicBoolean";
    Token["KeySimple"] = "keySimple";
    Token["KeyExplicitTag"] = "keyExplicitTag";
    Token["KeyAggregate"] = "keyAggregate";
    Token["KeyAggregateArgs"] = "keyAggregateArgs";
    Token["ValueIso8601Date"] = "valueIso8601Date";
    Token["ValueRelativeDate"] = "valueRelativeDate";
    Token["ValueDuration"] = "valueDuration";
    Token["ValuePercentage"] = "valuePercentage";
    Token["ValueBoolean"] = "valueBoolean";
    Token["ValueNumber"] = "valueNumber";
    Token["ValueText"] = "valueText";
    Token["ValueNumberList"] = "valueNumberList";
    Token["ValueTextList"] = "valueTextList";
})(Token || (Token = {}));
/**
 * An operator in a key value term
 */
export var TermOperator;
(function (TermOperator) {
    TermOperator["Default"] = "";
    TermOperator["GreaterThanEqual"] = ">=";
    TermOperator["LessThanEqual"] = "<=";
    TermOperator["GreaterThan"] = ">";
    TermOperator["LessThan"] = "<";
    TermOperator["Equal"] = "=";
    TermOperator["NotEqual"] = "!=";
})(TermOperator || (TermOperator = {}));
/**
 * Logic operators
 */
export var BooleanOperator;
(function (BooleanOperator) {
    BooleanOperator["And"] = "AND";
    BooleanOperator["Or"] = "OR";
})(BooleanOperator || (BooleanOperator = {}));
/**
 * The Token.Filter may be one of many types of filters. This enum declares the
 * each variant filter type.
 */
export var FilterType;
(function (FilterType) {
    FilterType["Text"] = "text";
    FilterType["TextIn"] = "textIn";
    FilterType["Date"] = "date";
    FilterType["SpecificDate"] = "specificDate";
    FilterType["RelativeDate"] = "relativeDate";
    FilterType["Duration"] = "duration";
    FilterType["Numeric"] = "numeric";
    FilterType["NumericIn"] = "numericIn";
    FilterType["Boolean"] = "boolean";
    FilterType["AggregateSimple"] = "aggregateSimple";
    FilterType["AggregateDate"] = "aggregateDate";
    FilterType["AggregateRelativeDate"] = "aggregateRelativeDate";
    FilterType["Has"] = "has";
    FilterType["Is"] = "is";
})(FilterType || (FilterType = {}));
var allOperators = [
    TermOperator.Default,
    TermOperator.GreaterThanEqual,
    TermOperator.LessThanEqual,
    TermOperator.GreaterThan,
    TermOperator.LessThan,
    TermOperator.Equal,
    TermOperator.NotEqual,
];
var textKeys = [Token.KeySimple, Token.KeyExplicitTag];
var numberUnits = {
    b: 1000000000,
    m: 1000000,
    k: 1000,
};
/**
 * This constant-type configuration object declares how each filter type
 * operates. Including what types of keys, operators, and values it may
 * recieve.
 *
 * This configuration is used to generate the discriminate Filter type that is
 * returned from the tokenFilter converter.
 */
export var filterTypeConfig = (_a = {},
    _a[FilterType.Text] = {
        validKeys: textKeys,
        validOps: [],
        validValues: [Token.ValueText],
        canNegate: true,
    },
    _a[FilterType.TextIn] = {
        validKeys: textKeys,
        validOps: [],
        validValues: [Token.ValueTextList],
        canNegate: true,
    },
    _a[FilterType.Date] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    _a[FilterType.SpecificDate] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    _a[FilterType.RelativeDate] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueRelativeDate],
        canNegate: false,
    },
    _a[FilterType.Duration] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueDuration],
        canNegate: false,
    },
    _a[FilterType.Numeric] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueNumber],
        canNegate: false,
    },
    _a[FilterType.NumericIn] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueNumberList],
        canNegate: false,
    },
    _a[FilterType.Boolean] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueBoolean],
        canNegate: true,
    },
    _a[FilterType.AggregateSimple] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueDuration, Token.ValueNumber, Token.ValuePercentage],
        canNegate: true,
    },
    _a[FilterType.AggregateDate] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: true,
    },
    _a[FilterType.AggregateRelativeDate] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueRelativeDate],
        canNegate: true,
    },
    _a[FilterType.Has] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [],
        canNegate: true,
    },
    _a[FilterType.Is] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueText],
        canNegate: true,
    },
    _a);
/**
 * Used to construct token results via the token grammar
 */
var TokenConverter = /** @class */ (function () {
    function TokenConverter(text, location) {
        var _this = this;
        /**
         * Creates a token with common `text` and `location` keys.
         */
        this.makeToken = function (args) { return (__assign({ text: _this.text(), location: _this.location() }, args)); };
        this.tokenSpaces = function (value) {
            return _this.makeToken({
                type: Token.Spaces,
                value: value,
            });
        };
        this.tokenFilter = function (type, key, value, operator, negated) {
            return _this.makeToken({
                type: Token.Filter,
                filter: type,
                config: filterTypeConfig[type],
                negated: negated,
                key: key,
                operator: operator !== null && operator !== void 0 ? operator : TermOperator.Default,
                value: value,
            });
        };
        this.tokenFreeText = function (value, quoted) {
            return _this.makeToken({
                type: Token.FreeText,
                value: value,
                quoted: quoted,
            });
        };
        this.tokenLogicGroup = function (inner) {
            return _this.makeToken({
                type: Token.LogicGroup,
                inner: inner,
            });
        };
        this.tokenLogicBoolean = function (bool) {
            return _this.makeToken({
                type: Token.LogicBoolean,
                value: bool,
            });
        };
        this.tokenKeySimple = function (value, quoted) {
            return _this.makeToken({
                type: Token.KeySimple,
                value: value,
                quoted: quoted,
            });
        };
        this.tokenKeyExplicitTag = function (prefix, key) {
            return _this.makeToken({
                type: Token.KeyExplicitTag,
                prefix: prefix,
                key: key,
            });
        };
        this.tokenKeyAggregate = function (name, args, argsSpaceBefore, argsSpaceAfter) {
            return _this.makeToken({
                type: Token.KeyAggregate,
                name: name,
                args: args,
                argsSpaceBefore: argsSpaceBefore,
                argsSpaceAfter: argsSpaceAfter,
            });
        };
        this.tokenKeyAggregateArgs = function (arg1, args) {
            return _this.makeToken({
                type: Token.KeyAggregateArgs,
                args: __spreadArray([{ separator: '', value: arg1 }], __read(args.map(listJoiner))),
            });
        };
        this.tokenValueIso8601Date = function (value) {
            return _this.makeToken({
                type: Token.ValueIso8601Date,
                value: moment(value),
            });
        };
        this.tokenValueRelativeDate = function (value, sign, unit) {
            return _this.makeToken({
                type: Token.ValueRelativeDate,
                value: Number(value),
                sign: sign,
                unit: unit,
            });
        };
        this.tokenValueDuration = function (value, unit) {
            return _this.makeToken({
                type: Token.ValueDuration,
                value: Number(value),
                unit: unit,
            });
        };
        this.tokenValuePercentage = function (value) {
            return _this.makeToken({
                type: Token.ValuePercentage,
                value: Number(value),
            });
        };
        this.tokenValueBoolean = function (value) {
            return _this.makeToken({
                type: Token.ValueBoolean,
                value: ['1', 'true'].includes(value.toLowerCase()),
            });
        };
        this.tokenValueNumber = function (value, unit) {
            var _a;
            return _this.makeToken({
                type: Token.ValueNumber,
                value: value,
                rawValue: Number(value) * ((_a = numberUnits[unit]) !== null && _a !== void 0 ? _a : 1),
                unit: unit,
            });
        };
        this.tokenValueText = function (value, quoted) {
            return _this.makeToken({
                type: Token.ValueText,
                value: value,
                quoted: quoted,
            });
        };
        this.tokenValueNumberList = function (item1, items) {
            return _this.makeToken({
                type: Token.ValueNumberList,
                items: __spreadArray([{ separator: '', value: item1 }], __read(items.map(listJoiner))),
            });
        };
        this.tokenValueTextList = function (item1, items) {
            return _this.makeToken({
                type: Token.ValueTextList,
                items: __spreadArray([{ separator: '', value: item1 }], __read(items.map(listJoiner))),
            });
        };
        this.text = text;
        this.location = location;
    }
    return TokenConverter;
}());
var options = {
    TokenConverter: TokenConverter,
    TermOperator: TermOperator,
    FilterType: FilterType,
};
export function parseSearch(query) {
    return grammar.parse(query, options);
}
//# sourceMappingURL=parser.jsx.map
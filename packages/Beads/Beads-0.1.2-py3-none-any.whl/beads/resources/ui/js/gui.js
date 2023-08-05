var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
/**
 * Convenience Wrapper for 'eel' object.
 * Can be accessed via const EEL.
 */
var EelWrapper = /** @class */ (function () {
    function EelWrapper() {
    }
    EelWrapper.prototype.parse = function (fsm, language, opts, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var graph, options, _a, code, error;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        graph = JSON.stringify(fsm);
                        options = JSON.stringify(opts);
                        return [4 /*yield*/, eel.parse(graph, language, options)()];
                    case 1:
                        _a = _b.sent(), code = _a[0], error = _a[1];
                        callback(code, error);
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.prototype.getVersion = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var version;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, eel.get_version()()];
                    case 1:
                        version = _a.sent();
                        callback(version);
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.prototype.getInfo = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var info;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, eel.get_info()()];
                    case 1:
                        info = _a.sent();
                        callback(info);
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.prototype.availableLanguages = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var available;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, eel.available_languages()()];
                    case 1:
                        available = _a.sent();
                        callback(JSON.parse(available)[EelWrapper.LANG]);
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.prototype.loadFile = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var graph;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, eel.load_file()()];
                    case 1:
                        graph = _a.sent();
                        callback(JSON.parse(graph));
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.prototype.setOption = function (option, value) {
        eel.set_option(option, value);
    };
    EelWrapper.prototype.unsetOption = function (option) {
        eel.unset_option(option);
    };
    EelWrapper.prototype.unsetAllOptions = function () {
        eel.unset_all_options();
    };
    EelWrapper.prototype.availableDefaults = function (callback) {
        return __awaiter(this, void 0, void 0, function () {
            var defaults;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, eel.available_defaults()()];
                    case 1:
                        defaults = _a.sent();
                        callback(JSON.parse(defaults));
                        return [2 /*return*/];
                }
            });
        });
    };
    EelWrapper.LANG = 'languages';
    return EelWrapper;
}());
var EEL = new EelWrapper();
// https://stackoverflow.com/a/30832210
// Function to download data to a file
function download(data, filename, type) {
    var file = new Blob([data], { type: type });
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a_1 = document.createElement("a");
        var url_1 = URL.createObjectURL(file);
        a_1.href = url_1;
        a_1.download = filename;
        document.body.appendChild(a_1);
        a_1.click();
        setTimeout(function () {
            document.body.removeChild(a_1);
            window.URL.revokeObjectURL(url_1);
        }, 0);
    }
}
function graphCSSRules() {
    var style = "@import url('https://fonts.googleapis.com/css?family=Oswald:200'); * {font-family: 'Oswald', Courier, monospace;} ";
    for (var x = 0; x != document.styleSheets.length; x++) {
        var sheet = document.styleSheets[x];
        for (var y = 0; y != sheet.cssRules.length; y++) {
            var rule = sheet.cssRules[y];
            if (/svg|\.state|\.transition/g.test(rule.selectorText)) {
                var css = rule.cssText;
                var cutoff = '#graph-container';
                style += css.slice(css.lastIndexOf(cutoff) + cutoff.length);
            }
        }
    }
    return style;
}
function saveSVG() {
    if (graph.nodes.length !== 0) {
        download(svgToString(), filename() + ".svg", "image/svg+xml");
    }
    else {
        notifyOfEmptyGraph();
    }
}
function svgToString() {
    var svg = document.querySelector("svg").cloneNode(true);
    var styles = graphCSSRules();
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n        <svg \n            xmlns=\"http://www.w3.org/2000/svg\" \n            xmlns:cc=\"http://creativecommons.org/ns#\" \n            xmlns:dc=\"http://purl.org/dc/elements/1.1/\" \n            xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\" \n            xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n            xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\" \n            xmlns:svg=\"http://www.w3.org/2000/svg\" \n            height=\"210mm\" \n            width=\"297mm\" \n            viewBox=\"0 0 297 210\" \n            version=\"1.1\" \n            id=\"svg57\" \n            >\n            <defs id=\"defs51\" />\n            <sodipodi:namedview \n                id=\"base\" \n                pagecolor=\"#ffffff\" \n                bordercolor=\"#666666\" \n                borderopacity=\"1.0\" \n                inkscape:pageopacity=\"0.0\" \n                inkscape:pageshadow=\"2\" \n                inkscape:document-units=\"mm\" \n                inkscape:current-layer=\"layer1\" \n                showgrid=\"false\" \n                inkscape:window-width=\"2560\" \n                inkscape:window-height=\"1330\" \n                inkscape:window-maximized=\"1\" />\n            <style type=\"text/css\">" + styles + "</style>\n            <metadata id=\"metadata54\">\n                <rdf:RDF>\n                    <cc:Work rdf:about=\"\">\n                        <dc:format>image/svg+xml</dc:format>\n                        <dc:type rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" />\n                        <dc:title />\n                    </cc:Work>\n                </rdf:RDF>\n            </metadata>\n            <g transform=\"scale(0.25)\" inkscape:label=\"Ebene 1\" inkscape:groupmode=\"layer\" id=\"layer1\">" + svg.innerHTML + "</g>\n        </svg>\n    ";
}
var exchangeTypes = new Map([
    ["python", "py"],
    ["javascript", "js"],
    ["typescript", "ts"]
]);
function saveCode(code, language) {
    if (code && code.indexOf('ERROR') != 0) {
        var ending = language;
        if (exchangeTypes.has(language)) {
            ending = exchangeTypes.get(language);
        }
        download(code, filename() + "." + ending, "text/plain");
    }
    else {
        window.alert('There is no code to save!');
    }
}
function savePNG() {
    if (graph.nodes.length > 0) {
        //code adoption of https://stackoverflow.com/questions/3975499/convert-svg-to-image-jpeg-png-etc-in-the-browser
        var downloadPNG_1 = function (data, filename) {
            var evt = new MouseEvent("click", {
                view: window,
                bubbles: false,
                cancelable: true
            });
            var a = document.createElement("a");
            a.setAttribute("download", filename);
            a.setAttribute("href", data);
            a.setAttribute("target", '_blank');
            a.dispatchEvent(evt);
        };
        var canvas_1 = document.createElement("canvas");
        var container = document.getElementById('graph-container');
        canvas_1.width = container.offsetWidth;
        canvas_1.height = container.offsetHeight;
        var context = canvas_1.getContext("2d");
        context.clearRect(0, 0, container.offsetWidth, container.offsetHeight);
        //@ts-ignore
        var DOMURL_1 = window.URL || window.webkitURL || window;
        var img_1 = new Image();
        var svgBlob = new Blob([svgToString()], { type: "image/svg+xml;charset=utf-8" });
        var url_2 = DOMURL_1.createObjectURL(svgBlob);
        img_1.onload = function () {
            context.drawImage(img_1, 0, 0);
            DOMURL_1.revokeObjectURL(url_2);
            var imgURI = canvas_1
                .toDataURL("image/png")
                .replace("image/png", "image/octet-stream");
            downloadPNG_1(imgURI, filename() + ".png");
        };
        img_1.src = url_2;
    }
    else {
        notifyOfEmptyGraph();
    }
}
function saveJson() {
    if (graph.nodes.length > 0) {
        download(JSON.stringify(graph), filename() + ".json", 'text/json');
    }
    else {
        notifyOfEmptyGraph();
    }
}
function notifyOfEmptyGraph() {
    window.alert('Please draw a graph first before you save it!');
}
function filename() {
    return graph.name || 'graph';
}
var graph = {
    name: "unnamed_graph",
    nodes: [],
    transitions: []
};
var r = 50;
var i = 1, j = 1;
var mousedownNode = null;
var mousedownTransition = null;
var svg = d3.select("#graph-container").append("svg");
svg.on("dblclick", function () {
    if (d3.event.ctrlKey || d3.event.metaKey) {
        var _a = d3.mouse(this), x = _a[0], y = _a[1];
        graph.nodes.push({ x: x, y: y, id: defaultStateName() });
        render();
    }
});
// creating arrows
svg.append("defs").append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 0 10 10')
    .attr('refX', 9)
    .attr('refY', 5)
    .attr('markerWidth', 5)
    .attr('markerHeight', 5)
    .attr('orient', 'auto')
    .append("path")
    .attr("d", "M 0 0 L 10 5 L 0 10 z");
var arrow = svg.append('path')
    .attr('d', 'M 200,200 L 400,400')
    .attr('fill', '#000')
    .attr('stroke-width', '3px')
    .attr('stroke', '#000')
    .attr("marker-end", "url(#arrow)")
    .style("display", "none");
svg.on("mousemove", function () {
    if (mousedownNode != null) {
        var _a = d3.mouse(this), x = _a[0], y = _a[1];
        arrow
            .attr('d', "M " + mousedownNode.x + "," + mousedownNode.y + " L " + x + "," + y)
            .style("display", "block");
    }
    if (mousedownTransition != null) {
        var _b = d3.mouse(this), x = _b[0], y = _b[1];
        mousedownTransition.offset = { x: x, y: y };
        console.log(mousedownTransition.offset);
    }
    if (mousedownTransition || mousedownNode) {
        render();
    }
});
svg.on('mouseup', function () {
    mousedownNode = null;
    mousedownTransition = null;
    arrow.style("display", "none");
    render();
});
function render() {
    var node = svg.selectAll(".state").data(graph.nodes);
    var group = node.enter()
        .append("g")
        .classed("state", true)
        .on("click", function (state) {
        if (d3.event.shiftKey) {
            graph.nodes.splice(graph.nodes.indexOf(state), 1);
            graph.transitions = graph.transitions.filter(function (t) { return t.from != state.id && t.to != state.id; });
            render();
        }
        if (d3.event.altKey) {
            if (graph.transitions.find(function (t) { return t.from == state.id && t.to == state.id; }) !== undefined) {
                return;
            }
            var newTransition = {
                from: "" + state.id,
                to: "" + state.id,
                label: defaultTransitionName(),
                visible: true,
                offset: null
            };
            graph.transitions.push(newTransition);
            render();
        }
    })
        .on("mousedown", function (state) {
        mousedownNode = state;
    })
        .on("mouseup", function (state) {
        if (mousedownNode == null || mousedownNode == state) {
            return;
        }
        if (graph.transitions.find(function (t) { return t.from == mousedownNode.id && t.to == state.id; }) !== undefined) {
            return;
        }
        var newTransition = {
            from: "" + mousedownNode.id,
            to: "" + state.id,
            label: defaultTransitionName(),
            visible: true,
            offset: null
        };
        graph.transitions.push(newTransition);
        mousedownNode = null;
    });
    group.append("circle")
        .attr("r", r)
        .merge(node.select("circle"))
        .attr("cx", function (state) { return state.x; })
        .attr("cy", function (state) { return state.y; });
    group.append("text")
        .call(make_editable, "id")
        .attr("dominant-baseline", "middle")
        .attr("text-anchor", "middle")
        .merge(node.select("text"))
        .text(function (state) { return state.id; })
        .attr("x", function (state) { return state.x; })
        .attr("y", function (state) { return state.y; });
    node.exit().remove();
    var transition = svg.selectAll(".transition").data(graph.transitions);
    var tgroup = transition.enter()
        .append("g")
        .classed("transition", true)
        .on("mousedown", function (transition) {
        mousedownTransition = transition;
    })
        .on("click", function (d) {
        if (d3.event.shiftKey) {
            graph.transitions.splice(graph.transitions.indexOf(d), 1);
            render();
        }
    });
    tgroup.append("path")
        .attr('fill', 'none')
        .attr('stroke-width', '3px')
        .attr('stroke', '#000')
        .attr("marker-end", "url(#arrow)")
        .merge(transition.select("path"))
        .attr('d', function (d) {
        var from = graph.nodes.find(function (s) { return s.id == d.from; });
        var to = graph.nodes.find(function (s) { return s.id == d.to; });
        var xDiff = to.x - from.x;
        var yDiff = to.y - from.y;
        var arrowLength = Math.sqrt(xDiff * xDiff + yDiff * yDiff);
        var t = 0.5;
        if (from == to) {
            d.loop = true;
            var x = r * Math.cos(-Math.PI / 4);
            var y = r * Math.sin(-Math.PI / 4);
            return "M " + (from.x - x) + "," + (from.y + y) + " A 50,50 0,1,1 " + (to.x + x) + "," + (to.y + y);
        }
        if (arrowLength < 2 * r) {
            d.visible = false;
            return;
        }
        d.visible = true;
        // Q1
        if (to.y <= from.y && to.x >= from.x) {
            var a = Math.atan((from.y - to.y) / (to.x - from.x));
            var x = r * Math.cos(a);
            var y = r * Math.sin(a);
            if (d.offset != null) {
                var startX = from.x + x;
                var startY = from.y - y;
                var endX = to.x - x;
                var endY = to.y + y;
                var controlX = d.offset.x / (2 * t * (1 - t)) - startX * t / (2 * (1 - t)) - endX * (1 - t) / (2 * t);
                var controlY = d.offset.y / (2 * t * (1 - t)) - startY * t / (2 * (1 - t)) - endY * (1 - t) / (2 * t);
                return "M " + startX + "," + startY + " Q " + controlX + "," + controlY + " " + endX + "," + endY;
            }
            return "M " + (from.x + x) + "," + (from.y - y) + " L " + (to.x - x) + "," + (to.y + y);
        }
        // Q2
        if (to.y >= from.y && to.x >= from.x) {
            var a = Math.atan((to.y - from.y) / (to.x - from.x));
            var x = r * Math.cos(a);
            var y = r * Math.sin(a);
            if (d.offset != null) {
                var startX = from.x + x;
                var startY = from.y + y;
                var endX = to.x - x;
                var endY = to.y - y;
                var controlX = d.offset.x / (2 * t * (1 - t)) - startX * t / (2 * (1 - t)) - endX * (1 - t) / (2 * t);
                var controlY = d.offset.y / (2 * t * (1 - t)) - startY * t / (2 * (1 - t)) - endY * (1 - t) / (2 * t);
                return "M " + startX + "," + startY + " Q " + controlX + "," + controlY + " " + endX + "," + endY;
            }
            return "M " + (from.x + x) + "," + (from.y + y) + " L " + (to.x - x) + "," + (to.y - y);
        }
        // Q3
        if (to.y >= from.y && to.x <= from.x) {
            var a = Math.atan((to.y - from.y) / (from.x - to.x));
            var x = r * Math.cos(a);
            var y = r * Math.sin(a);
            if (d.offset != null) {
                var startX = from.x - x;
                var startY = from.y + y;
                var endX = to.x + x;
                var endY = to.y - y;
                var controlX = d.offset.x / (2 * t * (1 - t)) - startX * t / (2 * (1 - t)) - endX * (1 - t) / (2 * t);
                var controlY = d.offset.y / (2 * t * (1 - t)) - startY * t / (2 * (1 - t)) - endY * (1 - t) / (2 * t);
                return "M " + startX + "," + startY + " Q " + controlX + "," + controlY + " " + endX + "," + endY;
            }
            return "M " + (from.x - x) + "," + (from.y + y) + " L " + (to.x + x) + "," + (to.y - y);
        }
        // Q4
        if (to.y <= from.y && to.x <= from.x) {
            var a = Math.atan((from.y - to.y) / (from.x - to.x));
            var x = r * Math.cos(a);
            var y = r * Math.sin(a);
            if (d.offset != null) {
                var startX = from.x - x;
                var startY = from.y - y;
                var endX = to.x + x;
                var endY = to.y + y;
                var controlX = d.offset.x / (2 * t * (1 - t)) - startX * t / (2 * (1 - t)) - endX * (1 - t) / (2 * t);
                var controlY = d.offset.y / (2 * t * (1 - t)) - startY * t / (2 * (1 - t)) - endY * (1 - t) / (2 * t);
                return "M " + startX + "," + startY + " Q " + controlX + "," + controlY + " " + endX + "," + endY;
            }
            return "M " + (from.x - x) + "," + (from.y - y) + " L " + (to.x + x) + "," + (to.y + y);
        }
    });
    tgroup.append("text")
        .attr("dominant-baseline", "middle")
        .attr("text-anchor", "middle")
        .call(make_editable, "label")
        .merge(transition.select("text"))
        .text(function (d) { if (d.visible)
        return d.label; })
        .attr("x", function (d) {
        var from = graph.nodes.find(function (s) { return s.id == d.from; });
        var to = graph.nodes.find(function (s) { return s.id == d.to; });
        if (d.loop) {
            return from.x;
        }
        var x = to.x - from.x;
        return (d.offset == null) ? (from.x + 0.5 * x) : d.offset.x;
    })
        .attr("y", function (d) {
        var from = graph.nodes.find(function (s) { return s.id == d.from; });
        var to = graph.nodes.find(function (s) { return s.id == d.to; });
        if (d.loop) {
            return from.y - 140;
        }
        var y = to.y - from.y;
        return (d.offset == null) ? (from.y + 0.5 * y - 20) : (d.offset.y - 30);
    });
    transition.exit().remove();
    clearTimeout();
    setTimeout(displaySummary, 200);
}
render();
function make_editable(selection, field) {
    selection.on("click", function (d) {
        if (d3.event.ctrlKey || d3.event.shiftKey)
            return;
        var text = d3.select(this);
        var group = d3.select(this.parentNode);
        var bb = this.getBBox();
        var w = 100;
        var h = 30;
        var fo = group.append("foreignObject")
            .attr("x", bb.x - (w - bb.width) / 2)
            .attr("y", bb.y - (h - bb.height) / 2)
            .attr("width", w)
            .attr("height", h);
        var input = fo.append("xhtml:form")
            .append("input")
            .style("width", w + "px")
            .style("height", h + "px")
            .attr("type", "text")
            .attr("value", d[field])
            .classed("label-input", function () { this.focus(); this.select(); return true; });
        input.on("blur", function () { fo.remove(); });
        input.on("keypress", function () {
            var e = d3.event;
            if (e.keyCode == 13) {
                var new_text_1 = changedLabel(input, e);
                graph.transitions.forEach(function (transition) {
                    if (transition.from == d[field])
                        transition.from = new_text_1;
                    if (transition.to == d[field])
                        transition.to = new_text_1;
                });
                d[field] = new_text_1;
                text.text(function (d) { return d[field]; });
                fo.remove();
            }
        });
    });
}
function changedLabel(input, event) {
    input.on("blur", null);
    if (typeof (event.cancelBubble) !== 'undefined') {
        event.cancelBubble = true;
    }
    if (event.stopPropagation) {
        event.stopPropagation();
    }
    event.preventDefault();
    return clearText(input.property("value"));
}
// node dragging
var dragging;
d3.select(window)
    .on("keydown", function () {
    if (d3.event.ctrlKey || d3.event.metaKey) {
        dragging = true;
        svg.selectAll(".state").call(nodeDrag);
        svg.selectAll(".state").on("mousedown", null);
    }
})
    .on("keyup", function () {
    if (dragging) {
        dragging = false;
        svg.selectAll(".state").on('.drag', null);
        svg.selectAll(".state").on("mousedown", function (state) {
            mousedownNode = state;
        });
    }
});
var nodeDrag = d3.drag()
    .subject(function () {
    for (var i = graph.nodes.length - 1, state, x, y; i >= 0; --i) {
        state = graph.nodes[i];
        x = state.x - d3.event.x;
        y = state.y - d3.event.y;
        if (x * x + y * y < r * r)
            return state;
    }
})
    .on("start", function () {
    graph.nodes.splice(graph.nodes.indexOf(d3.event.subject), 1);
    graph.nodes.push(d3.event.subject);
    if (d3.event.ctrlKey) {
        d3.event.subject.active = true;
    }
})
    .on("drag", function () {
    d3.event.subject.x = d3.event.x;
    d3.event.subject.y = d3.event.y;
})
    .on("end", function () {
    d3.event.subject.active = false;
})
    .on("start.render drag.render end.render", render);
/**
 * Display the summary if no states are drawn. Otherwise hide it.
 */
function displaySummary() {
    d3.select('#summary').classed('hidden', !!graph.nodes.length);
}
/**
 * Clear text that is entered by the user from invalid characters.
 * If the result is invalid 'INVALID_NAME' will be returned instead.
 *
 * @param text User input
 */
function clearText(text) {
    text = text.replace(/[^A-Za-z0-9_]/g, "");
    if (!/^[A-Za-z]/.test(text)) {
        text = 'INVALID_NAME';
    }
    return text;
}
/**
 * Create a default name for new states.
 */
function defaultStateName() {
    var name = "state_" + i;
    i++;
    return name;
}
/**
 * Create a default name for new transitions.
 */
function defaultTransitionName() {
    var name = "transition_" + j;
    j++;
    return name;
}
/**
 * Load a graph into the gui on startup.
 * Will only apply if the user provided --file option with valid input.
 *
 * @param {Schema} graph The graph to draw
 */
function load_graph(loadedGraph) {
    if (loadedGraph) {
        graph.name = loadedGraph['name'];
        graph.nodes = loadedGraph['nodes'];
        graph.transitions = loadedGraph['transitions'];
        render();
    }
    d3.select('#graph-name-field').attr('value', graph.name);
}
EEL.loadFile(load_graph);
var Creator = /** @class */ (function () {
    function Creator() {
    }
    Creator.prototype.create = function (tagName, options) {
        var element = document.createElement(tagName);
        if (options) {
            var content = options['content'];
            if (content) {
                if (typeof (content) === 'string') {
                    element.innerHTML = content;
                }
                else {
                    for (var _i = 0, content_1 = content; _i < content_1.length; _i++) {
                        var node = content_1[_i];
                        element.appendChild(node);
                    }
                }
            }
            var src = options['src'];
            if (src) {
                element.setAttribute('src', src);
            }
            var type = options['type'];
            if (type) {
                element.setAttribute("type", type);
            }
            var value = options['value'];
            if (value) {
                element.setAttribute("value", value);
            }
            var id = options['id'];
            if (id) {
                element.setAttribute('id', id);
            }
            var classList = options['classList'];
            if (classList) {
                element.setAttribute('class', classList);
            }
            if (options['disabled']) {
                element.setAttribute("disabled", "disabled");
            }
        }
        return element;
    };
    return Creator;
}());
/**
 * Wrapper class for a DOM HTMLElement.
 */
var ElementWrapper = /** @class */ (function (_super) {
    __extends(ElementWrapper, _super);
    function ElementWrapper(element) {
        var _this = _super.call(this) || this;
        _this.element = element;
        return _this;
    }
    ElementWrapper.prototype.appendSelf = function (container) {
        container.appendChild(this.element);
    };
    return ElementWrapper;
}(Creator));
/**
 * Class providing simple selection functionality thoughout the project.
 */
var SelectionHandler = /** @class */ (function (_super) {
    __extends(SelectionHandler, _super);
    function SelectionHandler(element, creator) {
        var _this = _super.call(this, element) || this;
        _this.mappedElements = new Map();
        _this.creator = creator;
        _this.selected = undefined;
        return _this;
    }
    SelectionHandler.prototype.createOption = function (id, cascadeSelection) {
        if (this.creator) {
            var option = this.creator(id);
            this.addOption(option, cascadeSelection);
            this.element.appendChild(option);
        }
    };
    SelectionHandler.prototype.addOption = function (option, cascadeSelection) {
        var _this = this;
        this.mappedElements.set(option, cascadeSelection);
        option.addEventListener("click", function () { return _this.select(option); }, false);
    };
    SelectionHandler.prototype.select = function (selection) {
        var currentSelection = this.selected;
        var isSelect = selection !== currentSelection;
        if (currentSelection) {
            var cascadeSelection = this.mappedElements.get(currentSelection);
            this.selectInternal(currentSelection, false, cascadeSelection);
            this.selected = undefined;
        }
        if (isSelect) {
            var cascadeSelection = this.mappedElements.get(selection);
            this.selectInternal(selection, true, cascadeSelection);
            this.selected = selection;
        }
    };
    SelectionHandler.prototype.selectInternal = function (element, select, cascadeSelection) {
        if (select) {
            element.classList.add(SelectionHandler.SELECTED);
            if (cascadeSelection) {
                for (var _i = 0, cascadeSelection_1 = cascadeSelection; _i < cascadeSelection_1.length; _i++) {
                    var furtherElement = cascadeSelection_1[_i];
                    furtherElement.classList.add(SelectionHandler.SELECTED);
                }
            }
        }
        else {
            element.classList.remove(SelectionHandler.SELECTED);
            if (cascadeSelection) {
                for (var _a = 0, cascadeSelection_2 = cascadeSelection; _a < cascadeSelection_2.length; _a++) {
                    var furtherElement = cascadeSelection_2[_a];
                    furtherElement.classList.remove(SelectionHandler.SELECTED);
                }
            }
        }
    };
    SelectionHandler.SELECTED = "selected";
    return SelectionHandler;
}(ElementWrapper));
/// <reference path="util.ts" />
/// <reference path="eel.ts" />
var OPT = /** @class */ (function (_super) {
    __extends(OPT, _super);
    function OPT(title, value, description) {
        var _this = _super.call(this, document.createElement('div')) || this;
        _this.title = title;
        _this.setContent(value);
        _this.element.appendChild(_this.content);
        var label = _this.create('span', { "content": title });
        _this.element.appendChild(label);
        var help = _this.create('p', { "content": description });
        _this.element.appendChild(help);
        return _this;
    }
    return OPT;
}(ElementWrapper));
var StringOption = /** @class */ (function (_super) {
    __extends(StringOption, _super);
    function StringOption(title, value, description) {
        return _super.call(this, title, value, description) || this;
    }
    StringOption.prototype.getValue = function () {
        return this.content['value'];
    };
    StringOption.prototype.setContent = function (value) {
        if (this.content) {
            this.element.removeChild(this.content);
        }
        this.content = this.create('input', { 'type': 'text', "value": value });
        this.element.insertBefore(this.content, this.element.firstChild);
    };
    return StringOption;
}(OPT));
var ToggleOption = /** @class */ (function (_super) {
    __extends(ToggleOption, _super);
    function ToggleOption(title, value, description) {
        var _this = _super.call(this, title, value, description) || this;
        _this.element.classList.add('toggle');
        return _this;
    }
    ToggleOption.prototype.getValue = function () {
        return "" + this.content.classList.contains('selected');
    };
    ToggleOption.prototype.setContent = function (value) {
        var _this = this;
        this.selected = value || false;
        var line = this.create('div', { 'classList': 'line horizontal' });
        var circle = this.create('div', { 'classList': 'button' });
        this.content = this.create('button', { 'content': [circle, line], 'classList': this.selected ? 'selected' : '' });
        this.content.addEventListener('click', function () { return _this.handleClick(); });
    };
    ToggleOption.prototype.handleClick = function () {
        if (this.selected) {
            this.content.classList.remove('selected');
            this.selected = false;
        }
        else {
            this.content.classList.add('selected');
            this.selected = true;
        }
    };
    return ToggleOption;
}(OPT));
var NumberOption = /** @class */ (function (_super) {
    __extends(NumberOption, _super);
    function NumberOption(title, value, description) {
        return _super.call(this, title, value, description) || this;
    }
    NumberOption.prototype.getValue = function () {
        return this.content["value"];
    };
    NumberOption.prototype.setContent = function (value) {
        var strValue = value === -1 ? '' : value.toString();
        this.content = this.create('input', { 'type': 'text', "value": strValue });
        this.content.addEventListener('input', this.correctInput, false);
    };
    NumberOption.prototype.correctInput = function () {
        this.content['value'] = this.content['value'].replace(/[^0-9]/g, '');
    };
    return NumberOption;
}(OPT));
var BackendOptions = /** @class */ (function (_super) {
    __extends(BackendOptions, _super);
    function BackendOptions(element) {
        var _this = _super.call(this) || this;
        _this.options = [];
        _this.element = _this.create('div');
        _this.appendSelf(element);
        return _this;
    }
    BackendOptions.prototype.createOption = function (title, type, value, description) {
        var option;
        if (type === 'boolean') {
            value = value || false;
            option = new ToggleOption(title, value, description);
        }
        else if (type === 'string') {
            value = value || '';
            option = new StringOption(title, value, description);
        }
        else if (type === 'number') {
            value = value || -1;
            option = new NumberOption(title, value, description);
        }
        if (option) {
            this.options.push(option);
            option.appendSelf(this.element);
        }
    };
    BackendOptions.prototype.getGenerationOptions = function () {
        for (var _i = 0, _a = this.options; _i < _a.length; _i++) {
            var option = _a[_i];
            if (option.title === 'skip-validation') {
                return { 'skip-validation': option.getValue() };
            }
        }
    };
    BackendOptions.prototype.getSelectedLanguage = function () {
        for (var _i = 0, _a = this.options; _i < _a.length; _i++) {
            var option = _a[_i];
            if (option.title === 'language') {
                return option.getValue();
            }
        }
    };
    BackendOptions.prototype.setSelectedLanguage = function (language) {
        for (var _i = 0, _a = this.options; _i < _a.length; _i++) {
            var option = _a[_i];
            if (option.title === 'language') {
                option.setContent(language);
            }
        }
    };
    BackendOptions.prototype.setup = function (defaults) {
        var _this = this;
        Object.keys(defaults).forEach(function (key) {
            var opt = defaults[key];
            var type = typeof (opt['typevalue']);
            var value = opt['current'];
            var desc = opt['description'];
            _this.createOption(key, type, value, desc);
        });
    };
    BackendOptions.prototype.init = function () {
        var _this = this;
        EEL.availableDefaults(function (defaults) { return _this.setup(defaults); });
    };
    BackendOptions.prototype.save = function () {
        this.options.forEach(function (option) {
            var valueToSet = option.getValue();
            if (valueToSet) {
                EEL.setOption(option.title, valueToSet);
            }
            else {
                EEL.unsetOption(option.title);
            }
        });
    };
    return BackendOptions;
}(ElementWrapper));
var BACKENDOPTIONS = new BackendOptions(document.getElementById('options'));
BACKENDOPTIONS.init();
/// <reference path="options.ts" />
/// <reference path="eel.ts" />
/// <reference path="prism.d.ts" />
var lastGeneratedCode;
d3.select("#code-gen-button").on("click", function () {
    var fsm = {
        'name': graph.name,
        "nodes": graph.nodes,
        "transitions": graph.transitions
    };
    var selectedLanguage = BACKENDOPTIONS.getSelectedLanguage();
    var options = BACKENDOPTIONS.getGenerationOptions();
    EEL.parse(fsm, selectedLanguage, options, function (code, error) { return displayCode(code, error, selectedLanguage); });
});
d3.select("#toggle-code-button").on("click", function () {
    var btn = d3.select("#toggle-code-button");
    var select = !btn.classed('selected');
    btn.classed('selected', select);
    d3.select("#text-area").classed('selected', select);
});
d3.select("#delete-btn").on("click", function () {
    d3.select("#code-container").html("");
    d3.select("#toggle-code-button").classed("error", false);
    graph.transitions = [];
    graph.nodes = [];
    i = 0;
    j = 0;
    render();
});
d3.select('#save-options-btn').on('click', function () { return BACKENDOPTIONS.save(); });
d3.select('#clear-options-btn').on('click', function () { return EEL.unsetAllOptions(); });
d3.select('#save-as-svg-btn').on('click', function () { return saveSVG(); });
d3.select('#save-as-png-btn').on('click', function () { return savePNG(); });
d3.select('#save-as-json-btn').on('click', function () { return saveJson(); });
d3.select('#save-code-btn').on('click', function () { return saveLastGeneratedCode(); });
var nameField = d3.select('#graph-name-field')
    .on('focusout', function () { return changedGraphName(); })
    .on("keypress", function () {
    if (d3.event.keyCode == 13) {
        changedGraphName();
        var input = nameField.node();
        input.blur();
    }
})
    .on("focus", function () {
    var input = nameField.node();
    input.select();
});
function changedGraphName() {
    var newName = changedLabel(nameField, d3.event);
    nameField.property("value", newName);
    graph.name = newName;
}
function saveLastGeneratedCode() {
    if (lastGeneratedCode) {
        saveCode(lastGeneratedCode[0], lastGeneratedCode[1]);
    }
    else {
        window.alert('No valid code can be saved!');
    }
}
function displayCode(code, error, language) {
    if (error) {
        lastGeneratedCode = undefined;
        d3.select("#code-container")
            .html("ERROR:\n\n" + error)
            .classed("error", true);
        d3.select('#toggle-code-button')
            .classed("error", true);
    }
    else {
        lastGeneratedCode = [code, language];
        var codeContainer = d3.select("#code-container");
        if (d3.select('#text-area').classed('selected')) {
            codeContainer
                .html("<pre><code class=\"language-" + language + "\">" + code + "</code></pre>")
                .classed("error", false);
            d3.select("#toggle-code-button")
                .classed("error", false);
            Prism.highlightAllUnder(document.getElementById("code-container"));
        }
        else {
            saveCode(code, language);
        }
    }
}
function setVersion(version) {
    d3.select("#version-span").html("Version: " + version);
}
EEL.getVersion(setVersion);
/**
 * Class to setup navigation of tutorial pages.
 */
var TutorialHelp = /** @class */ (function (_super) {
    __extends(TutorialHelp, _super);
    function TutorialHelp() {
        var _this = _super.call(this) || this;
        _this.selection = new SelectionHandler();
        return _this;
    }
    TutorialHelp.prototype.init = function () {
        var items = document.querySelectorAll('.help-item');
        for (var index = 0; index < items.length; index++) {
            var item = items[index];
            var previousBtn = this.createButton("previous");
            var nextBtn = this.createButton("next");
            var div = this.create('div', { 'classList': 'navigate', "content": [previousBtn, nextBtn] });
            if (index > 0) {
                this.selection.addOption(previousBtn, [items[index - 1]]);
            }
            else {
                previousBtn.classList.add('disabled');
            }
            if (index < items.length - 1) {
                this.selection.addOption(nextBtn, [items[index + 1]]);
            }
            else {
                nextBtn.classList.add('disabled');
            }
            if (index === 1) {
                // Initially display first tutorial page
                this.selection.select(previousBtn);
            }
            item.appendChild(div);
        }
    };
    TutorialHelp.prototype.createButton = function (s) {
        return this.create('button', { "content": s, "classList": s });
    };
    return TutorialHelp;
}(Creator));
var TUTORIAL = new TutorialHelp();
TUTORIAL.init();
function setInfo(info) {
    info = info.replace(/\\n|"/g, "")
        .replace(/\\u00a9/g, '&copy;')
        .replace(/<p><img(.*?)<\/p>/g, "");
    var article = d3.create("article")
        .html(info)
        .node();
    // Clear shell info code
    var shell = "\\shell\\";
    var languageshell = "language-shell";
    article.querySelectorAll(".\\" + shell + "\\").forEach(function (code) {
        code.classList.remove(shell);
        code.classList.add(languageshell);
        code.innerHTML = code.innerHTML.replace(/ /g, "  ")
            .replace(/        -/g, "\n\n    -")
            .replace(/#/g, "\n#")
            .replace(/\$/g, "\n\n$");
    });
    // Clear json info code
    var json = "\\json\\";
    var languagejson = "language-json";
    article.querySelectorAll(".\\" + json + "\\").forEach(function (code) {
        code.classList.remove(json);
        code.classList.add(languagejson);
        code.innerHTML = code.innerHTML.replace("{", "\n{")
            .replace(/\s\s+{/g, "\n   {")
            .replace(/\s\s+"/g, '\n"')
            .replace(/\s\s+]/g, "\n]");
    });
    // Clear .bead info code
    var codes = article.querySelectorAll("code");
    var beadCode = codes[codes.length - 1];
    beadCode.innerHTML = beadCode.innerHTML.replace(/\s\s+/g, "\n")
        .replace("#!", "\n#!");
    article.querySelectorAll("p a").forEach(function (a) {
        var link = a;
        link.innerHTML = link.href.replace(/http:\/\/localhost:[0-9]*\//g, "");
    });
    var logo = d3.create("img")
        .attr("src", "media/logo.png")
        .node();
    article.insertBefore(logo, article.firstChild);
    Prism.highlightAllUnder(article);
    document.getElementById("info").appendChild(article);
}
EEL.getInfo(setInfo);
/// <reference path="util.ts"/>
/// <reference path="prism.d.ts" />
var previewGraph = {
    'name': 'PreviewGraph',
    'nodes': [
        { id: "Initial", start: true },
        { id: "Intermediate" },
        { id: "End" }
    ],
    'transitions': [
        { label: "step", from: "Initial", to: "Intermediate", visible: true, offset: null },
        { label: "step", from: "Intermediate", to: "End", visible: true, offset: null },
        { label: "back", from: "End", to: "Intermediate", visible: true, offset: null },
        { label: "back", from: "Intermediate", to: "Initial", visible: true, offset: null },
        { label: "finish", from: "Initial", to: "End", visible: true, offset: null }
    ]
};
/**
 * Class representing a language.
 * It is used to generate a Preview for the code generated with this language template.
 */
var LanguagePreview = /** @class */ (function (_super) {
    __extends(LanguagePreview, _super);
    function LanguagePreview(language) {
        var _this = _super.call(this) || this;
        _this.language = language;
        var graph = _this.create('img', { 'src': LanguagePreview.IMG_SRC });
        var innerDiv = _this.create('div', { 'content': [graph] });
        var pre = _this.create('pre', { 'classList': "language-" + language });
        _this.element = _this.create('div', { 'content': [innerDiv, pre] });
        EEL.parse(previewGraph, _this.language, LanguagePreview.OPTS, function (code, error) {
            if (error) {
                console.log(error);
                pre.innerHTML = "No code preview available!";
            }
            else {
                pre.appendChild(_this.create('code', { 'content': code }));
                Prism.highlightAllUnder(pre);
            }
        });
        return _this;
    }
    LanguagePreview.IMG_SRC = "media/language-graph.svg";
    LanguagePreview.OPTS = { "skip-validation": true };
    return LanguagePreview;
}(ElementWrapper));
/**
 * Wrapper for all language previews.
 */
var LanguageHelp = /** @class */ (function (_super) {
    __extends(LanguageHelp, _super);
    function LanguageHelp(container) {
        var _this = _super.call(this, document.createElement('ul')) || this;
        _this.container = container;
        var creator = function (language) {
            var option = _this.create('li', { "id": language, "content": language });
            option.addEventListener("click", function () { return BACKENDOPTIONS.setSelectedLanguage(language); });
            return option;
        };
        _this.selection = new SelectionHandler(_this.element, creator);
        _this.selection.appendSelf(_this.container);
        return _this;
    }
    LanguageHelp.prototype.appendPreview = function (preview) {
        preview.appendSelf(this.container);
        this.selection.createOption(preview.language, [preview.element]);
    };
    LanguageHelp.prototype.init = function () {
        var _this = this;
        EEL.availableLanguages(function (languages) {
            languages.forEach(function (language) {
                _this.appendPreview(new LanguagePreview(language));
            });
        });
    };
    return LanguageHelp;
}(ElementWrapper));
var LANGUAGES = new LanguageHelp(document.getElementById('languages'));
LANGUAGES.init();
/// <reference path="./util.ts"/>
/**
 * Wrapper class for the gui menu.
 */
var Menu = /** @class */ (function (_super) {
    __extends(Menu, _super);
    function Menu(element) {
        var _this = _super.call(this, element) || this;
        _this.selection = new SelectionHandler(_this.element);
        return _this;
    }
    Menu.prototype.init = function () {
        this.putMenuOption('help-btn', 'help');
        this.putMenuOption('info-btn', 'info');
        this.putMenuOption('languages-btn', 'languages');
        this.putMenuOption('options-btn', 'options');
    };
    Menu.prototype.putMenuOption = function (buttonId, sectionId) {
        var section = document.getElementById(sectionId);
        var button = document.getElementById(buttonId);
        this.selection.addOption(button, [this.element, section]);
    };
    return Menu;
}(ElementWrapper));
var MENU = new Menu(document.getElementById('menu'));
MENU.init();
var ResizeHandler = /** @class */ (function (_super) {
    __extends(ResizeHandler, _super);
    function ResizeHandler(element) {
        var _this = _super.call(this, element) || this;
        var listener = function (mousemove) { return _this.resize(mousemove); };
        _this.element.addEventListener("mousedown", function (mousedown) {
            var undraggableSpace = parseInt(getComputedStyle(_this.element, '').width) - ResizeHandler.DRAGGABLE_BORDER_SIZE - 2;
            if (mousedown.offsetX > undraggableSpace) {
                _this.position = mousedown.x;
                document.addEventListener("mousemove", listener, false);
            }
        }, false);
        document.addEventListener("mouseup", function () {
            document.removeEventListener("mousemove", listener, false);
        }, false);
        return _this;
    }
    ResizeHandler.prototype.resize = function (mousemove) {
        var distance = this.position - mousemove.x;
        this.position = mousemove.x;
        var newWidth = parseInt(getComputedStyle(this.element, '').width) - distance;
        this.element.style.width = newWidth + "px";
    };
    ResizeHandler.DRAGGABLE_BORDER_SIZE = 8;
    return ResizeHandler;
}(ElementWrapper));
var CODERESIZER = new ResizeHandler(document.getElementById('text-area'));

#! arangosh

var analyzers = require("@arangodb/analyzers");

var normalize = analyzers.save("norm_accent_lower","norm", {
    locale: "en.utf-8",
    accent: false,
    case: "lower"
},  ["frequency", "norm", "position"]);

var text = analyzers.save("text_en", "text", {
    locale: "en.utf-8",
    case: "lower",
    accent: false,
    stemming: false,
    stopwords: []
}, ["frequency", "norm", "positiion"])
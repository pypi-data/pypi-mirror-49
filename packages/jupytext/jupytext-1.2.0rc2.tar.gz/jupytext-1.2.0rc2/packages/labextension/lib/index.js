"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const apputils_1 = require("@jupyterlab/apputils");
const notebook_1 = require("@jupyterlab/notebook");
const JUPYTEXT_FORMATS = [
    {
        formats: "ipynb,auto:light",
        label: "Pair Notebook with light Script"
    },
    {
        formats: "ipynb,auto:percent",
        label: "Pair Notebook with percent Script"
    },
    {
        formats: "ipynb,auto:hydrogen",
        label: "Pair Notebook with Hydrogen Script"
    },
    {
        formats: "ipynb,md",
        label: "Pair Notebook with Markdown"
    },
    {
        formats: "ipynb,Rmd",
        label: "Pair Notebook with R Markdown"
    },
    {
        formats: "custom",
        label: "Custom pairing"
    },
    {
        formats: "none",
        label: "Unpair Notebook"
    }
];
/**
 * Initialization data for the jupyterlab-jupytext extension.
 */
const extension = {
    id: "jupyterlab-jupytext",
    autoStart: true,
    requires: [apputils_1.ICommandPalette, notebook_1.INotebookTracker],
    activate: (app, palette, notebook_tracker) => {
        console.log("JupyterLab extension jupyterlab-jupytext is activated");
        // Jupytext formats
        JUPYTEXT_FORMATS.forEach((args, rank) => {
            const formats = args["formats"];
            const command = "jupytext:" + formats;
            app.commands.addCommand(command, {
                label: args["label"],
                isToggled: () => {
                    if (!notebook_tracker.currentWidget)
                        return false;
                    if (!notebook_tracker.currentWidget.context.model.metadata.has("jupytext"))
                        return formats == "none";
                    const jupytext = notebook_tracker.currentWidget.context.model.metadata.get("jupytext");
                    if (!jupytext.formats)
                        return formats == "none";
                    const lang = notebook_tracker.currentWidget.context.model.metadata.get("language_info");
                    const jupytext_formats = lang
                        ? jupytext.formats.replace("," + lang.file_extension.substring(1) + ":", ",auto:")
                        : jupytext.formats;
                    if (formats == "custom")
                        return (jupytext_formats &&
                            [
                                "ipynb,auto:light",
                                "ipynb,auto:percent",
                                "ipynb,auto:hydrogen",
                                "ipynb,md",
                                "ipynb,Rmd"
                            ].indexOf(jupytext_formats) < 0);
                    return jupytext_formats == formats;
                },
                isEnabled: () => {
                    if (!notebook_tracker.currentWidget)
                        return false;
                    if (formats == "custom" || formats == "none")
                        return true;
                    const notebook_extension = notebook_tracker.currentWidget.context.path.split('.').pop();
                    if (notebook_extension == "ipynb")
                        return true;
                    if (notebook_extension == "md")
                        return formats == "ipynb,md";
                    if (notebook_extension == "Rmd")
                        return formats == "ipynb,Rmd";
                    return formats != "ipynb,md" && formats != "ipynb,Rmd";
                },
                execute: () => {
                    console.log("Jupytext: executing command=" + command);
                    if (formats == "custom") {
                        alert("Please edit the notebook metadata directly if you wish a custom configuration.");
                        return;
                    }
                    const jupytext = notebook_tracker.currentWidget.context.model.metadata.get("jupytext");
                    if (formats == "none") {
                        if (!notebook_tracker.currentWidget.context.model.metadata.has("jupytext"))
                            return;
                        if (jupytext.formats) {
                            delete jupytext.formats;
                        }
                        if (Object.keys(jupytext).length == 0)
                            notebook_tracker.currentWidget.context.model.metadata.delete("jupytext");
                        return;
                    }
                    // set desired format
                    if (jupytext)
                        jupytext.formats = formats;
                    else
                        notebook_tracker.currentWidget.context.model.metadata.set("jupytext", { formats });
                }
            });
            console.log("Jupytext: adding command=" + command + " with rank=" + (rank + 1));
            palette.addItem({ command, rank: rank + 2, category: "Jupytext" });
        });
        // Jupytext's documentation
        palette.addItem({
            args: {
                text: "Jupytext Reference",
                url: "https://jupytext.readthedocs.io/en/latest/"
            },
            command: "help:open",
            category: "Jupytext",
            rank: 0
        });
        palette.addItem({
            args: {
                text: "Jupytext FAQ",
                url: "https://jupytext.readthedocs.io/en/latest/faq.html"
            },
            command: "help:open",
            category: "Jupytext",
            rank: 1
        });
        // Metadata in text representation    
        app.commands.addCommand("jupytext_metadata", {
            label: "Include Metadata",
            isToggled: () => {
                if (!notebook_tracker.currentWidget)
                    return false;
                if (!notebook_tracker.currentWidget.context.model.metadata.has("jupytext"))
                    return false;
                const jupytext = notebook_tracker.currentWidget.context.model.metadata.get("jupytext");
                if (jupytext.notebook_metadata_filter === '-all')
                    return false;
                return true;
            },
            isEnabled: () => {
                if (!notebook_tracker.currentWidget)
                    return false;
                if (!notebook_tracker.currentWidget.context.model.metadata.has("jupytext"))
                    return false;
                const jupytext = notebook_tracker.currentWidget.context.model.metadata.get("jupytext");
                if (jupytext.notebook_metadata_filter === undefined)
                    return true;
                if (jupytext.notebook_metadata_filter === '-all')
                    return true;
                return false;
            },
            execute: () => {
                console.log("Jupytext: toggling YAML header");
                if (!notebook_tracker.currentWidget)
                    return;
                if (!notebook_tracker.currentWidget.context.model.metadata.has("jupytext"))
                    return;
                const jupytext = notebook_tracker.currentWidget.context.model.metadata.get("jupytext");
                if (jupytext.notebook_metadata_filter) {
                    delete jupytext.notebook_metadata_filter;
                    if (jupytext.cell_metadata_filter === '-all')
                        delete jupytext.cell_metadata_filter;
                    return;
                }
                jupytext.notebook_metadata_filter = '-all';
                if (jupytext.cell_metadata_filter === undefined)
                    jupytext.cell_metadata_filter = '-all';
            }
        });
        palette.addItem({ command: "jupytext_metadata", rank: JUPYTEXT_FORMATS.length + 3, category: "Jupytext" });
    }
};
exports.default = extension;

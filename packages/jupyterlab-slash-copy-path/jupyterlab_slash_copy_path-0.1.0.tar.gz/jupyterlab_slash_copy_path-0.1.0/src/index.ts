import {
  IFileBrowserFactory
} from '@jupyterlab/filebrowser';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  Clipboard,
} from '@jupyterlab/apputils';


/**
 * Initialization data for the @epi2melabs/jupyterlab-slash-copy-path extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@epi2melabs/jupyterlab-slash-copy-path:plugin',
  autoStart: true,
  requires: [IFileBrowserFactory],
  activate: (app: JupyterFrontEnd, factory: IFileBrowserFactory) => {
    console.log('JupyterLab extension @epi2melabs/jupyterlab-slash-copy-path is activated!');
    const { commands } = app;
    const { tracker } = factory;

    commands.commandExecuted.connect((_, e) => {
      if (e.id !== "filebrowser:copy-path") {
        return;
      }

      const widget = tracker.currentWidget;
      if (!widget) {
        return;
      }

      const item = widget.selectedItems().next();
      if (!item) {
        return;
      }

      Clipboard.copyToSystem(`/${item.path}`);
    })
  }
};

export default plugin;
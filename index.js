'use strict'

require('babel-register');

const electron = require('electron');
const {ipcMain} = require('electron');
const app = electron.app;

// adds debug features like hotkeys for triggering dev tools and reload
require('electron-debug')();

// prevent window being garbage collected
let mainWindow;

function onClosed() {
	// dereference the window
	// for multiple windows store them in an array
	mainWindow = null;
}

function createMainWindow() {
	const win = new electron.BrowserWindow({
		width: 600,
		height: 520
	});

	win.loadURL(`file://${__dirname}/index.html`);
	win.isResizable = true
	win.on('closed', onClosed);
	win.setMenu(null);
	return win;
}

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.on('activate', () => {
	if (!mainWindow) {
		mainWindow = createMainWindow();
	}
});

app.on('ready', () => {
	mainWindow = createMainWindow();
});

ipcMain.on('resize-window', (event, w, h) => {
	h = h > 720 ? 720 : h
	mainWindow.setSize(w, h)
})

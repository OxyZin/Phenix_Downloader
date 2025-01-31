const { app, BrowserWindow } = require('electron');

function createwindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600

    });

    win.loadFile('src/index.html')
}

app.whenReady().then(createwindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
})

module.exports = {
    // ...
    packagerConfig: {
      icon: '/src/images/icon.ico' // no file extension required
    }
    // ...
  };
migrate((app) => {
    const settings = app.settings();
    settings.batch.enabled = true;
    settings.batch.maxRequests = 1000;
    app.save(settings);
}, (app) => {
    // Revert changes
    const settings = app.settings();
    settings.batch.enabled = false;
    settings.batch.maxRequests = 50;
    app.save(settings);
})
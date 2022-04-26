module.exports = {
    // changed to put dist inside backend folder
    outputDir: '../backend/dist',   

    // relative to outputDir
    // moves css, js, and img inside a static folder
    assetsDir: 'static',     

    // Need to restart when making changes here
    // Side note: Wasted about two hours
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://localhost:5000',
                changeOrigin: true,
                logLevel: 'debug',
                pathRewrite: {'^/api': '/api'},
            },
        }
    }
}
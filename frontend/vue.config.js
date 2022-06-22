module.exports = {
    // Need to restart when making changes here
    // Side note: Wasted about two hours
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://server.it-humke.de:9004',
                changeOrigin: true,
                pathRewrite: {'^/api': '/api'},
            },
        }
    }
}
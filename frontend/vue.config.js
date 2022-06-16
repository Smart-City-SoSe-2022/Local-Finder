module.exports = {
    // Need to restart when making changes here
    // Side note: Wasted about two hours
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://'+process.env.VUE_APP_URL,
                changeOrigin: true,
                pathRewrite: {'^/api': '/api'},
            },
        }
    }
}
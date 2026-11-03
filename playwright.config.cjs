const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'./tests',testMatch:'browser.spec.cjs',use:{baseURL:'http://127.0.0.1:8000',headless:true},webServer:{command:'python3 -m http.server 8000 --bind 0.0.0.0 --directory site',url:'http://127.0.0.1:8000',reuseExistingServer:true},reporter:'list'});

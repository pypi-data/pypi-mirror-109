
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "hbhoiqfd-3",
                            password: "uld8v8yp9d5m"
                        }
                    };
                }
                
                browser.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
                );
               
from parse_package.proxy import protocol, login, password, ip, port

proxies_with_password = {
    f'{protocol}': f'{protocol}://{login}:{password}@{ip}:{port}'
}

# Sing in by ip
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "_proxies",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = f"""
var config = {{
        mode: "fixed_servers",
        rules: {{
        singleProxy: {{
            scheme: "{protocol}",
            host: "{ip}",
            port: parseInt({port})
        }},
        bypassList: ["localhost"]
        }}
    }};

chrome._proxies.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{login}",
            password: "{password}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
);
"""

cookies = {
}

headers = {
}

json_data = {
}

url = 'your_url'

if __name__ == '__main__':
    print()

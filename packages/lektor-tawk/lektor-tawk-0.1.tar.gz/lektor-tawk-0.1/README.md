# Lektor Tawk

This plugin adds support for Tawk to Lektor. Once the plugin is enabled a render_tawk function will render a Tawk Live Chat.

## Enabling the Plugin

To enable the plugin add this to your project file:

```
$ lektor plugins add lektor-tawk
```

## Configuring the Plugin

The plugin has a config file that is needed to inform it about your website. Just create a file named tawk.ini into your configs/ folder and configure the live_chat_code key with the ID if your Tawk:

```
live_chat_code = your_live_chat_code
```

## In Templates

Now you can render to any of your templates by just using the render_tawk function. Just calling it is enough to get the live chat:

```
<div>{{ render_tawk }}</div>
```

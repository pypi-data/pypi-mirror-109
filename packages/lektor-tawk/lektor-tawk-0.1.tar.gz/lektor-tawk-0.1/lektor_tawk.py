# -*- coding: utf-8 -*-
from markupsafe import Markup

from lektor.pluginsystem import Plugin

SCRIPT = '''
    <script type="text/javascript">
    var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
        (function(){
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/%(live_chat_code)s';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
    })();
    </script>
'''

class TawkPlugin(Plugin):
    name = 'Lektor Tawk'
    description = u'Lektor plugin to add Tawk to a website.'

    def on_setup_env(self):
        live_chat_code = self.get_config().get('live_chat_code')

        if live_chat_code is None:
            raise RuntimeError('live_chat_code is not configured. '
                               'Please configure it in '
                               '`./configs/tawk.ini` file')

        def tawk():
            return Markup(SCRIPT % {'live_chat_code': live_chat_code})

        self.env.jinja_env.globals['render_tawk'] = tawk

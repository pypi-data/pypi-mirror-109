from nerdvision.plugins import Plugin, DidNotEnable

try:
    from ddtrace import Span, tracer  # type: ignore
except ImportError as e:
    raise DidNotEnable("ddtrace is not installed", e)


class DatadogAPMPlugin(Plugin):
    def load_plugin(self, nerdvision):
        old_set_exc_info = Span.set_exc_info

        def wrapped_set_exc_info(self, exc_type, exc_val, exc_tb):
            nerdvision.capture_exception(exc_type, exc_val, exc_tb)
            return old_set_exc_info(self, exc_type, exc_val, exc_tb)

        Span.set_exc_info = wrapped_set_exc_info

        def nv_dd_decorator(data):
            span = tracer.current_span()
            if span is not None:
                span.set_tag('nerdvision.link', 'https://app.nerd.vision/context/%s' % data['id'])
                return 'dd_trace', {
                    'name': 'DataDog',
                    'icon': 'https://branding.nerd.vision/external_assets/dd_icon_rgb.svg',
                    'span': span.span_id,
                    'trace': span.trace_id
                }
            return None

        nerdvision.add_context_decorator(nv_dd_decorator)

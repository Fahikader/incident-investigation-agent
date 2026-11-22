from strands.hooks import HookProvider, HookRegistry, BeforeToolCallEvent, AfterToolCallEvent

class InvestigationHook(HookProvider):
    def __init__(self, max_tool_calls: int = 8):
        self.max_tool_calls = max_tool_calls
        self.calls = 0
        self.trace = []

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.before_tool)
        registry.add_callback(AfterToolCallEvent, self.after_tool)

    def before_tool(self, event: BeforeToolCallEvent) -> None:
        self.calls += 1
        if self.calls > self.max_tool_calls:
            raise RuntimeError("Stopped: Agent reached max tool calls limit.")

    def after_tool(self, event: AfterToolCallEvent) -> None:
        self.trace.append({
            "step": self.calls,
            "tool": event.tool_use["name"],
            "input": event.tool_use["input"],
        })
